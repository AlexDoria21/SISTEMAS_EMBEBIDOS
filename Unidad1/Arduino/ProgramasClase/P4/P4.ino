int actuador = 10;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(actuador, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(actuador,1);
  delay(250);
  digitalWrite(actuador,0);
  delay(250);
}