#include <stdio.h>
#include <stdlib.h>
typedef struct test_
{
    int a;
    int b;
}sttest;
static sttest A;
void get(sttest *r)
{
    r = &A;
    return;
}
int main(int argn, char * argv[])
{
    // sttest *A = (sttest *)malloc(sizeof(sttest));
    // A.a = 1;
    // A.b = 2;
    // sttest *B  = (sttest *)malloc(sizeof(sttest));
    // get(B);
    // printf("B->a:%d B->b:%d\n",B->a,B->b);
    char *a = "{\"header\":{\"name\":\"resourceDisWakeupResponse\",\"namespace\":\"resourceConfig\"},\"payload\":{\"ratioActive\":0,\"arrayType\":0,\"boardType\":9,\"debug\":1,\"fileNum\":101,\"energyDiff\":0.1,\"micRatio\":6,\"blockSize\":115200,\"pat";
    printf("strlen(a):%d", strlen(a));
    return 0;
}