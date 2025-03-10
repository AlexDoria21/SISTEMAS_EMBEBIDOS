int actuadores[10] = {11,12,13};
void setup(){
  Serial.begin(9600);
  for(int i = 0; i < 4; i++){
    pinMode(actuadores[i], OUTPUT);
   }
}
int v;
void loop(){
  for(int i = 0; i < 4; i++){
    digitalWrite(actuadores[i],1);
    delay(100);
    digitalWrite(actuadores[i], 0);
    delay(100);
   }
  delay(100);
}