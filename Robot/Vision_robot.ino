
int echo = 12;
int trig = 11 ;

int m1p1 = 3;
int m1p2 = 5;
int m2p1 = 6;
int m2p2 = 9;
int CL = 4;
int motor_speed;
int scan_speed;
int dist;


// geting distance
int getDistance() {
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    
    long duration = pulseIn(echo, HIGH);
    int distance = duration * 0.034 / 2;
    
    if (distance == 0) distance = 100;
    if (distance > 100) distance = 100;
    
    return distance;
}


void setup() { // adruino setup
    motor_speed = 160;
    scan_speed = 150;
    Serial.begin(9600);
    // pinmodes
    pinMode(echo, INPUT);
    pinMode(trig, OUTPUT);
    pinMode(m1p1, OUTPUT);
    pinMode(m1p2, OUTPUT);
    pinMode(m2p1, OUTPUT);
    pinMode(m2p2, OUTPUT);
    pinMode(CL, OUTPUT);
    stop(); // sttopign robot
    delay(500);
    Serial.println("READY");   
}



void loop() {
    dist = getDistance();
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        while (Serial.available()) Serial.read();
  
        switch (cmd) {
            case 'F': forward(); break;
            case 'B': backward(); break;
            case 'R': turnRight(); break;
            case 'L': turnLeft(); break;
            case 'S': stop(); break;
            case 'E': scanRight(); break;   
            case 'W': scanLeft(); break;    
            case 'N': lightOn(); break;     
            case 'M': lightOff(); break;    
        }
    }
}

void forward() {
    if (dist < 20) { //stop
        return;
    }
    else {
      analogWrite(m1p1, motor_speed);
      analogWrite(m1p2, 0);
      analogWrite(m2p1, motor_speed);
      analogWrite(m2p2, 0);
    } 
}

void backward() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, motor_speed);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, motor_speed);
}

void stop() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void turnRight() {
    analogWrite(m1p1, motor_speed);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, scan_speed);
}

void turnLeft() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, scan_speed);
    analogWrite(m2p1, motor_speed);
    analogWrite(m2p2, 0);
}

void scanLeft() {
    analogWrite(m1p1, 0);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, scan_speed);
    analogWrite(m2p2, 0);
}

void scanRight() {
    analogWrite(m1p1, scan_speed);
    analogWrite(m1p2, 0);
    analogWrite(m2p1, 0);
    analogWrite(m2p2, 0);
}

void lightOn() {
    digitalWrite(CL, HIGH);
}

void lightOff() {
    digitalWrite(CL, LOW);
}
