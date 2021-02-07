#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
void thread(void)
{
    int i;
    for (i = 0; i < 3; i++)
    {
        printf("1\n");
    }
    sleep(3);
    printf("wake up\n");
    return;
}
int main()
{
    printf("Hello world from t1 Main\n");
    int i, ret1;
    pthread_t id1;
    ret1 = pthread_create(&id1, NULL, (void *)thread, NULL);
    if (ret1 != 0)
    {
        printf("error\n");
        exit(1);
    }
    printf("this is a main process\n");
    pthread_join(id1,NULL);
    return 0;
}
