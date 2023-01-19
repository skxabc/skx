#include <stdio.h>
char *mystrncpy(char *str1, const char *str2, size_t n){
    if(str1 == nullptr || str2 == nullptr)return nullptr;
    char *ptr = str1;
    while (n--)
    {
        *str1++ = *str2++;
    }
    *str1='\0';
    
    return ptr;
}
int main(int argc, char **argv){
    char name[]="hello world";
    char dest[20];
    mystrncpy(dest, name, sizeof(name));
    printf("dest:%s\n", dest);
    return 0;
}