// Normalmente leemos únicamente una vez el valor de un sensor y mandamos
// la información al puerto serial.
//
// Esto puede generar inconsistencias en las lecturas, por lo que se busca
// minimizar este problema mediante el preprocesamiento.

// Primera aproximación: medidas de tendencia central.

int sensor = A1;

// Definimos constantes y variables globales.
int totLecturas = 30;  // Total de lecturas (teorema del límite central).
int valor[30];         // Vector para almacenar las lecturas.
int valormenor = 1024; // Inicializamos con el valor máximo de la lectura.

void setup() {
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios.
}

void loop() {
  // Leer valores del sensor y almacenarlos en el vector.
  for (int i = 0; i < totLecturas; i++) {
    valor[i] = analogRead(sensor);
    delayMicroseconds(100);  // Pequeña espera entre lecturas.
  }

  // Reiniciar valormenor a su valor inicial.
  valormenor = 1024;

  // Buscar el valor menor en el vector.
  for (int i = 0; i < totLecturas; i++) {
    if (valor[i] < valormenor) {
      valormenor = valor[i];
    }
  }

  // Enviar el valor menor al puerto serial.
  Serial.println(valormenor);

  delay(10);  // Breve pausa antes de la siguiente iteración.
}
