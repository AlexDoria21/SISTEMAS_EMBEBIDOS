int actuadores[10] = {11,12,13};
void setup(){
  Serial.begin(9600);
  for(int i = 0; i < 4; i++){
    pinMode(actuadores[i], OUTPUT);
  }
  Serial.setTimeout(10);
}

int v;
void loop(){
  if(Serial.available()>0){
    v = Serial.readString().toInt();
    digitalWrite(actuadores[v], 1);
    delay(100);
    digitalWrite(actuadores[v], 0);
    delay(100);
  }
}