import json

class JsonSocket:
    """A socket that reads and writes json objects."""

    def __init__(self, socket):
        """Create a JsonSocket wrapping the provided socket."""
        self._socket = socket

    def read_json(self):
        """Read an object."""
        buffer = b""
        while not buffer.endswith(b"\r\n"):
            buffer += self._socket.read(1024)

        return json.loads(buffer.decode("UTF-8"))

    def write_json(self, obj):
        """Write an object."""
        buffer = ("%s\r\n" % json.dumps(obj)).encode("ASCII")
        self._socket.write(buffer)