#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
unsigned long intervaloMuestra = 120000; // 2 minutos
unsigned long intervaloHora = 3600000;   // 1 hora
float muestras[30];
int indiceMuestra = 0;
unsigned long marcaTiempoHora = 0;
unsigned long marcaTiempoMuestra = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  marcaTiempoHora = millis();
}

void loop() {
  if (millis() - marcaTiempoHora <= intervaloHora) {
    if (indiceMuestra < 30 && (millis() - marcaTiempoMuestra) >= intervaloMuestra) {
      float temperatura = dht.readTemperature();
      if (!isnan(temperatura)) {
        muestras[indiceMuestra] = temperatura;
        indiceMuestra++;
        marcaTiempoMuestra = millis();
      }
    }
  } else {
    // Ordenar para mediana
    for (int i = 0; i < 29; i++) {
      for (int j = 0; j < 29 - i; j++) {
        if (muestras[j] > muestras[j + 1]) {
          float temp = muestras[j];
          muestras[j] = muestras[j + 1];
          muestras[j + 1] = temp;
        }
      }
    }
    float mediana = (muestras[14] + muestras[15]) / 2.0;
    
    Serial.print((millis() / intervaloHora) % 24);
    Serial.print(",");
    Serial.println(mediana, 1);
    
    indiceMuestra = 0;
    marcaTiempoHora = millis();
  }
}