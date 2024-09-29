#include <Servo.h>

Servo servo1; // Create a servo object for the first servo
Servo servo2; // Create a servo object for the second servo
Servo servo3; // Create a servo object for the third servo
Servo servo4; // Create a servo object for the fourth servo

int servoPin1 = 9;  // Pin where the first servo is connected
int servoPin2 = 10; // Pin where the second servo is connected
int servoPin3 = 11; // Pin where the third servo is connected
int servoPin4 = 12; // Pin where the fourth servo is connected

char blinkSignal;
int currentPos = 0; // Variable to store the current position of all servos

void setup()
{
  Serial.begin(9600); // Start serial communication at 9600 baud

  // Attach the servos to the specified pins
  servo1.attach(servoPin1);
  servo2.attach(servoPin2);
  servo3.attach(servoPin3);
  servo4.attach(servoPin4);

  // Initialize all servos at 0 degrees
  servo1.write(currentPos);
  servo2.write(currentPos);
  servo3.write(currentPos);
  servo4.write(currentPos);
}

void loop()
{
  if (Serial.available() > 0)
  {
    blinkSignal = Serial.read(); // Read the incoming byte from the serial port

    if (blinkSignal == 'B')
    { // Check if the signal indicates a blink
      if (currentPos == 0)
      {
        // Move all servos to 180 degrees
        servo1.write(180);
        servo2.write(180);
        servo3.write(180);
        servo4.write(180);
        currentPos = 180; // Update the current position
      }
      else if (currentPos == 180)
      {
        // Move all servos to 0 degrees
        servo1.write(0);
        servo2.write(0);
        servo3.write(0);
        servo4.write(0);
        currentPos = 0; // Update the current position
      }
      delay(500); // Small delay to allow the servos to reach the position before next blink
    }
  }
}
