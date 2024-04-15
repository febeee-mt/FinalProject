import unittest
from arduino_connect.arduino_conn import ArduinoConnection
import json


PORT = 'rfc2217://localhost:4000'
CONN_TYPE='URL'

class TestArduinoCases(unittest.TestCase):
    
    def setUp(self) -> None:
        self.ardu = ArduinoConnection(PORT, 9600, 10, CONN_TYPE)


    #@unittest.skip('Skipped')
    def test_get_data_responses_block_state_1(self):
        self.ardu.execute('w', 'CS:1')
        self.ardu.execute('r')
        for i in range(1,11):
            strs=""
            self.ardu.execute('w', 'GD')
            a=self.ardu.execute('r')
            for i in a:
                strs+=i.decode('utf-8')
                
            self.assertEqual(json.loads(strs)['msg'], 'Ok')


    #@unittest.skip('Skipped')
    def test_get_data_responses_block_state_2(self):
        self.ardu.execute('w', 'CS:2')
        self.ardu.execute('r')
        for i in range(1,11):
            strs=""
            self.ardu.execute('w', 'GD')
            a=self.ardu.execute('r')
            for i in a:
                strs+=i.decode('utf-8')
                
            self.assertEqual(json.loads(strs)['msg'], 'Ok')

    #@unittest.skip('Skipped')
    def test_change_state(self):
        for x in ['1', '2']:
            strs=""
            self.ardu.execute('w', f'CS:{x}')
            a=self.ardu.execute('r')
            for i in a:
                strs+=i.decode('utf-8')


            self.assertDictEqual(json.loads(strs), {'data': {'state': x}, 'err': 0, 'msg': 'Ok'})


    #@unittest.skip('Skipped')
    def test_get_data_state_1(self):
        strs=""
        self.ardu.execute('w', 'CS:1')
        self.ardu.execute('r')
        self.ardu.execute('w', 'GD')
        a=self.ardu.execute('r')
        for i in a:
            strs+=i.decode('utf-8')
                
        self.assertIn('INs', json.loads(strs)['data'].keys())
        self.assertIn('OUTs', json.loads(strs)['data'].keys())


    #@unittest.skip('Skipped')
    def test_get_data_state_2(self):
        strs=""
        self.ardu.execute('w', 'CS:2')
        self.ardu.execute('r')
        self.ardu.execute('w', 'GD')
        a=self.ardu.execute('r')
        for i in a:
            strs+=i.decode('utf-8')
                
        self.assertNotIn('INs', json.loads(strs)['data'].keys())
        self.assertIn('OUTs', json.loads(strs)['data'].keys())



    #@unittest.skip('Skipped')
    def test_bad_commands(self):
        commands = ['GD ', 'gd', 'CS:0', 'CS:3',
                    ' cs:2', 'OUT:', 'OUT:[1-0,2-0,3-0,4-1 ]',
                    'OUT:[1-0,2-0,3-3,4-1]']
        
        for i in commands:
            strs=""
            self.ardu.execute('w', i)
            a=self.ardu.execute('r')
            for i in a:
                strs+=i.decode('utf-8')
                
            self.assertEqual(json.loads(strs)['err'], 1)

    
    #@unittest.skip('Skipped')
    def test_change_outs(self):
        strs=""
        self.ardu.execute('w', 'CS:2')
        a=self.ardu.execute('r')
        
        self.ardu.execute('w', 'OUT:[1-1,2-1,3-1,4-1]')
        self.ardu.execute('r')

        self.ardu.execute('w', 'GD')
        a=self.ardu.execute('r')
        for i in a:
            strs+=i.decode('utf-8')

        data=json.loads(strs)['data']['OUTs']
        self.assertEqual(data['1']['data'], 1)
        self.assertEqual(data['2']['data'], 1)
        self.assertEqual(data['3']['data'], 1)
        self.assertEqual(data['4']['data'], 1)
    


    
def main() -> None:
    unittest.main()

if __name__ == '__main__':
    main()

