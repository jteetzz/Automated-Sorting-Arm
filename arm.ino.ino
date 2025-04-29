// Define relay pins
const int wristClose = 9;
const int wristOpen = 8;
const int wristUp= 7;
const int wristDown= 6;
const int shoulderUp= 5;
const int shoulderDown= 4;
const int baseRight = 3;
const int baseLeft = 2;

void setup() {
  pinMode(wristClose, OUTPUT);
  pinMode(wristOpen, OUTPUT);
  pinMode(wristUp, OUTPUT);
  pinMode(wristDown, OUTPUT);
  pinMode(shoulderUp, OUTPUT);
  pinMode(shoulderDown, OUTPUT);
  pinMode(baseRight, OUTPUT);
  pinMode(baseLeft, OUTPUT);


}

void loop() {
  digitalWrite(wristClose, LOW);  // Relay 1 ON
  delay(1000);
  digitalWrite(wristClose, HIGH); // Stop

  // Close gripper (GND)
  digitalWrite(wristOpen, LOW); // Relay 2 ON
  delay(1000);
  digitalWrite(wristOpen, HIGH); // Stop

}