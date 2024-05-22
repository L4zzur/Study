#include <stdint.h>
#include <stm32f10x.h>

/*
Задание 4
Написать библиотеку для обмена данными с внешними устройствами по протоколу SPI (SPI1)
Реализовать:
- void SPI1_Init(void);
- void SPI1_Write(uint8_t data)
- uint8_t SPI1_Read();
*/

void delay_us(uint32_t us){
    __asm__ __volatile__(
        "push {r0}\r\n"
        "mov R0, %0\r\n"
        "_loop:\r\n"
            "cmp R0, #0\r\n"
            "beq _exit\r\n"
            "sub R0, R0, #1\r\n"
            "nop\r\n"
            "b _loop\r\n"
        "_exit:\r\n"
        "pop {r0}\r\n"
        :: "r"(9 * us)
    );
};



void SPI1_Init()
{
    // Включаем тактирование PORTA, SPI1
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_SPI1EN;
    // A4 -> CS (chip select)
    GPIOA->CRL = GPIOA->CRL & ~(GPIO_CRL_MODE4 | GPIO_CRL_CNF4);
    GPIOA->CRL = GPIOA->CRL | GPIO_CRL_MODE4_0; // A4 Output, 10 Mhz, General purpose output push-pull
    // A5 -> SCL (clock)
    GPIOA->CRL = GPIOA->CRL & ~(GPIO_CRL_MODE5 | GPIO_CRL_CNF5);
    GPIOA->CRL = GPIOA->CRL | GPIO_CRL_MODE5_0 | GPIO_CRL_CNF5_1; // A5 Output, 10 Mhz, Alternate function output push-pull
    // A2 -> RSE (reset)
    GPIOA->CRL = GPIOA->CRL & ~(GPIO_CRL_MODE2 | GPIO_CRL_CNF2);
    GPIOA->CRL = GPIOA->CRL | GPIO_CRL_MODE2_0; // A2 Output, 10 Mhz, General purpose output push-pull
    // A3 -> RS (command/data)
    GPIOA->CRL = GPIOA->CRL & ~(GPIO_CRL_MODE3 | GPIO_CRL_CNF3);
    GPIOA->CRL = GPIOA->CRL | GPIO_CRL_MODE3_0; // A3 Output, 10 Mhz, General purpose output push-pull
    // A7 -> MOSI (SPI, serial input)
    GPIOA->CRL = GPIOA->CRL & ~(GPIO_CRL_MODE7 | GPIO_CRL_CNF7);
    GPIOA->CRL = GPIOA->CRL | GPIO_CRL_MODE7_0 | GPIO_CRL_CNF7_1; // A7 Output, 10 Mhz, Alternate function output push-pull

    // Параметры SPI
    SPI1->CR1 &= ~SPI_CR1_DFF; // Размер кадра 8 бит
    SPI1->CR1 &= ~SPI_CR1_LSBFIRST; // MSB First
    SPI1->CR1 &= ~SPI_CR1_CRCEN; // CRC Calculation disable
    SPI1->CR1 |= SPI_CR1_SSM; // SS в высоком состоянии
    SPI1->CR1 |= SPI_CR1_SSI;
    // SPI1->CR1 &= ~SPI_CR1_BR; // Обнуляем
    // SPI1->CR1 |= SPI_CR1_BR_2; // ставим скорость передачи f_PCLK/32
    SPI1->CR1 |= SPI_CR1_BR;
    SPI1->CR1 |= SPI_CR1_MSTR; // Master mode (ведущий)
    SPI1->CR1 &= ~SPI_CR1_CPOL; // Polarity
    SPI1->CR1 &= ~SPI_CR1_CPHA; // Phase

    SPI1->CR1 |= SPI_CR1_SPE; // Включаем SPI
}

void SPI1_Write(uint8_t data)
{
    // Ждем, пока не освободится буфер передатчика
    while (!(SPI1->SR & SPI_SR_TXE));
    // Заполняем буфер передатчика
    SPI1->DR = data;
}

uint8_t SPI1_Read()
{
    SPI1->DR = 0; // запускаем обмен
    // Ждем, пока не появится новое значение в буфере приемника
    while (!(SPI1->SR & SPI_SR_RXNE));
    // Возвращаем прочитанное значение
    return SPI1->DR;
}

void cmd(uint8_t data)
{
    GPIOA->ODR &= ~GPIO_ODR_ODR3;
    GPIOA->ODR &= ~GPIO_ODR_ODR4;
    delay_us(1000);
    SPI1_Write(data);
    GPIOA->ODR |= GPIO_ODR_ODR4;
}

void dat(uint8_t data)
{
    GPIOA->ODR |= GPIO_ODR_ODR3;
    GPIOA->ODR &= ~GPIO_ODR_ODR4;
    delay_us(1000);
    SPI1_Write(data);
    GPIOA->ODR |= GPIO_ODR_ODR4;
}

void main(void) 
{
    RCC->APB2ENR |= RCC_APB2ENR_IOPCEN;
    GPIOC->CRH = GPIOC->CRH & ~(GPIO_CRH_CNF13 | GPIO_CRH_MODE13) | GPIO_CRH_MODE13_0;
    GPIOC->ODR = GPIOC->ODR & ~GPIO_ODR_ODR13;
    SPI1_Init();
    
    GPIOA->ODR &= ~GPIO_ODR_ODR2;
    delay_us(1000);
    GPIOA->ODR |= GPIO_ODR_ODR2;
    delay_us(1000);

    cmd(0xA2);
    cmd(0xA0);
    cmd(0xC8);
    cmd(0x28 | 0x07);
    cmd(0x20 | 0x05);
    cmd(0xA6);
    cmd(0xAF);

    // Очищение экрана в цикле по всем 8 страницам
    for (int k = 0; k < 8; k++)
    {  
        cmd(0xB0 | k); // Выбор страницы (линии)
        cmd(0b00010000); // Перевод каретки в начало
        cmd(0b00000000);
        delay_us(1000);
        for (int i = 0; i < 129; i++) { 
            dat(0xFF);
        }
    }

    while (1) {
        delay_us(100000);
        GPIOC->ODR |= GPIO_ODR_ODR13;
        delay_us(100000);
        GPIOC->ODR = GPIOC->ODR & ~GPIO_ODR_ODR13;
    }
}

