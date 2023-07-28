#include <FreeRTOS_AVR.h>

const uint8_t LED_PIN = 13;

// 세마포어 선언
SemaphoreHandle_t sem;

/*
 * Thread 1, Thread 2로부터 신호를 받으면 LED를 off함
 */
// Thread 1 선언
static void Thread1(void* arg) {
  while (1) {

    // Thread2로 부터 신호를 기다림
    xSemaphoreTake(sem, portMAX_DELAY);

    // LED off.
    digitalWrite(LED_PIN, LOW);
  }
}
//------------------------------------------------------------------------------
/*
 * Thread 2, LED on을 하고 Thread 1에게 신호를 줘서 LED off를 함
 */
// Thread 2 선언
static void Thread2(void* arg) {

  pinMode(LED_PIN, OUTPUT);

  while (1) {
    // LED on.
    digitalWrite(LED_PIN, HIGH);

    // 200 millisecond 딜레이
    vTaskDelay((200L * configTICK_RATE_HZ) / 1000L);

    // Thread 1에게 신호를 줌
    xSemaphoreGive(sem);

    // 200 milliseconds 딜레이
    vTaskDelay((200L * configTICK_RATE_HZ) / 1000L);
  }
}

void setup() {
  portBASE_TYPE s1, s2;

  Serial.begin(9600);
  
  // 세마포어 시작
  sem = xSemaphoreCreateCounting(1, 0);

  // Task를 우선순위 2로 생성
  s1 = xTaskCreate(Thread1, NULL, configMINIMAL_STACK_SIZE, NULL, 2, NULL);

  // Task를 우선순위 1로 설정
  s2 = xTaskCreate(Thread2, NULL, configMINIMAL_STACK_SIZE, NULL, 1, NULL);

  // check for creation errors
  if (sem== NULL || s1 != pdPASS || s2 != pdPASS ) {
    Serial.println(F("Creation problem"));
    while(1);
  }
  // 스케줄러 시작
  vTaskStartScheduler();
  Serial.println(F("Insufficient RAM"));
  while(1);
}

// loop는 사용하지 않음
void loop() {
  
}
