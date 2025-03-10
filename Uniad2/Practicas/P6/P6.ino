#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define LED_PIN 13

DHT dht(DHTPIN, DHTTYPE);
unsigned long intervaloMuestra = 120000; // 2 minutos
unsigned long intervaloHora = 3600000;   // 1 hora
float muestras[30];
int indiceMuestra = 0;
unsigned long marcaTiempoHora = millis();
unsigned long marcaTiempoMuestra = marcaTiempoHora;
bool estadoAC = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
}

void loop() {
  // Recepción de comandos desde Python
  if(Serial.available() > 0){
    char comando = Serial.read();
    estadoAC = (comando == 'L');
    digitalWrite(LED_PIN, estadoAC);
  }

  // Toma de muestras cada 2 minutos
  if((millis() - marcaTiempoMuestra) >= intervaloMuestra && indiceMuestra < 30){
    float temp = dht.readTemperature();
    if(!isnan(temp)){
      muestras[indiceMuestra++] = temp;
    }
    marcaTiempoMuestra = millis();
  }

  // Procesamiento horario
  if((millis() - marcaTiempoHora) >= intervaloHora){
    // Calcular mediana
    float tempOrdenadas[30];
    memcpy(tempOrdenadas, muestras, sizeof(muestras));
    ordenarBurbuja(tempOrdenadas, 30);
    
    float mediana = (tempOrdenadas[14] + tempOrdenadas[15]) / 2.0;
    
    // Enviar dato a Python
    Serial.println(mediana, 1);
    
    // Reiniciar variables
    indiceMuestra = 0;
    marcaTiempoHora = millis();
  }
}

void ordenarBurbuja(float* arr, int n) {
  for(int i=0; i<n-1; i++){
    for(int j=0; j<n-i-1; j++){
      if(arr[j] > arr[j+1]){
        float temp = arr[j];
        arr[j] = arr[j+1];
        arr[j+1] = temp;
      }
    }
  }
}