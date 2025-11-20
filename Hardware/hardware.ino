#include <Arduino.h>

// ----- MOTOR PINS -----
int ENA = 5; 
int IN1 = 6;
int IN2 = 7;

int ENB = 9;
int IN3 = 10;
int IN4 = 11;

// ----- ULTRASONIC SENSOR -----
int trigPin = 2;
int echoPin = 3;

String command = "";

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;
  return distance;
}

void stopWheelchair() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void moveRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readString();
    command.trim();

    long distance = getDistance();

    if (distance < 30) {
      stopWheelchair();
      return;
    }

    if (command == "FORWARD") moveForward();
    else if (command == "LEFT") moveLeft();
    else if (command == "RIGHT") moveRight();
    else if (command == "STOP") stopWheelchair();
  }
}