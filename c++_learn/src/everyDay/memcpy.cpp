#include<stdio.h>
#include<iostream>

using namespace std;
void *mymemcpy(void *str1, const void *str2, size_t n){
    char *dest = (char *)str1;
    const char* src = (const char *)str2;
    if(dest != nullptr && src != nullptr){
        while (n--)
        {
            *(dest++) = *(src++);
        }
    }
    
    return dest;
}
int main(int argc, char** argv){
    char name[10]="shikaixun";
    char namecpy[10]="";
    printf("namecpy:%s", namecpy);
    mymemcpy(namecpy, name, sizeof(name));
    printf("namecpy:%s", namecpy);
    return 0;
}
