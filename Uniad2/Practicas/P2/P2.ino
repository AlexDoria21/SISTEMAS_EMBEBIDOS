#include <DHT.h>

#define DHTPIN 2      // Pin donde está conectado el DHT11
#define DHTTYPE DHT11 // Tipo de sensor
#define NUM_LECTURAS 30 // Número de lecturas en 1 hora
#define INTERVALO_LECTURA 120000 // 2 minutos entre lecturas (120,000 ms)

DHT dht(DHTPIN, DHTTYPE);
float temperaturas[NUM_LECTURAS];

void setup() {
    Serial.begin(115200);
    dht.begin();
}

void ordenarDatos(float arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                float temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

float calcularMediana(float arr[], int n) {
    ordenarDatos(arr, n);
    if (n % 2 == 0) {
        return (arr[n / 2 - 1] + arr[n / 2]) / 2.0;
    } else {
        return arr[n / 2];
    }
}

void loop() {
    for (int h = 0; h < 12; h++) { // 12 horas
        for (int i = 0; i < NUM_LECTURAS; i++) {
            temperaturas[i] = dht.readTemperature();
            delay(INTERVALO_LECTURA);
        }

        float mediana = calcularMediana(temperaturas, NUM_LECTURAS);

        // Enviar la mediana por el puerto serie
        Serial.print("Hora ");
        Serial.print(h + 1);
        Serial.print(": ");
        Serial.println(mediana);

        delay(1000);  // Pequeña pausa antes de continuar con la siguiente hora
    }

    while (true); // Detiene el programa después de 12 horas
}
