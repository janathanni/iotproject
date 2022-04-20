#include <Arduino.h>
#line 1 "/Users/kimdonghyun/developer/raspberrypi/project_pri/nodemcu/remote_light/app.ino"
#include <ESP8266WiFi.h>
#include <MqttCom.h>
#include <PubSubClient.h>
#include <Servo.h>

const char *ssid = "olleh_WiFi_05A8";
const char *password = "0000000942";
const char *mqtt_server = "172.30.1.17";

Servo servo;

MqttCom com;
WiFiClient client;
PubSubClient mqttClient(client);

#line 16 "/Users/kimdonghyun/developer/raspberrypi/project_pri/nodemcu/remote_light/app.ino"
void callback(char *topic, byte *payload, unsigned int length);
#line 35 "/Users/kimdonghyun/developer/raspberrypi/project_pri/nodemcu/remote_light/app.ino"
void setup();
#line 60 "/Users/kimdonghyun/developer/raspberrypi/project_pri/nodemcu/remote_light/app.ino"
void loop();
#line 16 "/Users/kimdonghyun/developer/raspberrypi/project_pri/nodemcu/remote_light/app.ino"
void callback(char *topic, byte *payload, unsigned int length)
{
  payload[length] = '\0';
  // int value = String((char *)payload).toInt();

  Serial.println(topic);
  Serial.println(String((char *)payload));
  if (String((char *)payload) == "myroom turn on")
  {
    servo.write(180);
  }
  else if (String((char *)payload) == "myroom turn off")
  {
    servo.write(0);
  }

  Serial.println("hihihihi");
}

void setup()
{
  Serial.begin(115200);
  servo.attach(D2);
  WiFi.begin(ssid, password);
  mqttClient.setServer(mqtt_server, 1883);
  mqttClient.setCallback(callback);
  while (!mqttClient.connected())
  {
    Serial.println("Connecting to MQTT....");

    if (mqttClient.connect("ESP8266Cleint"))
    {
      mqttClient.subscribe("iot/light/myRoom");
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.print(mqttClient.state());
      delay(2000);
    }
  }
}

void loop()
{
  mqttClient.loop();
}

