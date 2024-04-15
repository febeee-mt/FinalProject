from arduino_connect.arduino_conn import ArduinoConnection
import json
import time
def main():
    ard = ArduinoConnection('rfc2217://localhost:4000', 9600, 10, 'URL')
    while True:
        try:
            strs=""
            data=input("> ")
            ard.execute('w', data)
            a=ard.execute('r')
            for i in a:
                strs+=i.decode('utf-8')
            
            print(json.loads(strs))
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()