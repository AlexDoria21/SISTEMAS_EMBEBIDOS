int sensores[] = {A0, A1, A2,A4};
int actuadores[ ] = {10, 11, 12, 13};
int i;
void setup() {
  // put your setup code here, to run once:
    for  (i = 0; i<4; i++){}
      pinMode(actuadores[i], OUTPUT);
}

int valor;
void loop() {
  // put your main code here, to run repeatedly:
      for (i = 0; i<4; i++){
      valor = analogRead(sensores[i]);

    ///
      valor = valor/512;


      digitalWrite(sensores[i], valor);


  }

}
