int servoPin = 3; // servo pin
int relayPin = 4; // relay pin its actually a relay to control the servo motor power
int servoAngle = 90; // servo angle
int servoSpeed = 10; // servo speed
#include <Servo.h>
Servo servo;


// 1c2 lcd setup
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

// LCD setup
void lcdSetup() {
  lcd.init();
  lcd.backlight();
}

// servo setup
void servoSetup() {
  servo.attach(servoPin);
  servo.write(90);
}


void setup() {
  // pinmodes
  pinMode(relayPin, OUTPUT);
  // put your setup code here, to run once:
  run_servo();
  Serial.begin(9600);
  servoSetup();
  servo.write(servoAngle);
  lcdSetup();
  lcd.clear();
  lcd.print("Vision Robot");
  delay(1000);
}

void loop() {
    showcommand("listening");
    if (Serial.available() > 0) { // if there is a command available
        // receiving two part command in one string
        String data = Serial.readStringUntil('.');
        data.trim();
        int commaIndex = data.indexOf(',');
        int startIndex = 0;
        
        while (commaIndex != -1) {
          String cmd = data.substring(startIndex, commaIndex);
          processCommand(cmd.charAt(0)); 
          startIndex = commaIndex + 1;
          commaIndex = data.indexOf(',', startIndex);
        }
        // last command
        String lastCmd = data.substring(startIndex);
        lastCmd.trim();
        if (lastCmd.length() > 0) {
          processCommand(lastCmd.charAt(0));
        }
    }
}

void processCommand(char cmd) {
  if (cmd == 'L') {
    left();
  } else if (cmd == 'R') {
    right();
  } else if (cmd == 'S') {
    reset_servo();
  }
    else {
      showcommand(cmd);
    }
}

void showcommand(String text) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(text);
  lcd.print(" ");
}

void left() {
  // turning the servo to left only 10 degrees
  servoAngle = max(servoAngle - 10, 0);
  servo.write(servoAngle);
  delay(servoSpeed);
}

void reset_servo() {
    servoAngle = 90;
    servo.write(servoAngle);
    delay(servoSpeed);
}

void right() {
  // turning the servo to right only 10 degrees
  servoAngle = min(servoAngle + 10, 180);
  servo.write(servoAngle);
  delay(servoSpeed);
}


void run_servo() {
    digitalWrite(relayPin, HIGH);
}
