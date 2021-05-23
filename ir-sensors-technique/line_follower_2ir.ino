#define motorAspeed 5//Enable1 L298 Pin motorAspeed 
#define motorA1 6 // Right motor forward
#define motorA2 7 // Right motor backward
#define motorB1 8 // Left motor backward 
#define motorB2 9 // Left motor backward
#define motorBspeed 10 //Enable2 L298 Pin motorBspeed 

#define rightSensor A0 //ir sensor Right
#define leftSensor A1 //ir sensor Left
#define middleSensor A2 //ir sensor Left
 
int turnDelay = 100;

void setup(){ // put your setup code here, to run once

  pinMode(rightSensor, INPUT); // declare if sensor as input  
  pinMode(leftSensor, INPUT); // declare ir sensor as input
  
  pinMode(motorAspeed, OUTPUT); // declare as output for L298 Pin motorAspeed 
  pinMode(motorA1, OUTPUT); // declare as output for L298 Pin motorA1 
  pinMode(motorA2, OUTPUT); // declare as output for L298 Pin motorA2 
  pinMode(motorB1, OUTPUT); // declare as output for L298 Pin motorB1   
  pinMode(motorB2, OUTPUT); // declare as output for L298 Pin motorB2 
  pinMode(motorBspeed, OUTPUT); // declare as output for L298 Pin motorBspeed 
  
  analogWrite(motorAspeed, 150); // Write The Duty Cycle 0 to 255 Enable Pin A for Motor1 Speed 
  analogWrite(motorBspeed, 150); // Write The Duty Cycle 0 to 255 Enable Pin B for Motor2 Speed 
  delay(1000);
}
void loop(){   
  if((digitalRead(rightSensor) == LOW) && (digitalRead(leftSensor) == LOW)){forward();}   //if Right Sensor and Left Sensor are at White color then it will call forward function
  
  else if((digitalRead(rightSensor) == HIGH) && (digitalRead(leftSensor) == LOW)){turnRight();} //if Right Sensor is Black and Left Sensor is White then it will call turn Right function  
  
  else if((digitalRead(rightSensor) == LOW) && (digitalRead(leftSensor) == HIGH)){turnLeft();}  //if Right Sensor is White and Left Sensor is Black then it will call turn Left function
  
  else if((digitalRead(rightSensor) == HIGH) && (digitalRead(leftSensor) == HIGH)){Stop();} //if Right Sensor and Left Sensor are at Black color then it will call Stop function
}

void forward(){  //forward
  digitalWrite(motorA1, HIGH); //Right Motor forward Pin 
  digitalWrite(motorA2, LOW);  //Right Motor backward Pin 
  digitalWrite(motorB1, HIGH);  //Left Motor backward Pin 
  digitalWrite(motorB2, LOW); //Left Motor forward Pin 

  analogWrite(motorAspeed, 150);
  analogWrite(motorBspeed, 150);
}

void turnRight(){ //turnRight
  digitalWrite(motorA1, HIGH); //Right Motor forward Pin 
  digitalWrite(motorA2, LOW);  //Right Motor backward Pin 
  digitalWrite(motorB1, LOW); //Left Motor backward Pin 
  digitalWrite(motorB2, HIGH);  //Left Motor forward Pin

  analogWrite(motorAspeed, 100);
  analogWrite(motorBspeed, 150);
  delay(turnDelay);
}

void turnLeft(){ //turnLeft
  digitalWrite(motorA1, LOW);  //Right Motor forward Pin 
  digitalWrite(motorA2, HIGH); //Right Motor backward Pin  
  digitalWrite(motorB1, HIGH);  //Left Motor backward Pin 
  digitalWrite(motorB2, LOW); //Left Motor forward Pin  

  analogWrite(motorAspeed, 150);
  analogWrite(motorBspeed, 100);
  delay(turnDelay);
}

void Stop(){ //stop
  digitalWrite(motorA1, LOW); //Right Motor forward Pin 
  digitalWrite(motorA2, LOW); //Right Motor backward Pin 
  digitalWrite(motorB1, LOW); //Left Motor backward Pin 
  digitalWrite(motorB2, LOW); //Left Motor forward Pin

  analogWrite(motorAspeed, 0);
  analogWrite(motorBspeed, 0);
  
}
