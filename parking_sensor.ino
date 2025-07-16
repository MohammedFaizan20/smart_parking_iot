#include <WiFi.h>           // For ESP32 WiFi
#include <HTTPClient.h>     // For making HTTP requests

// Replace with your network credentials:
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// FastAPI endpoint:
const char* serverName = "http://YOUR_BACKEND_URL/parking/public/send_parking_data";

// Hardcoded API key
String api_key = "#54321";

// HC-SR04 Pins
const int trigPin = 5;  // Example GPIO
const int echoPin = 18; // Example GPIO

#define SOUND_SPEED 0.034

long duration;
float distanceCm;

void setup() {
  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  WiFi.begin(sssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(" Connected to WiFi!");
}

void loop() {
  // Measure distance:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2;

  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  int statusValue;

  // Define occupied vs free
  if (distanceCm < 10) { // Set your threshold
    statusValue = 1; // Occupied
  } else {
    statusValue = 0; // Free
  }

  // Send POST if connected:
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverName);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // ✅ Body: api_key and value ONLY
    String httpRequestData = 
      "api_key=" + api_key + 
      "&value=" + String(statusValue);

    Serial.print("Sending POST: ");
    Serial.println(httpRequestData);

    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      Serial.println("Response:");
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(5000); // Wait 5 sec before next reading
}
