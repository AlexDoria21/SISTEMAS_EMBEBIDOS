//Procsamiento de datos
//
//Normalmente leeos unicamente una v dasa sensor y mandamos
//la informacion al puerto serial
//
//Esto es incorrecro debeido  que podrian generarse inosistencias en las lecturas, por lo que  debe bsucarse
//tratar de aminorar esta situacion mediante el preprocesamiento..

//primera aproximacion.... medidas de tedencia central
//


int sensor = A0;
void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
}
//PROMEDIO MEDIA
int totLecturas = 30;//Es el teorema del limite central por eso es 30, se usa cuando no 
int valor[30]; //Vector
void loop() {
  // put your main code here, to run repeatedly:
    for(int i = 0; i<totLecturas; i++){
      valor[i] = analogRead(sensor);
      delayMicroseconds(100);
    }
  
  
  int prom = 0;
  for(int i = 0; i<totLecturas;i++){
    prom += valor[i];
  } 
  prom /= totLecturas;


  Serial.println(prom);

  delay(10);
}
