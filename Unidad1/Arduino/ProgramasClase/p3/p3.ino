int actuador = 10;
void setup(){
  Serial.begin(9600);
  pinMode(actuador, OUTPUT);
}
int v;
void loop(){
  digitalWrite(actuador, 1);
  delay(1000);
  digitalWrite(actuador,  0);
  delay(1000);
}