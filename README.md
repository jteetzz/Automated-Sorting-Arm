# Automated Sorting Arm
This is the code repository for our 497 Project - Automated Sorted Arm.

The code was my (Murads) responsibility for this project.

## Image_Processor.py
This script determines the color and shape of an object through use of a webcam. For the purposes of this project however, the detectable shape was limited to only squares (cubes). 

*Sending the data to the **Arduino**:*
```python
# Send the color name to Arduino
msg = f"start:{color_name}\n"
arduino.write(msg.encode())
```
## Arm.ino
This is the Arduino script which controls the robotic arm. 

The script awaits for a signal from our **Image_Processor.py** script and performs movements onto the robotic arm depending on **1. if a square object is detected** and **2. the color of that object**.

Depending on the **color** of the cube, the arm will **rotate** a specific amount of units corresponding to its bin:

```
// returns how many leftward steps to rotate from pickup to color zone
int getRotationSteps(String color) {
  if (color == "Red") return 1;
  else if (color == "Blue") return 2;
  else if (color == "Orange") return 3;
  else if (color == "Yellow") return 4;
  else if (color == "Green") return 5;
  else return -1;
}
```

```
...

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
  
...
  ```

After the rotation, the arm is prompted to drop the cube, and rotate back to its default **docker** destination:

```
...

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

...
```

### How to use
1. Start the **Image_Processor**: `python3 Image_Processor.py`

 2. Start `arm.ino` in **Arduino IDE**.
(Note: Ensure correct connections given source code.)

 3. Ensure the bot is facing the **docker** station by default without any rotations, and that its **destination spots** are setup along the arms rotation trajectory.

 4. Ensure that the camera connected to the device is on and is facing the **docker** station.

 5. Place a cube on the **docker** station, and sit back and watch the robotic arm take care of the rest!



