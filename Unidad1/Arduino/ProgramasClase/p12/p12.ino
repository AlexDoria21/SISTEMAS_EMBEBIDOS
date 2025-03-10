int sensor = 2;
void setup(){
  Serial.begin(9600);
}
int v;
void loop(){
  v = analogRead(sensor);
  Serial.println("valor  ="+ String(v));
  delay(500);
}