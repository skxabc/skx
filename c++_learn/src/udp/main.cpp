#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/select.h>
#include <netdb.h>

int send_udp_packet(const char *host, const char *port, const char *message) {
    struct addrinfo hints, *servinfo, *p;
    int sockfd, rv;
    int numbytes;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;

    if ((rv = getaddrinfo(host, port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    for (p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                             p->ai_protocol)) == -1) {
            perror("talker: socket");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "talker: failed to bind socket\n");
        return 2;
    }

    if ((numbytes = sendto(sockfd, message, strlen(message), 0,
                           p->ai_addr, p->ai_addrlen)) == -1) {
        perror("talker: sendto");
        exit(1);
    }

    freeaddrinfo(servinfo);

    return sockfd;
}

int recv_udp_packet(int sockfd, char *buf, int buf_len) {
    struct sockaddr_storage their_addr;
    socklen_t addr_len;
    int numbytes;

    addr_len = sizeof their_addr;
    if ((numbytes = recvfrom(sockfd, buf, buf_len - 1, 0,
                             (struct sockaddr *) &their_addr, &addr_len)) == -1) {
        perror("recvfrom");
        exit(1);
    }

    buf[numbytes] = '\0';

    return numbytes;
}

int diff_time_ms(struct timeval *start, struct timeval *end) {
    return (end->tv_sec - start->tv_sec) * 1000 + (end->tv_usec - start->tv_usec) / 1000;
}

int get_current_time(struct timeval *time) {
    gettimeofday(time, NULL);
    return 0;
}

int main(int argc, char const *argv[])
{
    int cnt = 30;
    char msg[256];
    while (cnt -- > 0)
    {
        struct timeval start, end;
        get_current_time(&start);
        printf("begin\n");
        int sockfd = send_udp_packet("10.180.97.83", "5555", "hello");
        printf("udp sent\n");
        recv_udp_packet(sockfd, msg, 256);
        printf("udp recv\n");
        get_current_time(&end);
        printf("%d\n", diff_time_ms(&start, &end));
        printf("%s\n", msg);
    }
    
    return 0;
}
