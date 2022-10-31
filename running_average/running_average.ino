// initialize input port
int eyebrowPin = A0; // from eyebrow
int cheekPin = A3; // from cheek
//int templePin = A3; // from temple

int eyebrow;
int eyebrow_min = 10000;
int cheek;
int cheek_min = 10000;
int temp;

int window = 10; // window width for running average

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  eyebrow = 0;
  cheek = 0;
  //temple = 0;
  for (int i = 0; i <= window; i++) {
    analogRead(eyebrowPin);
    delay(10);
    eyebrow += analogRead(eyebrowPin);
    delay(1);
    analogRead(cheekPin);
    delay(10);
    cheek += analogRead(cheekPin);
    delay(1);
  }
//   eyebrow = eyebrow / window;
  if (eyebrow < eyebrow_min) {
    eyebrow_min = eyebrow;
  }
  eyebrow -= eyebrow_min;
//   cheek = cheek / window;
  if (cheek < cheek_min) {
    cheek_min = cheek;
  }
  cheek -= cheek_min;
  Serial.print(eyebrow);
  Serial.print(" ");
  Serial.print(cheek);
  Serial.println();
}


