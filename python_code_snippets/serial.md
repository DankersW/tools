# Serial wrapper

## Simple sync Serial interface
```python
from serial import Serial
from typing import List
from collections import namedtuple

class SerialInterface:
    _default_config: dict = {'port': '/dev/ttyACM0', 'baudrate': 115200, 'term_seq': b'> ', 'timeout': 1}

    def __init__(self, config: dict = None) -> None:
        if config is None:
            config = self._default_config
        self.config = namedtuple('config', config.keys())(**config)

    def execute(self, cmd: str) -> List[str]:
        print(f"Executing: {cmd}")
        _cmd = self._add_line_ending(line=cmd)
        rx_buffer = []
        with Serial(port=self.config.port, baudrate=self.config.baudrate, timeout=self.config.timeout) as serial:
            serial.write(_cmd.encode())
            while True:
                rx_data = serial.readline()
                if rx_data == self.config.term_seq:
                    break
                line_buffer = rx_data.decode('ascii').rstrip()
                if line_buffer != "":
                    rx_buffer.append(line_buffer)
        return rx_buffer

    @staticmethod
    def _add_line_ending(line: str) -> str:
        if line[-1] != '\r':
            line += '\r'
        return line


if __name__ == '__main__':
    serial_interface = SerialInterface()
    result = serial_interface.execute(cmd="cli colors off\r")
    print(result)

    result = serial_interface.execute(cmd="mesh enable\r")
    print(result)
    result = serial_interface.execute(cmd="mesh list")
    print(result)
```