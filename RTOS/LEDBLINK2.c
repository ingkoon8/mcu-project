#include <FreeRTOS_AVR.h>

// Thread1, 8번 pin에 LED 설정 후 200ms마다 Blink, Task 1 출력
void Thread1( void *pvParameters )  {

  pinMode(8, OUTPUT);

  while(1) {
    Serial.println("Task1");
    digitalWrite(8, HIGH);   
    vTaskDelay( 200 / portTICK_PERIOD_MS ); 
    digitalWrite(8, LOW);    
    vTaskDelay( 200 / portTICK_PERIOD_MS ); 
  }
}

// Thread2, 7번 pin에 LED 설정 후 300ms마다 Blink, Task 2 출력
void Thread2( void *pvParameters ) {

  pinMode(7, OUTPUT);
  while(1) {
    Serial.println("Task2");
    digitalWrite(7, HIGH);   
    vTaskDelay( 300 / portTICK_PERIOD_MS ); 
    digitalWrite(7, LOW);   
    vTaskDelay( 300 / portTICK_PERIOD_MS ); 
  }

}

// Threadprint, 500ms마다 카운트 1씩 추가해서 출력
void Threadprint( void *pvParameters ) {

  int counter = 0;
  while(1) {
    counter++;
    Serial.println(counter); 
    vTaskDelay(500 / portTICK_PERIOD_MS); }
}


void setup() {

  Serial.begin(9600);
  xTaskCreate(Thread1, NULL, configMINIMAL_STACK_SIZE, NULL, 1, NULL);
  xTaskCreate(Thread2, NULL, configMINIMAL_STACK_SIZE, NULL, 2, NULL);
  xTaskCreate(Threadprint, NULL, configMINIMAL_STACK_SIZE, NULL, 3, NULL);
  vTaskStartScheduler();

}

void loop() {

}
