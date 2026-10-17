// EMMY AI GLASSES
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#define BUTTON_PIN 1
const char* ssid = "EMMY_WIFI";
const char* password = "12345678";
const char* serverUrl = "https://emmy97193.pythonanywhere.com/ai-glasses/see";
void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.println("EMMY AI Ready");
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) delay(500);
}
void loop() {
  if(digitalRead(BUTTON_PIN) == LOW){
    delay(300);
    camera_fb_t * fb = esp_camera_fb_get();
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "image/jpeg");
    http.POST(fb->buf, fb->len);
    Serial.println(http.getString());
    http.end();
    esp_camera_fb_return(fb);
    delay(2000);
  }
}
