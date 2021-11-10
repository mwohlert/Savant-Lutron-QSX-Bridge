import asyncio
import sys
from types import FunctionType

from pylutron_caseta.smartbridge import Smartbridge
import logging
import socket
import threading
import select
import optparse
from pathlib import Path

from utils.setup import generateAndSignCertificate, generatePrivateKey, pingLeapHost

debug_log = True
bind_ip = 'localhost'
bind_port = 5000
server = None

lutron_client_key_name = "caseta.key"
lutron_client_key_path = Path.cwd().joinpath(lutron_client_key_name)
lutron_client_cert_name = "caseta.crt"
lutron_client_cert_path = Path.cwd().joinpath(lutron_client_cert_name)
lutron_bridge_ca_cert_name = "caseta-bridge.crt"
lutron_bridge_ca_cert_path = Path.cwd().joinpath(lutron_bridge_ca_cert_name)

lutron_loop = asyncio.new_event_loop()
asyncio.set_event_loop(lutron_loop)

bridge : Smartbridge = None


logging.basicConfig(
  level=logging.INFO if not debug_log else logging.DEBUG,
  format="%(asctime)s [%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler("bridge.log"),
    logging.StreamHandler()
  ]
)


async def lutron_command(id: str, parameter: int):
  state = -1
  if parameter > 3:
    state = await bridge.get_led_status(id)
  else:
    await bridge.sim_press_button(id, parameter)

  return state


def handle_client_connection(client_socket: socket, stop: FunctionType):
  while not stop():
    # check if there is something in the socket, wait for one second to allow stopping thread
    r, _, _ = select.select((client_socket,), [], [], 1)
    if r:
      # we have data in the socket
      request = client_socket.recv(1024)
      if not request:
        # Socket has been closed
        break
      logging.info(f'Received request: {request}')
      try:
        elements = request.decode("utf-8").split(",")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        state = loop.run_until_complete(lutron_command(
          elements[1].lstrip(), int(elements[2])))
        if(state >= 0):
          response = f"~DEVICE,{elements[1]},{state}"
          logging.info(f'Response to Savant: {response}')
          client_socket.send(response.encode())
      except Exception as err:
        logging.error(f'Error occured during lutron processing: {err}')

      finally:
        loop.close()

  client_socket.close()


def setup_bridge(host: str):
  logging.info(
      "Lutron QSX processor has not been paired to this program yet")
  logging.info("Generating private key")
  priv_key = generatePrivateKey(lutron_client_key_path)
  logging.info("Asking QSX processor to accept our key")
  generateAndSignCertificate(
      logging, host, priv_key, lutron_client_cert_path, lutron_bridge_ca_cert_path)

def start_bridge(host: str):
  stop_client_sockets = False
  client_socket_threads = []
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind((bind_ip, bind_port))
  server.listen(5)  # max backlog of connections
  logging.info('Listening on {}:{}'.format(bind_ip, bind_port))

  while True:
    try:
      client_sock, address = server.accept()
      logging.info('Accepted connection from {}:{}'.format(
        address[0], address[1]))
      client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock, lambda: stop_client_sockets)
      )
      client_socket_threads.append(client_handler)
      client_handler.start()
    except KeyboardInterrupt:
      # CTRL-C pressed
      logging.info("Shutting down bridge")
      stop_client_sockets = True
      for thread in client_socket_threads:
        thread.join()
      server.close()
      exit(0)

async def connect_to_lutron(host: str):

  bridge = Smartbridge.create_tls(
    host, lutron_client_key_name, lutron_client_cert_name, lutron_bridge_ca_cert_name,
    systemType_str="homeworks"
  )

  await bridge.connect()


required_options = "host".split()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--host', dest='host',
                      help='Hostname/IP Address of the Lutron QSX processor')

    (options, args) = parser.parse_args()
    for r in required_options:
        if options.__dict__[r] is None:
            parser.error("parameter %s required" % r)
            parser.print_usage()

    host = options.host

    # Check if client certificate has been generated
    if not lutron_client_key_path.exists() or not lutron_client_cert_path.exists() or not lutron_bridge_ca_cert_path.exists():
        setup_bridge(host)

    logging.info("Verifying connection to QSX processor")
    ping_res = pingLeapHost(host, lutron_client_cert_path,
                            lutron_client_cert_path, lutron_bridge_ca_cert_path)
    if not ping_res:
      logging.error("Failed to connect to QSX processor. Please try restarting this application and/or the lutron QSX processor. Otherwise delete all the certificate and start fresh")
      sys.exit(1)

    logging.info("Connecting to QSX processor")
    lutron_loop.run_until_complete(connect_to_lutron(host))

    start_bridge(host)
