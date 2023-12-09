#include <EEPROM.h>

#define MIN_ADDRESS 0
#define MAX_ADDRESS 100
int rool = A0;
int gaas = 7;
int pidur = 3;
int nupp = 2;
int nupp_vajutused = 0;
int rool_min = 0;
int rool_max = 1024;

int disable_nupp = 5;
int disabled = 0;

void setup() {
  EEPROM.get(MIN_ADDRESS, rool_min);
  EEPROM.get(MAX_ADDRESS, rool_max);

  Serial.begin(9600);
  Serial.println("Starting program");
  Serial.print("Rool min ");
  Serial.println(rool_min);
  Serial.print("Rool max ");
  Serial.println(rool_max);

  pinMode(disable_nupp, INPUT_PULLUP);
  pinMode(gaas, INPUT_PULLUP);
  pinMode(pidur, INPUT_PULLUP);
  pinMode(nupp, INPUT_PULLUP);
  delay(5000);

}

void loop() {
  int rool_v = analogRead(rool);
  int gaas_v = digitalRead(gaas);
  int pidur_v = digitalRead(pidur);
  int nupp_v = digitalRead(nupp);

  if (digitalRead(disable_nupp)) {

    if (disabled == 1) {
      disabled = 0;
    }
    else {
      disabled = 1;
    }

    while (digitalRead(disable_nupp) == 0) {
      delay(0);
      Serial.println("???");
    }
  }

  if (nupp_v == 0 && nupp_vajutused == 0) {
    nupp_vajutused += 1;

    rool_min = rool_v;
    EEPROM.put(MIN_ADDRESS, rool_min);
    Serial.println(rool_min);
    Serial.println("Written to EEPROM min");
    delay(10000);
  }
  else if (nupp_v == 0 && nupp_vajutused == 1) {
    nupp_vajutused += 1;

    rool_max = rool_v;
    EEPROM.put(MAX_ADDRESS, rool_max);
    Serial.println(rool_max);
    Serial.println("Written to EEPROM max");
    delay(10000);
  }
  else if (nupp_v == 0 && nupp_vajutused > 1) {
    Serial.println("kalibreerimine on juba lõppenud");
    delay(10000);
  }

  int rool_mapped = map(rool_v, rool_min, rool_max, -100, 100);

  if (disabled == 0) {
    Serial.print(rool_mapped);
    Serial.println(" r");

    if (gaas_v == 0) {
      Serial.print("1");
      Serial.println(" g");
    }

    if (pidur_v == 0) {
      Serial.print("1");
      Serial.println(" p");
    }
  }
  delay(10);
}
