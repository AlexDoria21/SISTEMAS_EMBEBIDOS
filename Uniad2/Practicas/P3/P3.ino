#define NUM_POT 4  // Número de potenciómetros
#define NUM_LECTURAS 30  // Cantidad de lecturas por iteración
#define INTERVALO_LECTURA 500  // 500ms entre lecturas

int pinesPotenciometros[NUM_POT] = {A0, A1, A2, A3};  // Pines de los potenciómetros
int valores[NUM_POT][NUM_LECTURAS];  // Matriz para almacenar valores

void setup() {
    Serial.begin(115200);
}

// Ordenar datos para la mediana
void ordenarDatos(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// Calcular la mediana
int calcularMediana(int arr[], int n) {
    ordenarDatos(arr, n);
    return (n % 2 == 0) ? (arr[n / 2 - 1] + arr[n / 2]) / 2 : arr[n / 2];
}

// Calcular la moda
int calcularModa(int arr[], int n) {
    int maxContador = 0;
    int moda = arr[0];

    for (int i = 0; i < n; i++) {
        int contador = 0;
        for (int j = 0; j < n; j++) {
            if (arr[j] == arr[i]) contador++;
        }
        if (contador > maxContador) {
            maxContador = contador;
            moda = arr[i];
        }
    }

    return (maxContador == 1) ? -1 : moda; // Si todos los valores son únicos, no hay moda
}

// Calcular la media
int calcularMedia(int arr[], int n) {
    long suma = 0;
    for (int i = 0; i < n; i++) suma += arr[i];
    return suma / n;
}

void loop() {
    for (int iteracion = 0; iteracion < 20; iteracion++) {  // 20 iteraciones
        for (int i = 0; i < NUM_LECTURAS; i++) {
            for (int j = 0; j < NUM_POT; j++) {
                valores[j][i] = analogRead(pinesPotenciometros[j]);
            }
            delay(INTERVALO_LECTURA);
        }

        for (int j = 0; j < NUM_POT; j++) {
            int minVal = valores[j][0], maxVal = valores[j][0];

            for (int i = 1; i < NUM_LECTURAS; i++) {
                if (valores[j][i] < minVal) minVal = valores[j][i];
                if (valores[j][i] > maxVal) maxVal = valores[j][i];
            }

            int media = calcularMedia(valores[j], NUM_LECTURAS);
            int mediana = calcularMediana(valores[j], NUM_LECTURAS);
            int moda = calcularModa(valores[j], NUM_LECTURAS);

            // Enviar datos en formato CSV
            Serial.print(iteracion + 1); Serial.print(",");
            Serial.print(j + 1); Serial.print(",");  // Número del potenciómetro
            Serial.print(minVal); Serial.print(",");
            Serial.print(maxVal); Serial.print(",");
            Serial.print(media); Serial.print(",");
            Serial.print(mediana); Serial.print(",");
            Serial.println(moda);
        }
    }

    while (true);  // Detener el programa después de 20 iteraciones
}
