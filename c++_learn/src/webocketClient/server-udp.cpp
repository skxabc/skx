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

int listen_udp_and_send_back(const char *port) {
    struct addrinfo hints, *servinfo, *p;
    int sockfd, rv;
    int numbytes;
    char buf[1024];
    struct sockaddr_storage their_addr;
    socklen_t addr_len;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    if ((rv = getaddrinfo(NULL, port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }

    for (p = servinfo; p != NULL; p = p->ai_next) {
        if ((sockfd = socket(p->ai_family, p->ai_socktype,
                             p->ai_protocol)) == -1) {
            perror("listener: socket");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "listener: failed to bind socket\n");
        return 2;
    }

    if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
        close(sockfd);
        perror("listener: bind");
        return 3;
    }

    freeaddrinfo(servinfo);

    addr_len = sizeof their_addr;
    while (1)
    {
        if ((numbytes = recvfrom(sockfd, buf, sizeof buf, 0,
                                 (struct sockaddr *)&their_addr, &addr_len)) == -1)
        {
            perror("recvfrom");
            exit(1); 
        }

        if (sendto(sockfd, buf, numbytes, 0,
                   (struct sockaddr *)&their_addr, addr_len) == -1)
        {
            perror("sendto");
            exit(1);
        }
    }
    
    
}

int main(int argc, char const *argv[])
{
    listen_udp_and_send_back(argv[1]);
    pause();
    return 0;
}
