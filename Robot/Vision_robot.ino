// the arduino portgram

int servo_pin = 3;
int led = 4;
String last_text;

String data;

//// importing the servo library
#include <Servo.h>
// importing the ic2 lcd library
#include <LiquidCrystal_I2C.h>
// Initialize LCD with I2C address, columns, and rows
LiquidCrystal_I2C lcd(0x27, 16, 2);

Servo servo;

void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(50);
  servo.attach(servo_pin);
  servo.write(90); // 90 degrees (resetting it)
  // initializing the lcd
  lcd.begin(16, 2);
  lcd.print("Hello world!");
  delay(1000);
  lcd.setCursor(0, 1);
  lcd.print("waiting");
  last_text = "waiting";
}

void loop() {

  if (Serial.available()) {

    data = Serial.readStringUntil('\n');

    int separator = data.indexOf('|');
     
    // check if the command is valid
    if (command == "") {
        continue;
    }
    if (separator != -1) {

      String command = data.substring(0, separator);
      String lcdText = data.substring(separator + 1);

      Serial.print("Command: ");
      Serial.println(command);

      Serial.print("LCD: ");
      Serial.println(lcdText);

      // robot control
      if (command == "L") {
        // turn left
        left();
      }
      else if (command == "R") {
        // turn right
        right();
      }
      else if (command == "S") {
        // Reset the robot
        reset();
      }
      else if (command == "C") {
        // recenter the robot
        recenter();
      }
      else if (command == "P") {
        // light on
        light();
      }
      else if (command == "O") {
        // light off
        light_off();
      }

      // lcd control
      lcd_print(lcdText);

    }
  }
}


void lcd_print(String text) {
    if (text != last_text && text != "") {
        last_text = text;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print(text);
    }
}


void right() {
    // turn the servo right for 20 degrees
    // getting the current position
    int current_pos = servo.read();
    servo.write(constrain(current_pos + 20,0,180));
}

void left() {
    // turn the servo left for 20 degrees
    // getting the current position
    int current_pos = servo.read();
    servo.write(constrain(current_pos - 20,0,180));
}

void recenter() {
    int current_pos = servo.read();
    if (current_pos > 93) {
        for (int i = current_pos; i > 90; i--) {
            servo.write(i);
            delay(100);
        }
    }
    else if (current_pos < 87) {
        for (int i = current_pos; i < 90; i++) {
            servo.write(i);
            delay(100);
        }
    }
}

void reset() {
    servo.write(90); // 90 degrees (resetting it)
}

void light() {
    digitalWrite(led, HIGH);
}

void light_off() {
    digitalWrite(led, LOW);
}
