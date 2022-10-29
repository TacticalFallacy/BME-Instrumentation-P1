int sensorPin = 0;
int window = 10;
void setup() {
 Serial.begin(9600);
}
void loop() { 
  int data = 0;
  for (int i = 0; i <= window; i++) {
    data += analogRead(sensorPin);
  }
  Serial.println(data/window);
}