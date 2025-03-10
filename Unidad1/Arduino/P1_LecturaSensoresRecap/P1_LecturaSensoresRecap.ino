// Usar minúsculas para consistencia en nombres de variables
int pots[4] = {A0, A1, A2, A3};
int vals[4];  // Corregir mayúscula inconsistente

void setup() {
  Serial.begin(9600);        
  Serial.setTimeout(100);    
}

void loop() {                // void faltante y minúscula
  for(int i = 0; i < 4; i++) { // Variable 'i' faltante y espacios
    vals[i] = analogRead(pots[i]);
    delayMicroseconds(1000);  // 1 ms de espera entre lecturas
  }

  String c;
  // Formatear cadena con valores (notar 'F' final mayúscula)
  c = "i" + String(vals[0]) + "-" + String(vals[1]) 
      + "-" + String(vals[2]) + "-" + String(vals[3]) + "F";
  
  Serial.println(c);    
  
  delay(10);  // Retardo base de 10 ms
}