int actuador = 10;
void setup(){
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(actuador, OUTPUT);
}

int v;
void loop(){
  if(Serial.available()>0){
    v = Serial.readString().toInt();
    digitalWrite(actuador, v);
  }
  delay(100);
}