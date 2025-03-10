#define POT_PIN A0  // Pin analógico donde está el potenciómetro
#define N 5         // Tamaño del vector (ajustable)

void setup() {
    Serial.begin(9600);  // Inicia comunicación serial
}

void loop() {
    int valores[N];  // Vector para almacenar los datos

    // Leer valores del potenciómetro y almacenarlos en un vector
    for (int i = 0; i < N; i++) {
        valores[i] = analogRead(POT_PIN); // Leer valor del potenciómetro (0-1023)
        delay(100);  // Pequeño retraso
    }

    // Enviar los valores por Serial separados por comas
    for (int i = 0; i < N; i++) {
        Serial.print(valores[i]);
        if (i < N - 1) Serial.print(","); // Separador de datos
    }
    Serial.println();  // Nueva línea para marcar fin de transmisión

    delay(1000);  // Esperar antes de la siguiente lectura
}
