#include <DHT.h>
#include <Array.h>

#define DHTPIN 2          // Pin digital para el DHT11
#define DHTTYPE DHT11
#define MUESTRAS 5        // Número de lecturas para la mediana
#define INTERVALO 2000    // Intervalo entre lecturas

DHT dht(DHTPIN, DHTTYPE);
Array<float> temperaturas;
int iteracion = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();
  temperaturas.reserve(MUESTRAS);
}

float leerTemperatura() {
  float t = dht.readTemperature();  // Leer solo temperatura
  if (isnan(t)) {
    return -999.9;  // Valor especial para error
  }
  return t;
}

void procesarDatos() {
  temperaturas.clear();
  
  // Tomar múltiples lecturas
  for(int i=0; i<MUESTRAS; i++){
    float temp = leerTemperatura();
    if(temp != -999.9) {
      temperaturas.push_back(temp);
    }
    delay(250);
  }
  
  // Calcular mediana
  if(temperaturas.size() > 0){
    temperaturas.sort();
    float mediana = temperaturas[temperaturas.size()/2];
    Serial.println(mediana, 1);  // 1 decimal
  } else {
    Serial.println("ERROR");     // En caso de fallos
  }
}

void loop() {
  if(millis() - iteracion >= INTERVALO){
    procesarDatos();
    iteracion = millis();
  }
  
  // Control LED desde Python
  if(Serial.available() > 0){
    char c = Serial.read();
    digitalWrite(13, c == 'L' ? HIGH : LOW);
  }
}