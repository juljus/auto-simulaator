#include <EEPROM.h>

#define MIN_ADDRESS 0
#define MAX_ADDRESS 100
#define MID_ADDRESS 200
int rool = A0;
int gaas = 7;
int pidur = 3;
int nupp = 2;
int nupp_vajutused = 0;
int rool_min = 0;
int rool_max = 1024;
int cal_min;
int cal_max;
int cal_mid;

int disable_nupp = 5;
int disabled = 0;

void setup() {
  EEPROM.get(MIN_ADDRESS, cal_min);
  EEPROM.get(MAX_ADDRESS, cal_max);
  EEPROM.get(MID_ADDRESS, cal_mid);

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
}

void Calibrate()
{
  while (nupp_vajutused <= 2)
  {
    int nupp_v = digitalRead(nupp);
    

    if (nupp_v == 0)
    {
      switch (nupp_vajutused)
      {
      case 0:
        cal_min = analogRead(rool);

        EEPROM.put(MIN_ADDRESS, cal_min);

        Serial.println(cal_min);
        Serial.println("Written to EEPROM min");
        break;

      case 1:
        cal_max = analogRead(rool);

        EEPROM.put(MAX_ADDRESS, cal_max);

        Serial.println(cal_max);
        Serial.println("Written to EEPROM min");
        break;

      case 2:
        cal_mid = analogRead(rool);

        EEPROM.put(MID_ADDRESS, cal_mid);

        Serial.println(cal_mid);
        Serial.println("Written to EEPROM min");
        break;

      default:
        break;
      }

      nupp_vajutused++;
      delay(1000);
    }
  }
}

void loop() {
  if (nupp_vajutused == 0) {
    Calibrate();
  }

  int rool_v = analogRead(rool);
  int gaas_v = digitalRead(gaas);
  int pidur_v = digitalRead(pidur);

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

  int rool_mapped;

  if (rool_v < cal_mid)
  {
    rool_mapped = map(rool_v, cal_min, cal_mid, -100, 0);
  }
  else
  {
    rool_mapped = map(rool_v, cal_mid, cal_max, 0, 100);
  }

  if (disabled == 0) {
    Serial.print(rool_mapped);
    Serial.println(" r");

    if (pidur_v == 0) {
      Serial.print("1");
      Serial.println(" p");
    }
    else if (gaas_v == 0) {
      Serial.print("1");
      Serial.println(" g");
    }
    else {
      Serial.print("1");
      Serial.println(" n");
    }
  }
  delay(10);
}
