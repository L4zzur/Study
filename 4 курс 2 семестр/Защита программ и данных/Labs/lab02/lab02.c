#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>

int main() {
    HCRYPTPROV hProv;
    DWORD bData;
    DWORD dwDataLen = sizeof(bData);

    if (!CryptAcquireContext(&hProv, NULL, "Microsoft Enhanced RSA and AES Cryptographic Provider", 24, CRYPT_VERIFYCONTEXT))
    {
        printf("Cannot connect to provider");
        return 0;
    }

    if (CryptGetProvParam(hProv, PP_IMPTYPE, &bData, &dwDataLen, 0))
    {
        printf("Provider implementation type is ");
        switch (bData) 
        {
            case CRYPT_IMPL_HARDWARE:
                printf("Hardware");
                break;
            case CRYPT_IMPL_SOFTWARE:
                printf("Software");
                break;
            case CRYPT_IMPL_MIXED:
                printf("Mixed");
                break;
            case CRYPT_IMPL_UNKNOWN:
                printf("Unknown");
                break;
            case CRYPT_IMPL_REMOVABLE:
                printf("Removable");
                break;
            default:
                printf("Wrong implementation type");
        }
    }
    else
    {
        printf("Cant define provider implementation type");
    }
    
    if (CryptGetProvParam(hProv, PP_VERSION, &bData, &dwDataLen, 0)) 
    {
        printf("\nProvider version is %d", bData);
        printf("\nProvider version is %d.%d\n\n", (bData & 0xFF00) >> 8, bData & 0xFF);
    }

    PROV_ENUMALGS_EX algoInfo;
    DWORD dwBufLen = sizeof(algoInfo);
    DWORD dwFlags = CRYPT_FIRST;

    printf("%5s %15s %10s %12s %40s %7s %7s %7s %8s %9s\n", "ID", "Class", "Type", "Name", "Long name", "Def len", "Min len", "Max len", "Name len", "Protocols");
    while (TRUE) {
        dwDataLen = dwBufLen;
        if (CryptGetProvParam(hProv, PP_ENUMALGS_EX, &algoInfo, &dwDataLen, dwFlags))
        {
            LPCTSTR className;
            LPCTSTR typeName;

            switch (GET_ALG_CLASS(algoInfo.aiAlgid))
            {
                case ALG_CLASS_DATA_ENCRYPT:
                    className = "Data Encrypt";
                    break;
                case ALG_CLASS_MSG_ENCRYPT:
                    className = "Message Encrypt";
                    break;
                case ALG_CLASS_HASH:
                    className = "Hash";
                    break;
                case ALG_CLASS_KEY_EXCHANGE:
                    className = "Key Exchange";
                    break;
                case ALG_CLASS_SIGNATURE:
                    className = "Signature";
                    break;
                default:
                    className = "Another";
            }

            switch (GET_ALG_TYPE(algoInfo.aiAlgid))
            {
                case ALG_TYPE_DSS:
                    typeName = "DSS";
                    break;
                case ALG_TYPE_RSA:
                    typeName = "RSA";
                    break;
                case ALG_TYPE_BLOCK:
                    typeName = "Block";
                    break;
                case ALG_TYPE_STREAM:
                    typeName = "Stream";
                    break;
                default:
                    typeName = "Another";
                    break;
            }

            printf("%5d %15s %10s %12s %40s %7d %7d %7d %8d %9d\n",
				algoInfo.aiAlgid, className, typeName, algoInfo.szName, algoInfo.szLongName, algoInfo.dwDefaultLen, algoInfo.dwMinLen, algoInfo.dwMaxLen, algoInfo.dwNameLen, algoInfo.dwProtocols);

            dwFlags = CRYPT_NEXT;
        }
        else
        {
            DWORD error = GetLastError();
            if (error == ERROR_NO_MORE_ITEMS)
                break;
            else {
                printf("Error!");
                return 0;
            }
        }
    }


    CryptReleaseContext(hProv, 0);
    return 0;
}