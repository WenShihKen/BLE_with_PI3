#include <math.h>
#include <DHT.h>
#include <DHT_U.h>
#include <SoftwareSerial.h>

#define RxD 12
#define TxD 13

#define x1 350
#define y1 0
#define x2 3000
#define y2 64

//3C:A3:08:90:68:05
SoftwareSerial BTSerial(13, 12);

//Constants
#define DHTPIN 7     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

//Variables
int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value

double mv2ppm(double delta_mv) {
  double a = (y1 - (((y2 * log(x1)) - (y1 * log(x2))) / (log(x1) - log(x2)))) / log(x1);
  double b = (((y2 * log(x1)) - (y1 * log(x2))) / (log(x1) - log(x2)));
  return exp((delta_mv - b) / a);
}


void setup() {
  BTSerial.flush();
  delay(500);

  BTSerial.begin(9600);
  //BTSerial.println("The controller has successfuly connected to the PC");
  
  Serial.begin(115200);
  dht.begin();
  pinMode(A0, INPUT);
  digitalWrite(A0, HIGH);
}

void loop() {
  uint16_t calVal = 0;
  uint16_t sensorVal = getAverage(A0, 100, 5);

  if (calVal < sensorVal)
    calVal = sensorVal;
  double volt = computeVolts(sensorVal);
  double sensorVolt = (volt / 7.8) * 1000;
  double calVolt = (computeVolts(calVal) / 7.8) * 1000;
  double EMF = calVolt - sensorVolt;
  double ppm = mv2ppm(EMF);
  

  //Read data and store it to variables hum and temp
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  //Print temp and humidity values to serial monitor
  
  Serial.println(analogRead(A0));

  BTSerial.print(temp);
  BTSerial.print(" ");
  BTSerial.print(hum);
  BTSerial.print(" ");
  BTSerial.print(ppm);

  
  

  delay(7000);
}

double computeVolts(int rawADC) {
  return ((rawADC * 4.95) / 1023.0);
}

uint16_t getAverage(byte sensorPin, int avgNum, int del) {
  int i = 0;
  long sum = 0;
  unsigned int value = 0;
  unsigned int result = 0;

  for (i = 0 ; i < avgNum ; i++)
  {
    value = analogRead(sensorPin);
    sum = sum + value;
    delayMicroseconds(del);
  }
  result = sum / avgNum;
  return (result);
}
