// Procesamiento de datos
// Leemos múltiples valores de un sensor analógico y determinamos el valor máximo
// para minimizar inconsistencias en las lecturas.

int sensor = A0;           // Pin analógico para el sensor
const int totLecturas = 30; // Total de lecturas (teorema del límite central)

void setup() {
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  int valormayor = 0;  // Inicializamos al valor más bajo posible (0 para analogRead)

  // Leer valores del sensor y determinar el máximo
  for (int i = 0; i < totLecturas; i++) {
    int lectura = analogRead(sensor);
    if (lectura > valormayor) {
      valormayor = lectura;
    }
    delayMicroseconds(100);  // Pequeña espera entre lecturas
  }

  // Enviar el valor máximo al monitor serial
  Serial.println(valormayor);

  delay(10);  // Breve pausa antes de la siguiente iteración
}
