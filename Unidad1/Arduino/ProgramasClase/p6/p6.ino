long v;
void setup(){
  Serial.begin(9600);
}
void loop(){
  v = millis();
  Serial.println(v);
  delay(1000);
}