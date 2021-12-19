#include<stdlib.h>
#include<stdio.h>

int main(int argc, char * agrv[])
{
    short a = 0;
    a = 1;
    printf("a addr:0x%p\n", &a);
    printf("haoyue a:%d\n", a);
    printf("next value:%d\n", *(char*)(&a + 1));
    return 0;
}