#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>

//---------------------------
// Лабораторная 1
// Задание 1
// Создать программу, которая, используя функцию CryptEnumProviders,
// выводит на экран название всех криптопровайдеров, установленных в системе, и номер их типа.
//---------------------------

int main()
{
    DWORD dwProvType, cbProvName;
    DWORD dwBuffSize = 50 * sizeof(TCHAR);
    LPTSTR pszProvName = (TCHAR *) malloc(dwBuffSize);

    DWORD i = 0;
    BOOL result;
    int errorNo;

    while (TRUE) {
        cbProvName = dwBuffSize;
        result = CryptEnumProviders(i, NULL, 0, &dwProvType,
                                    pszProvName, &cbProvName);
        if (result) {
            printf("Provider name: %s; type number: %d\n",
                pszProvName, dwProvType);
            i++;
        }
        else {
            errorNo = GetLastError();
            if (errorNo == ERROR_NO_MORE_ITEMS) break;
            if (errorNo == ERROR_MORE_DATA) {
                free(pszProvName);
                dwBuffSize = cbProvName;
                pszProvName = (TCHAR *) malloc(dwBuffSize);
            }
        }
    }

    return 0;
}
