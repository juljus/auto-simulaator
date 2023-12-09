#include <EEPROM.h>

int rool = A0;
int gaas = A1;
int pidur = 3;
int nupp = 2;
int nupp_vajutused = 0;
int rool_min = 0;
int rool_max = 1024;

int disable_nupp = 5;
int disabled = 0;

void setup() {
  rool_min = EEPROM.read(0);
  rool_max = EEPROM.read(1);

  Serial.begin(9600);

  pinMode(disable_nupp, INPUT);
  pinMode(rool, INPUT);
  pinMode(gaas, INPUT);
  pinMode(pidur, INPUT);
  pinMode(nupp, INPUT_PULLUP);

}

void loop() {
  int rool_v = analogRead(rool);
  int gaas_v = analogRead(gaas);
  int pidur_v = digitalRead(pidur);
  int nupp_v = digitalRead(nupp);

  if (digitalRead(disable_nupp)) {

    if (disabled == 1) {
      disabled = 0;
    }
    else {
      disabled = 1;
    }

    while (digitalRead(disable_nupp)) {
      delay(0);
    }
  }

  if (nupp_v == 0 && nupp_vajutused == 0) {
    nupp_vajutused += 1;

    rool_min = rool_v;
    EEPROM.write(0, rool_min);
    Serial.println(rool_min);
    delay(3000);
  }
  else if (nupp_v == 0 && nupp_vajutused == 1) {
    nupp_vajutused += 1;

    rool_max = rool_v;
    EEPROM.write(1, rool_max);
    Serial.println(rool_max);
  }
  else if (nupp_v == 0 && nupp_vajutused > 1) {
    Serial.println("kalibreerimine on juba lõppenud");
  }

  int rool_mapped = map(rool_v, rool_min, rool_max, -100, 100);

  if (disabled == 0) {
    Serial.print(-5);
    Serial.println(" r");

    if (gaas_v == 1) {
    Serial.print("1");
    Serial.println(" g");

    if (pidur_v == 1) {
    Serial.print("1");
    Serial.println(" p");
    }
  }
}
