import serial
import time

class ArduinoConnection:
    baudrate: int
    conn_type: str
    __serial_obj: serial.Serial

    def __init__(self, __port: str, __baudrate: int, __timeout: int = 10,  __conn_type: str = 'COM') -> None:
        self.conn_type = __conn_type
        self.baudrate = __baudrate
        try:
            if __conn_type == 'URL':
                self.__serial_obj = serial.serial_for_url(__port, baudrate=self.baudrate, timeout=__timeout)
            else:
                self.__serial_obj = serial.Serial(__port, baudrate=self.baudrate, timeout=__timeout)
        except:
            print('Arduino not connected')
        

    def execute(self, type_op: str, data: str=''):
        with self.__serial_obj as ser:
            if type_op == 'r':
                return self.__wait_for_response(ser)
            
            if type_op == 'w':
                ser.write(bytes(data, 'UTF-8'))


    def __wait_for_response(self, ser: serial.Serial):
        time_count=0
        new_str=[]
        character=ser.read()
        while character !=b';':
            start = time.time()
            new_str.append(character)
            character=ser.read()
            end = time.time()
            time_count+= (end-start)
            if time_count > 6:
                raise Exception("ERROR TIMEOUT")

        return new_str