// define relay pins
const int wristClose = 9;
const int wristOpen = 8;
const int wristUp = 7;
const int wristDown = 6;
const int shoulderUp = 5;
const int shoulderDown = 4;
const int baseRight = 3; // unused
const int baseLeft = 2;

void setup() {
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
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("Start:")) {
      String color = command.substring(6);
      color.trim();
      start(color);
    }
  }
}

void start(String color) {
  Serial.println("cube detected, starting grab sequence...");

  // lower shoulder to reach the cube
  digitalWrite(shoulderDown, LOW);
  delay(1000);
  digitalWrite(shoulderDown, HIGH);

  // close gripper to pick up cube
  digitalWrite(wristClose, LOW);
  delay(1000);
  digitalWrite(wristClose, HIGH);

  // raise the arm
  digitalWrite(shoulderUp, LOW);
  delay(1000);
  digitalWrite(shoulderUp, HIGH);

  // rotate base left to destination
  int stepsToColor = getRotationSteps(color);
  if (stepsToColor == -1) {
    Serial.println("unknown color. aborting.");
    return;
  }

  rotateBaseLeft(stepsToColor * 1000);

  // lower arm to place the cube
  digitalWrite(shoulderDown, LOW);
  delay(1000);
  digitalWrite(shoulderDown, HIGH);

  // open gripper to release the cube
  digitalWrite(wristOpen, LOW);
  delay(1000);
  digitalWrite(wristOpen, HIGH);

  // raise arm again
  digitalWrite(shoulderUp, LOW);
  delay(1000);
  digitalWrite(shoulderUp, HIGH);

  // rotate base left to return to dock
  int stepsBackToDock = 6 - stepsToColor;
  rotateBaseLeft(stepsBackToDock * 1000);

  Serial.println("cube placed and arm returned to dock.");
}

// returns how many leftward steps to rotate from pickup to color zone
int getRotationSteps(String color) {
  if (color == "Red") return 1;
  else if (color == "Blue") return 2;
  else if (color == "Orange") return 3;
  else if (color == "Yellow") return 4;
  else if (color == "Green") return 5;
  else return -1;
}

// rotate base left for given duration
void rotateBaseLeft(int duration) {
  digitalWrite(baseLeft, LOW);
  delay(duration);
  digitalWrite(baseLeft, HIGH);
}
