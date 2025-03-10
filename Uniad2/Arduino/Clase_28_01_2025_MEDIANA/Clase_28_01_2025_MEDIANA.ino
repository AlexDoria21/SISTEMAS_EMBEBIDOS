// Procesamiento de datos
// Normalmente leemos únicamente una vez el valor de un sensor y mandamos
// la información al puerto serial.
// Esto puede generar inconsistencias en las lecturas, por lo que se busca
// minimizar este problema mediante el preprocesamiento.

// Primera aproximación: cálculo de la mediana.

int sensor = A0;           // Pin analógico para el sensor
const int totLecturas = 30; // Total de lecturas (teorema del límite central)
int valor[totLecturas];    // Arreglo para almacenar las lecturas

void setup() {
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  // Leer valores del sensor y almacenarlos en el vector
  for (int i = 0; i < totLecturas; i++) {
    valor[i] = analogRead(sensor);
    delayMicroseconds(100);  // Pequeña espera entre lecturas
  }

  // Ordenar el arreglo de menor a mayor (ordenamiento burbuja mejorado)
  for (int i = 0; i < totLecturas - 1; i++) {
    for (int j = i + 1; j < totLecturas; j++) {
      if (valor[j] < valor[i]) {
        int temp = valor[i];
        valor[i] = valor[j];
        valor[j] = temp;
      }
    }
  }

  // Calcular y enviar la mediana al monitor serial
  int mediana = valor[totLecturas / 2];  // Valor central del arreglo ordenado
  Serial.println(mediana);

  delay(10);  // Breve pausa antes de la siguiente iteración
}
