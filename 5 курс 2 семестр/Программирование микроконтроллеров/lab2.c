#include <stdint.h>
#include <stm32f10x.h>

void delay_us(uint32_t us){
    __asm__ __volatile__(
        "push {r0}\r\n"
        "mov R0, %0\r\n"
        "_loop:\r\n"
        "subs R0, R0, #1\r\n"
        "beq _exit\r\n"
        "nop\r\n"
        "b _loop\r\n"
    "_exit:\r\n"
        "pop {r0}\r\n"
    :: "r"(9 * us)
    );
}



int main(void) {
    RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;
    GPIOC->CRH = GPIOC->CRH & ~(GPIO_CRH_CNF13 | GPIO_CRH_MODE13) | GPIO_CRH_MODE13_0; // PC13 = output
    GPIOC->CRH = GPIOC->CRH & ~(GPIO_CRH_CNF14 | GPIO_CRH_MODE14) | GPIO_CRH_CNF14_1; // PC14 = Input
    GPIOC->ODR |= GPIO_ODR_ODR14; // Enable PC14 Pull-up

    while (1) {
        GPIOC->ODR |= GPIO_ODR_ODR13; // Включаем светодиод
        delay_us(500000); // Задержка 500 мс
        GPIOC->ODR &= ~GPIO_ODR_ODR13; // Выключаем светодиод
        delay_us(500000); // Задержка 500 мс
    }
}

