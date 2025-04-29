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
  // Listen for call from the image processor
  Serial.begin(9600);

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
  // Listen for updates by our processor
  if(Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if(command == "Start")
    {
      // We're ready to go
      start();
    }
  }

  digitalWrite(wristClose, LOW);  // Relay 1 ON
  delay(1000);
  digitalWrite(wristClose, HIGH); // Stop

  // Close gripper (GND)
  digitalWrite(wristOpen, LOW); // Relay 2 ON
  delay(1000);
  digitalWrite(wristOpen, HIGH); // Stop
}

void start(String color)
{
  //[TODO]: everything
  Serial.println("Cube detected, we should be moving to grab it");
}