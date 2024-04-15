//#include "arduino_layer/arduino_device.h"
#include <Regexp.h>
#include <DHT.h>
#include <DHT_U.h>
#include <stdlib.h>
#include <Arduino.h>
//#include <Arduino.h>
//#include "definitions2.h"

//=================================================================================================

// CONSTANTS
#define DHTTYPE DHT22

const char* FORMAT_STATE_1 = "{\"INs\": {\"1\": {\"dataType\": \"T\", \"data\": %d}, \"2\": {\"dataType\": \"H\", \"data\": %d}, \"3\": {\"dataType\": \"B\", \"data\": %d}}, \"OUTs\": {\"1\": {\"data\": %d}, \"2\": {\"data\": %d}, \"3\": {\"data\": %d}, \"4\": {\"data\": %d}}}";

const char* FORMAT_STATE_2 = "{\"OUTs\": {\"1\": {\"data\": %d}, \"2\": {\"data\": %d}, \"3\": {\"data\": %d}, \"4\": {\"data\": %d}}}";

String ALLOWED_STATES = "12";

//=================================================================================================

// ENUMS
enum DHTTYPES {
    DH11 = DHT11,
    DH22 = DHT22
};

enum IO {
    OUT4=12,
    OUT3=10,
    OUT2=8,
    OUT1=6,
    INDICATOR=13,
    IN1=A0,
    IN2=A1,
    IN3=A4,
    IN4=A5,
};

enum COMMANDID {
  CS,
  GD,
  OUT,
  NOT_COMMAND
};

enum ERRORID{
  NOT_ERROR,
  BAD_COMMAND,
  SENSOR_ERROR,
  INCORRECT_STATE
};

//=================================================================================================


// NAMESPACES
namespace DataUtils {
    bool CheckMatch(char* data, char* regex){
        MatchState ms;
        ms.Target(data);
        return ms.Match(regex) > 0;
    }

    // Not implemented
    void StringToChar(String str, char* &data){
      char dt[40]="";

      for(unsigned int i =0; i <str.length(); i++){
        dt[i] += str.c_str()[i];
      }

      data = dt; 
    }
    
    //{data: $data, err: $err, msg: $msg}
    void PrintData(ERRORID errorId, char* data="null"){
      char data2[400]="";
      char* msg="Ok";

      if(errorId == ERRORID::BAD_COMMAND){
        msg="Command not exist";
      }

      if(errorId == ERRORID::SENSOR_ERROR){
        msg="Temperature Sensor Error : Verify connections";
      }
      if(errorId == ERRORID::INCORRECT_STATE){
        msg="That command not work in this state";
      }

      if(errorId == ERRORID::NOT_ERROR){
        sprintf(data2, "{\"data\":%s,\"err\":%d,\"msg\":\"%s\"};",data, errorId, msg);
      }
      else{
        sprintf(data2, "{\"data\":\"null\",\"err\":%d,\"msg\":\"%s\"};", errorId, msg);
      }
      Serial.print(data2);
    }
}

namespace Middlewares {

    bool CheckChangeStateMiddleware(char* data, String str){
      return DataUtils::CheckMatch(data, "CS:[1-2]") && str.length() == 4;
    }

    bool CheckGetDataMiddleware(char* data, String str){
      return DataUtils::CheckMatch(data, "GD") && str.length() == 2;
    }

    bool CheckOutsMiddleware(char* data, String str){
      return DataUtils::CheckMatch(data, "OUT:%[[1-4]%-[0-1],[1-4]%-[0-1],[1-4]%-[0-1],[1-4]%-[0-1]%]") && str.length() == 21;
    }
}

//=================================================================================================


DHT dht(IN1, DHTTYPE);

// Function for 1 Arg commands
// Function for 2 Arg commands
// Functions to check all formats

class ArduinoDevice {
    private:
        char state;
    public:
        ArduinoDevice();
        void SetupArduino();
        void Loop();
        void Setup(IO inDht=IN1, DHTTYPES dhtType=DH22, int baudRate=9600, int timeOut=10);
        bool SerialMiddleware(char* data, COMMANDID& counter, String str);
        //template <typename... ArgsType>
        int GetData(/*ArgsType... args*/);
        String GetCommand();
        void SetState(char newState);
        void GetArgs(String* firstArg, String* secondArg, String sentence);
        void ChangeOuts(String outStates);
};

void ArduinoDevice::Setup(IO inDht, DHTTYPES dhtType, int baudRate, int timeOut){
  DHT dht_temp(inDht, dhtType);
  dht = dht_temp;
  dht.begin();

  Serial.begin(baudRate);
  Serial.setTimeout(timeOut);
  pinMode(IO::IN1, INPUT);
  pinMode(IO::IN2, INPUT);
  pinMode(IO::IN3, INPUT);
  pinMode(IO::OUT1, OUTPUT);
  pinMode(IO::OUT2, OUTPUT);
  pinMode(IO::OUT3, OUTPUT);
  pinMode(IO::OUT4, OUTPUT);
  pinMode(IO::INDICATOR, OUTPUT);
}

ArduinoDevice::ArduinoDevice(){
  this->state = '1';
}

//template <typename... ArgsType>
int ArduinoDevice::GetData(/*ArgsType... args*/){
    char* data = (char*)malloc(sizeof(char)*400);
    if(this->state == '1'){
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();

        if(!isnan(humidity) && !isnan(temperature)){
          sprintf(data, FORMAT_STATE_1, (int)temperature, (int)humidity, digitalRead(IN3), digitalRead(IO::OUT1), digitalRead(IO::OUT2), digitalRead(IO::OUT3), digitalRead(IO::OUT4));
          DataUtils::PrintData(ERRORID::NOT_ERROR, data);
          //Serial.print(data);
        }
        else{
          DataUtils::PrintData(ERRORID::SENSOR_ERROR);
        }

    }

    if(this->state == '2'){
        sprintf(data, FORMAT_STATE_2, digitalRead(IO::OUT1), digitalRead(IO::OUT2), digitalRead(IO::OUT3), digitalRead(IO::OUT4));
        DataUtils::PrintData(ERRORID::NOT_ERROR, data);
        //Serial.print(data);
    }
    
    free(data);

    return 0;
}

String ArduinoDevice::GetCommand(){
    bool entry = false;
    String data="";
    if(Serial.available() > 0){
        entry=true;
        digitalWrite(IO::INDICATOR, LOW);
        data= Serial.readString();
    }
    if(entry){
        entry = false;
        digitalWrite(IO::INDICATOR, HIGH);
    }
    return data;
}

void ArduinoDevice::SetState(char newState){
    //Verify if new state is valid (not neccesary because regex)
    bool flag=false;
    for (unsigned int i = 0; i < ALLOWED_STATES.length(); i++) {
        if (newState == ALLOWED_STATES[i]){
            flag=true;
            break;
        }
    }
    
    if(!flag) return;

    this->state = newState;
}

void ArduinoDevice::GetArgs(String* firstArg, String* secondArg, String sentence){
  bool second=false;
  for (unsigned int i = 0; i < sentence.length(); i++){
    if(sentence[i]==':'){
      second=true;
      continue;
    }
    
    if(!second)
      *firstArg += sentence[i];
    else
      *secondArg += sentence[i];
  }

}

void ArduinoDevice::ChangeOuts(String outStates){
  String states[4];
  IO outsArray[4] = {OUT1, OUT2, OUT3, OUT4};
  String temp="";
  int counter=0;

  for (unsigned int i = 0; i < outStates.length(); i++) {
    //[1-0, 2-0, 3-0, 4-1]
    if(outStates[i]== ',' || outStates[i]==']'){
      states[counter]=temp;
      temp="";
      counter++;
      continue;
    }

    if(outStates[i]== ' ' || outStates[i]=='[' ){
      continue;
    }

    temp+=outStates[i];
  }
  // i => state_counter
  // x => char_state_counter
  for (unsigned int state_counter = 0; state_counter <= states->length(); state_counter++) {

    bool outValue = false;
    String outIndex="1", outNewState="0";
    for(unsigned int char_state_counter = 0; char_state_counter < states[state_counter].length(); char_state_counter++){

      if(states[state_counter][char_state_counter]=='-'){
        outValue=true;
        continue;
      }
      if(states[state_counter][char_state_counter]==' '){
        continue;
      }
      
      if(!outValue){
        outIndex=states[state_counter][char_state_counter];
      }
      else{
        outNewState=states[state_counter][char_state_counter];
      }
    }
    
    digitalWrite(outsArray[atoi(outIndex.c_str())-1], (outNewState=="0"?0x0:0x1));
  }
  
}




bool ArduinoDevice::SerialMiddleware(char* data, COMMANDID& counter, String str){
  const int middlewareLength = 3;
  bool flag=false;

  //Order of array needs to be same that COMMANDID enum

  bool (*middlewaresFunctions[middlewareLength])(char* data, String str) = {
    Middlewares::CheckChangeStateMiddleware,
    Middlewares::CheckGetDataMiddleware,
    Middlewares::CheckOutsMiddleware
  };

  for (unsigned int i = 0; i < middlewareLength; i++) {
    if(middlewaresFunctions[i](data, str)){
      flag=true;
      counter=(COMMANDID)i;
      break;
    }
  }
  
  if(!flag){
    DataUtils::PrintData(ERRORID::BAD_COMMAND);
  }
  
  return flag;
}

void ArduinoDevice::Loop(){
  
  if(Serial.available() >0){
    delay(1000);
    String command = this->GetCommand();
    COMMANDID commandCounter = COMMANDID::NOT_COMMAND;
    
    // Check if data in is in format
    char commandChar[40]="";

    for(unsigned int i =0; i <command.length(); i++){
      commandChar[i] += command.c_str()[i];
    }

    if(!this->SerialMiddleware(commandChar, commandCounter, command)){
      return;
    }
    
    if(commandCounter == COMMANDID::GD){
      this->GetData();
      return;
    }


    if(commandCounter == COMMANDID::OUT || commandCounter == COMMANDID::CS){
      String fisrtArg = "";
      String secondArg = "";
      this->GetArgs(&fisrtArg, &secondArg, command);

      if(commandCounter==COMMANDID::CS){
        this->SetState(secondArg[0]);
        char dtCS[9]="";
        sprintf(dtCS, "{\"state\":\"%c\"}", this->state);
      
        DataUtils::PrintData(ERRORID::NOT_ERROR, dtCS);
      }

      if(commandCounter==COMMANDID::OUT){
        if(this->state=='2') {
          this->ChangeOuts(secondArg);
          char dtCS[16]="";
          sprintf(dtCS, "{\"OUTs\":\"%d%d%d%d\"}", digitalRead(IO::OUT1), digitalRead(IO::OUT2), digitalRead(IO::OUT3), digitalRead(IO::OUT4));
        
          DataUtils::PrintData(ERRORID::NOT_ERROR, dtCS);
          return;
        }

        DataUtils::PrintData(ERRORID::INCORRECT_STATE);
      }
      return;
    }
  }
}


ArduinoDevice* ad;

// Separate setup to constructor
void setup(){
  ad= new ArduinoDevice();
  ad->Setup();
}

void loop(){
  ad->Loop();
}
