#include <LiquidCrystal.h>

// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  lcd.begin(16, 2);
  lcd.print("Waiting for game");
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      String userScore = data.substring(0, commaIndex);
      String computerScore = data.substring(commaIndex + 1);

      if (userScore == "Game Over") {
        lcd.clear();
        lcd.print(computerScore);  // Display winner message
        delay(5000);  // Hold final message
        lcd.clear();
        lcd.print("Waiting for game");
      } else {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("You: " + userScore);
        lcd.setCursor(0, 1);
        lcd.print("Comp: " + computerScore);
        delay(1000);
      }
    }
  }
}
