// Procesamiento de datos - Cálculo de MODA
// Se utilizan 4 potenciómetros para registrar métricas.
// Normalmente, se lee una única vez el valor del sensor, pero aquí hacemos un preprocesamiento
// para calcular la moda de cada potenciómetro.

// Pines analógicos para los potenciómetros
int pot1 = A0;
int pot2 = A1;
int pot3 = A2;
int pot4 = A3;

// Configuración de lecturas
int totLecturas = 30;       // Total de lecturas (teorema del límite central)
int lecturas1[30];          // Vector para almacenar las lecturas del potenciómetro 1
int lecturas2[30];          // Vector para almacenar las lecturas del potenciómetro 2
int lecturas3[30];          // Vector para almacenar las lecturas del potenciómetro 3
int lecturas4[30];          // Vector para almacenar las lecturas del potenciómetro 4

void setup() {
  Serial.begin(9600);       // Inicializar comunicación serial
}

// Función para capturar lecturas del potenciómetro
void capturarLecturas(int pin, int *lecturas) {
  for (int i = 0; i < totLecturas; i++) {
    lecturas[i] = analogRead(pin);
    delayMicroseconds(100); // Pausa breve entre lecturas
  }
}

// Función para calcular la moda de un vector de lecturas
int calcularModa(int *lecturas) {
  int frecuencia[1024] = {0};  // Array para contar las frecuencias (valores de 0 a 1023)
  int moda = 0, maxFrecuencia = 0;

  // Contar frecuencias
  for (int i = 0; i < totLecturas; i++) {
    frecuencia[lecturas[i]]++;
  }

  // Encontrar el valor con la mayor frecuencia
  for (int i = 0; i < 1024; i++) {
    if (frecuencia[i] > maxFrecuencia) {
      maxFrecuencia = frecuencia[i];
      moda = i;
    }
  }

  return moda;
}

void loop() {
  // Capturar lecturas de los potenciómetros
  capturarLecturas(pot1, lecturas1);
  capturarLecturas(pot2, lecturas2);
  capturarLecturas(pot3, lecturas3);
  capturarLecturas(pot4, lecturas4);

  // Calcular las modas
  int moda1 = calcularModa(lecturas1);
  int moda2 = calcularModa(lecturas2);
  int moda3 = calcularModa(lecturas3);
  int moda4 = calcularModa(lecturas4);

  // Enviar los resultados al puerto serial
  Serial.print(moda1);
  Serial.print(",");
  Serial.print(moda2);
  Serial.print(",");
  Serial.print(moda3);
  Serial.print(",");
  Serial.println(moda4); // Usar println para indicar el fin de la línea

  delay(1000); // Esperar un segundo antes de la siguiente iteración
}
