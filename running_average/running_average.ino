// initialize input port
int eyebrowPin = A0; // from eyebrow
int cheekPin = A1; // from cheek
//int templePin = A3; // from temple

int eyebrow;
int cheek;
//int temple;

int window = 1000; // window width for running average
int a = 0;
int b = 250;

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
    eyebrow += analogRead(eyebrowPin);
    cheek += analogRead(cheekPin);
  }
  // eyebrow = eyebrow / window;
  // cheek = cheek / window;
  Serial.print(eyebrow);
  Serial.print(" ");
  Serial.print(cheek);
  Serial.println();
}


