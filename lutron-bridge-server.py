import asyncio
from types import FunctionType

from pylutron_caseta.smartbridge import Smartbridge
import socket
import threading
import select
from time import sleep

debug_log = True

bind_ip = 'localhost'
bind_port = 5000
server = None



if(debug_log):
    print('Listening on {}:{}'.format(bind_ip, bind_port))


async def lutron_command(id: str, parameter: int):
    # `Smartbridge` provides an API for interacting with the Caséta bridge.
    bridge = Smartbridge.create_tls(
        "192.168.11.50", "caseta.key", "caseta.crt", "caseta-bridge.crt",
        systemType="homeworks"
    )

    state = -1

    await bridge.connect()

    if parameter > 3:
        state = await bridge.get_led_status(id)
    else: 
        await bridge.sim_press_button(id, parameter)

    await bridge.close()
    return state

def handle_client_connection(client_socket: socket, stop: FunctionType):
    while not stop():
        # check if there is something in the socket, wait for one second to allow stopping thread
        r, _, _ = select.select((client_socket,), [], [], 1)
        if r:
            print("Receiving")
            #we have data in the socket
            request = client_socket.recv(1024)
            if not request:
                # Socket has been closed
                client_socket.close()
                exit()
            if(debug_log):
                # #DEVICE,{ADDRESS},{PARAMETER}
                print(request)
            try:
                elements = request.decode("utf-8").split(",")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                print(elements[1].lstrip())
                print(int(elements[2]))
                state = loop.run_until_complete(lutron_command(elements[1].lstrip(), int(elements[2])))
                if(state >= 0):
                    response = f"~DEVICE,{elements[1]},{state}\r\n"
                    client_socket.send(response.encode())
            except Exception as err:
                print(f'Error occured during lutron processing: {err}')
                
            finally:
                loop.close()
    
    client_socket.close()

if __name__ == '__main__':
    stop_client_sockets = False
    client_socket_threads = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    

    while True:
        try:
            client_sock, address = server.accept()
            if(debug_log):
                print('Accepted connection from {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(client_sock, lambda: stop_client_sockets)
            )
            client_socket_threads.append(client_handler)
            client_handler.start()
        except KeyboardInterrupt:
            # CTRL-C pressed
            stop_client_sockets = True
            for thread in client_socket_threads:
                thread.join()
            server.close()
            exit(0)
