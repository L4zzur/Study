#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>

//---------------------------
// Лабораторная 1
// Задание 2
// Создать программу, которая, используя функцию CryptEnumProviderTypes,
// выводит на экран название всех зарегистрированных в системе
// типов криптопровайдеров и число, соответствующее данному типу.
//---------------------------

int main()
{
    DWORD pdwProvType, pcbProvName;
    DWORD dwBuffSize = 50 * sizeof(TCHAR);
    LPTSTR pszProvName = (TCHAR *) malloc(dwBuffSize);

    DWORD i = 0;
    BOOL result;
    int errorNo;

    while (TRUE) {
        pcbProvName = dwBuffSize;
        result = CryptEnumProviderTypes(i, NULL, 0, &pdwProvType,
                                    pszProvName, &pcbProvName);
        if (result) {
            printf("Provider type name: %s; type number: %d\n",
                    pszProvName, pdwProvType);
            i++;
        }
        else {
            errorNo = GetLastError();
            if (errorNo == ERROR_NO_MORE_ITEMS) break;
            if (errorNo == ERROR_MORE_DATA) {
                free(pszProvName);
                dwBuffSize = pcbProvName;
                pszProvName = (TCHAR *) malloc(dwBuffSize);
            }
        }
    }

    return 0;
}
