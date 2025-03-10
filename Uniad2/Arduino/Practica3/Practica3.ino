const int potPins[] = {A0, A1, A2, A3};  // Pines analógicos
const int numPots = 4;                   // Número de potenciómetros
unsigned long lastSend = 0;              // Control de tiempo

void setup() {
  Serial.begin(115200);                  
  while (!Serial);                       
  Serial.println("ARDUINO_INICIADO");    
}

void loop() {
  if (millis() - lastSend >= 50) {       
    leerYEnviarPotenciometros();  // Nombre de función sin acento
    lastSend = millis();
  }
}

// Nombre de función corregido
void leerYEnviarPotenciometros() {
  static String datos;
  datos.reserve(30);                     
  
  for (int i = 0; i < numPots; i++) {
    int valor = 0;
    for (int j = 0; j < 5; j++) {
      valor += analogRead(potPins[i]);
    }
    valor /= 5;
    
    datos += String(valor);
    if (i < numPots - 1) datos += ",";    
  }
  datos += "\n";                          
  
  Serial.print(datos);
  datos = "";                             
}