#include <stm32f10x.h>

uint8_t button_state = 0xFF;
int i = 0;
int freq = 7200;

int toggle = 0;

void TIM2_IRQHandler() {
	if (toggle == 1) {
		GPIOC->ODR |= GPIO_ODR_ODR13;
		toggle = 0;
	} else if (toggle == 0) {
		GPIOC->ODR = GPIOC->ODR & ~GPIO_ODR_ODR13;
		toggle = 1;
	}
	TIM2->SR &= ~TIM_SR_UIF;
}

void main() {
	RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;
	GPIOC->CRH = GPIOC->CRH & ~(GPIO_CRH_CNF13 | GPIO_CRH_MODE13) | GPIO_CRH_MODE13_0;
	GPIOC->ODR = GPIOC->ODR & ~GPIO_ODR_ODR13;

	RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
	NVIC_ClearPendingIRQ(TIM2_IRQn);
	RCC->APB1RSTR |= RCC_APB1RSTR_TIM2RST;
	RCC->APB1RSTR &= ~RCC_APB1RSTR_TIM2RST;

	NVIC_EnableIRQ(TIM2_IRQn);
	NVIC_SetPriority(TIM2_IRQn, 0);

	TIM2->PSC = freq;
    TIM2->ARR = 10000;
	TIM2->DIER |= TIM_DIER_UIE;
	
	TIM2->CR1 |= TIM_CR1_DIR;
	TIM2->CR1 |= TIM_CR1_CEN;

	GPIOC->ODR |= GPIO_ODR_ODR13;
	GPIOC->ODR = GPIOC->ODR & ~GPIO_ODR_ODR13;
	while (1) {
        if(!(GPIOC->IDR & GPIO_IDR_IDR14)){ // Button is pressed
            button_state = ~button_state;
            for(i=0; i<300000; i++){ __NOP(); }; // Debouncing
            while(!(GPIOC->IDR & GPIO_IDR_IDR14)); // Wait the button to be released
        }
        if(button_state){
            TIM2->PSC = 500;
        } else {
            TIM2->PSC = freq;
        }

    }
}