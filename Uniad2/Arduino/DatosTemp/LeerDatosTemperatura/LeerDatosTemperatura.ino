#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int ciclo = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  if (ciclo >= 24) return;
  
  float temp[30];
  
  for (int i = 0; i < 30; i++) {
    temp[i] = dht.readTemperature();
    delay(500);
  }
  
  ordenarArray(temp, 30);
  float medianaTemp = (temp[14] + temp[15]) / 2.0;
  
  Serial.println(medianaTemp);  // Solo envía temperatura
  ciclo++;
}

void ordenarArray(float *array, int n) {
  for (int i = 0; i < n-1; i++) {
    for (int j = 0; j < n-i-1; j++) {
      if (array[j] > array[j+1]) {
        float temp = array[j];
        array[j] = array[j+1];
        array[j+1] = temp;
      }
    }
  }
}