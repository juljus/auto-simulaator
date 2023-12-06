#include <EEPROM.h>

int rool = A0;
int gaas = A1;
int pidur = 3;
int nupp = 2;
int nupp_vajutused = 0;
int rool_min = 0;
int rool_max = 1024;

void setup() {
  rool_min = EEPROM.read(0);
  rool_max = EEPROM.read(1);

  Serial.begin(9600);
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

  // Serial.print(rool_mapped);
  // Serial.println(" r");

  //Serial.print(gaas_v);
  //Serial.println(" g");

  //Serial.print(pidur_v);
  //Serial.println(" p");
  
  //Serial.println(nupp_v);
}
