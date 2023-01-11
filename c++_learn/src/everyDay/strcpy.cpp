#include<stdio.h>
char *mystrcpy(char *dst, const char *src){
    if(dst == nullptr || src == nullptr)return nullptr;
    char *ptr = dst;
    while(*src != '\0'){
        *dst++ = *src++;
    }
    *dst = '\0';
    return ptr;
}
int main(int argc, char **argv){
    char name[]="shikaixun";
    char dest[20];
    printf("before strcpy dest is:%s", dest);
    mystrcpy(dest, name);
    printf("after strcpy dest is:%s", dest);
    return 0;
}