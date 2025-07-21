#include <Arduino.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Ticker.h>
#include <ESP32Servo.h>
#include "DHT.h"

#define BUZZER       16 
#define LIGHT        17   
#define MQ2          35   
#define PIR          33   
#define BUTTON       27   
#define SERVO        32    
#define DHT_PIN      14   
#define DHT_TYPE     DHT11  

const char ssid[] = "Smarthome";
const char pass[] = "12345678";

#define API_KEY "AIzaSyBDmMJ64Fzm2BWN2hcZDDcF9CTbDCUNG5I"
#define DATABASE_URL "final-project-439bc-default-rtdb.asia-southeast1.firebasedatabase.app"
#define DATABASE_SECRET "06T7o5RqAnJiOPEvUIsyGc7QXo9NNBUjZkH7uddZ"
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

DHT dht(DHT_PIN, DHT_TYPE);
Servo servo;
Ticker blinker;

int gasLevel;
float temperature, humidity;
int doorState = 0, previousDoorState = 0;
int lightState = 0, previousLightState = 0;
int autoLightControl = 0;
unsigned long timeout;

void blink();
void tick(int times = 1, int delayTime = 100);
void initializePins();

void blink() {
    digitalWrite(BUZZER, !digitalRead(BUZZER));
}

void tick(int times, int delayTime) {
    while (times--) {
        digitalWrite(BUZZER, HIGH);
        delay(delayTime);
        digitalWrite(BUZZER, LOW);
        delay(delayTime);
    }
}

void initializePins() {
    pinMode(BUZZER, OUTPUT);
    tick(1, 60);

    pinMode(LIGHT, OUTPUT);
    digitalWrite(LIGHT, LOW);

    pinMode(PIR, INPUT_PULLUP);
    pinMode(BUTTON, INPUT);

    dht.begin();
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    ESP32PWM::allocateTimer(3);
    
    servo.setPeriodHertz(50);
    servo.attach(SERVO, 500, 2400);
    servo.write(40);

    WiFi.begin(ssid, pass);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(300);
    }
    Serial.println();
    Serial.print("Connected with IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);
    config.database_url = DATABASE_URL;
    // config.signer.test_mode = true;
    config.signer.tokens.legacy_token = DATABASE_SECRET;
    Firebase.begin(&config, &auth);
    Firebase.reconnectWiFi(true);
    Firebase.setDoubleDigits(5);

    tick(3, 90);
}

void setup() {
    Serial.begin(9600);
    initializePins();
}

void loop() {
    gasLevel = map(analogRead(MQ2), 0, 4095, 0, 99);
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();

    Serial.print(digitalRead(PIR));
    Serial.print("\t");
    Serial.print(gasLevel);
    Serial.print("\t");
    Serial.print(temperature);
    Serial.print("\t");
    Serial.print(humidity);
    Serial.print("\t\n");

    if (Firebase.ready() && millis() - timeout > 1000) {
        Firebase.setFloat(fbdo, "/Sensor/Temperature", temperature);
        Firebase.setFloat(fbdo, "/Sensor/Humidity", humidity);
        Firebase.setInt(fbdo, "/Sensor/Gas", gasLevel);

        if (Firebase.getString(fbdo, "Door")) {
            String response = fbdo.to<String>();
            response.replace("\\\"", "");
            int doorCommand = response.toInt();
            if (doorCommand == -1) {
                blinker.attach(0.1, blink);
            } else {
                blinker.detach();
                digitalWrite(BUZZER, LOW);
                doorState = doorCommand;
            }
        }

        if (Firebase.getString(fbdo, "Light")) {
            String lightResponse = fbdo.to<String>();
            lightResponse.replace("\\\"", "");
            int lightCommand = lightResponse.toInt();
            Serial.println("Light State: " + String(lightCommand));
            if (lightCommand == -1) {
                autoLightControl = 1;
            } else {
                autoLightControl = 0;
                lightState = lightCommand;
            }
        }

        timeout = millis();
    }

    if (digitalRead(BUTTON) == LOW) {
        delay(10); 
        if (digitalRead(BUTTON) == LOW) {
            tick();
            while (digitalRead(BUTTON) == LOW) delay(10);
            doorState = 1 - doorState;
            Firebase.setString(fbdo, "Door", String(doorState));
        }
    }

    if (autoLightControl == 1) { 
        if (digitalRead(PIR) == HIGH && digitalRead(LIGHT) == LOW) { 
            digitalWrite(LIGHT, HIGH);
        }
        if (digitalRead(PIR) == LOW && digitalRead(LIGHT) == HIGH) { 
            digitalWrite(LIGHT, LOW);
        }
    }

    if (doorState != previousDoorState) {
        tick(1, 60);
        if (doorState == 1) {
            servo.write(120); 
        } else {
            servo.write(40); 
        }
        previousDoorState = doorState;
    }

    if (lightState != previousLightState) { 
        tick(1, 60);
        if (lightState == 1) {
            digitalWrite(LIGHT, HIGH);
        } else {
            digitalWrite(LIGHT, LOW);
        }
        previousLightState = lightState;
    }

    delay(100);
}
