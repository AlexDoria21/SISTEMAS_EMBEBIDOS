int sensor = 2;

void setup(){
  Serial.begin(9600);
}
int v;
void loop(){
  v = analogRead(sensor);
  Serial.println(v);
  delay(1000);
}