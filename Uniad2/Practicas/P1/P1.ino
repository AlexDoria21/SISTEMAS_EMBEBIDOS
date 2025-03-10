const int pot1 = A0;
const int pot2 = A1;
const int pot3 = A2;
const int pot4 = A3;
const int numLecturas = 30;

int valores[4][numLecturas]; // Almacena los valores de los 4 potenciómetros

// Función para calcular la moda
int calcularModa(int arr[], int n) {
    int maxContador = 0, moda = arr[0];

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

    // Si todos los valores son únicos, retornamos -1 para indicar "No hay moda"
    return (maxContador == 1) ? -1 : moda;
}

// Función para calcular la mediana 
float calcularMediana(int arr[], int n) {
    // Ordenamos los valores usando bubble sort 
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    // Si es par, promediamos los dos del centro; si es impar, tomamos el del medio
    return (n % 2 == 0) ? (arr[n / 2 - 1] + arr[n / 2]) / 2.0 : arr[n / 2];
}

// Función para calcular la media
float calcularMedia(int arr[], int n) {
    int suma = 0;
    for (int i = 0; i < n; i++) {
        suma += arr[i];
    }
    return suma / (float)n;
}

void setup() {
    Serial.begin(115200);
}

void loop() {
    // Capturar 30 valores de cada potenciómetro
    for (int i = 0; i < numLecturas; i++) {
        valores[0][i] = analogRead(pot1);
        valores[1][i] = analogRead(pot2);
        valores[2][i] = analogRead(pot3);
        valores[3][i] = analogRead(pot4);
        delay(50);  // Pequeña pausa entre lecturas
    }

    // Calcular estadísticas y enviar resultados por puerto serie
    for (int i = 0; i < 4; i++) {
        int minVal = valores[i][0];
        int maxVal = valores[i][0];

        for (int j = 1; j < numLecturas; j++) {
            if (valores[i][j] < minVal) minVal = valores[i][j];
            if (valores[i][j] > maxVal) maxVal = valores[i][j];
        }

        float media = calcularMedia(valores[i], numLecturas);
        float mediana = calcularMediana(valores[i], numLecturas);
        int moda = calcularModa(valores[i], numLecturas);

        // Enviar los datos en formato CSV
        Serial.print(i + 1); Serial.print(",");  // Número de potenciómetro
        Serial.print(minVal); Serial.print(",");
        Serial.print(maxVal); Serial.print(",");
        Serial.print(media); Serial.print(",");
        Serial.print(mediana); Serial.print(",");
        Serial.println(moda);
    }

    delay(5000);  // Espera antes de la siguiente medición
}
