#include <stdio.h>
#include <windows.h>

int main()
{
    DWORD bufferLength = NULL;  // длина массива

    GetUserName(NULL, &bufferLength);   // пустой адрес и адрес длины буффера, для получения длины буффера
    printf("Required buffer length: %d\n", bufferLength);

    TCHAR * nameBuffer = malloc(bufferLength);  // массив
    GetUserName(nameBuffer, &bufferLength);
    printf("Username: %s (length: %d)", nameBuffer, bufferLength);

    free(nameBuffer); // очистка буффера из динамическои? памяти

    return 0;
}
