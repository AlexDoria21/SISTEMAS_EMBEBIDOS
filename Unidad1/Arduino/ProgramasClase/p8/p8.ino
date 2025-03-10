int sensor = 2;
int actuador = 10;
void setup(){
  Serial.begin(9600);
}
int v;
void loop(){
  v = digitalRead(sensor);
  v = v/4;
  analogWrite(actuador, v);
  delay(100);
}