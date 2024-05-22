#include <stdint.h>
#include <stm32f10x.h>
#include <stdio.h>
#include <stdlib.h>

/*
Задание 5
Работа с UART
Реализовать библиотеку для работы с UART:
- void UART1_Init(void);
- void UART1_Write(uint8_t data)
- uint8_t UART1_Read()
*/


// Инициализация
void UART1_Init()
{
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_USART1EN;

    GPIOA->CRH = 0b100010010000;
    GPIOA->ODR |= GPIO_ODR_ODR10;

    USART1->CR1 |= USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
    USART1->BRR = 7500;
    USART1->CR2 &= ~(USART_CR2_STOP_0 | USART_CR2_STOP_1);
    USART1->CR2 &= ~USART_CR2_CLKEN;  
}

// Запись в буфер
void UART1_Write(uint8_t data)
{
    // Ждем, пока не освободится буфер передатчика
    while ((USART1->SR & USART_SR_TXE) == 0);
    // заполняем буфер передатчика
    USART1->DR = data;
}

// Чтение из буфера
uint8_t UART1_Read(void)
{
    // Ждем, пока не появится новое значение в буфере приемника
    while ((USART1->SR & USART_SR_RXNE) == 0);
    // возвращаем значение буфера приемника
    return USART1->DR;
}

// Считывание цифры или пробела/минуса
uint8_t read_digit(uint8_t special_char) 
{
	uint8_t char_ = 0;
	while ((char_ < '0' || char_ > '9') && char_ != special_char) 
	{
		char_ = UART1_Read();
	}
	return char_;
}

// Считывание оператора
uint8_t read_operator() 
{
	uint8_t char_ = 0; // переменная для хранения считанного символа
	while (1) {
		char_ = UART1_Read();
		switch (char_) {
		case '+':
		case '-':
		case '*':
		case '/':
			return char_;
		default:
			continue;
		}
	}
}

// Считывание числа
uint32_t read_number() {
	int32_t number = 0;
	uint8_t char_ = read_digit(45); // первый символ может быть '-'

	UART1_Write(char_); 
	uint8_t negative = 0; // флаг отрицательного числа
	if (char_ == '-') 
		negative = 1; 
	else 
		number = char_ - '0';

	while (1) 
	{
		uint8_t char_ = read_digit(32); // " " - фиксируем конец числа
		UART1_Write(char_);
		if (char_ == ' ') // если число закончилось, то выходим
			break;
		char_ -= '0';
		number = number * 10 + char_; // считываем следующую цифру
	}
	if (negative) 
		return -number;
	return number;
}

// Вывод числа
void write_number(int32_t number) {
	uint8_t length = 0; // длина числа
	int32_t tmp = number; // временная копия
	uint8_t arr[16] = {0}; // массив для хранения числа
	uint8_t negative = 0; // флаг отрицательного числа

	// если число отрицательное, то меняем знак на плюс
	if (number < 0)
	{
		number *= -1;
		negative = 1;
	}

	// определяем длину числа
	do { 
		tmp /= 10;
		length += 1;
	} while (tmp != 0);

	// заполняем массив
	for (uint8_t i = 0; i < length; i++) {
		arr[i] = number % 10 + '0';
		number /= 10;
	}

	// добавляем знак, если число отрицательное
	if (negative)
		UART1_Write('-');

	// вывод числа
	for (uint8_t i = length; i > 0; i--)
		UART1_Write(arr[i - 1]); 

	UART1_Write(32); // пробел
}

void main(void) {
	UART1_Init();

	while (1) {
		int32_t a = read_number(); // считываем первое число
		uint8_t op = read_operator(); // считываем оператор
		UART1_Write(op); 
		UART1_Write(' ');
		int32_t b = read_number(); // считываем второе число
		UART1_Write('=');
		UART1_Write(' ');
		int32_t result = 0;
		uint8_t error = 0;

		// определяем операцию
		switch (op) { 
			case '+': 
				result = a + b;
				break;
			case '-':
				result = a - b;
				break;
			case '*': 
				result = a * b;
				break;
			case '/':
				if (b == 0)
					error = 1;
				else
					result = a / b;
				break;
		}

		// вывод результата
		if (error)
			UART1_Write(63); // "?" - ошибка
		else
			write_number(result);
		UART1_Write('\r');
		UART1_Write('\n');
	}
}