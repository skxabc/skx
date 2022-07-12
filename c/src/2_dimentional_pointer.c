#include <stdio.h>
#include <stdlib.h>
typedef struct test_
{
    int a;
    int b;
    void (*func)();
}sttest;
void (*func1)();
void callback(sttest* test)
{
    printf("callback hello world a:%d\n",test->a);
}

int main(int argn, char * argv[])
{
    sttest a = {11,22,callback};
    // a.func(&a);
    func1 = callback;
    func1(&a);
    return 0;
}