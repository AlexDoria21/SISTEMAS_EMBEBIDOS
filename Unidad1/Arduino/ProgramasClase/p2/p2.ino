int sensor = 2;
void setup(){
  Serial.begin(9600);
  pinMode(sensor,INPUT);
}
int v;
void loop(){
  v = digitalRead(sensor);
  Serial.println(v);
  delay(1000);
}