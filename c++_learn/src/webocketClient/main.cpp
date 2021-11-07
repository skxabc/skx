#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    // const int val = IPTOS_LOWDELAY;
    // setsockopt(sock, SOL_SOCKET, IP_TOS, (const void *)&val, sizeof(int));
    int value = 1;
    setsockopt(sock, SOL_SOCKET, SO_ERROR, (char *)&value, sizeof(int));
    fcntl(sock, F_SETFL, O_NONBLOCK);

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    addr.sin_port = htons(5555);

    int ret = connect(sock, (const struct sockaddr *)&addr, sizeof(addr));
    printf("ret : %d, errno %d desc:%s\n", ret, errno, strerror(errno));
    // ret为0或者-1&&errno 11为连接成功，可以加个检查流程
    sleep(3);
    /*
    在这调用recv接口，检查返回值和errno
    */
    //printf("skx1");
    fflush(stdout);
   char buf[256];
   while(1){
        ssize_t len = recv(sock, buf, 256, 0);
        printf("recv ret:%d errno:%d desc:%s\n", len, errno, strerror(errno));
        sleep(1);

   }


    // 也可以试试用getsockopt检查socket
    int error = 0;
    socklen_t length = sizeof(error);

    while (1) {
        if (getsockopt(sock, SOL_SOCKET, SO_ERROR, &error, &length) < 0) {
            printf("error : %d, errno %d\n", error, errno);
        }
        sleep(1);
    }
    return 0;
}