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

int print_addrinfo(struct addrinfo *ai) {
    char ipstr[INET6_ADDRSTRLEN];
    struct sockaddr_in *ipv4;
    struct sockaddr_in6 *ipv6;

    if (ai->ai_family == AF_INET) {
        ipv4 = (struct sockaddr_in *) ai->ai_addr;
        inet_ntop(AF_INET, &ipv4->sin_addr, ipstr, sizeof ipstr);
        printf("IPv4: %s\n", ipstr);
    } else if (ai->ai_family == AF_INET6) {
        ipv6 = (struct sockaddr_in6 *) ai->ai_addr;
        inet_ntop(AF_INET6, &ipv6->sin6_addr, ipstr, sizeof ipstr);
        printf("IPv6: %s\n", ipstr);
    } else {
        printf("Unknown address family\n");
    }

    return 0;
}

int listen_tcp(const char *port) {
    int sockfd, new_fd;
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage their_addr;
    socklen_t addr_len;
    char s[INET6_ADDRSTRLEN];
    int yes = 1;
    int rv;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
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

        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
                       sizeof(int)) == -1) {
            perror("setsockopt");
            exit(1);
        }

        if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
            close(sockfd);
            perror("listener: bind");
            continue;
        }

        break;
    }

    if (p == NULL) {
        fprintf(stderr, "listener: failed to bind socket\n");
        return 2;
    }

    freeaddrinfo(servinfo);

    if (listen(sockfd, 10) == -1) {
        perror("listen");
        exit(1);
    }

    printf("listener: waiting for connections...\n");

    addr_len = sizeof their_addr;
    if ((new_fd = accept(sockfd, (struct sockaddr *) &their_addr,
                         &addr_len)) == -1) {
        perror("accept");
        exit(1);
    }
    return new_fd;
}

int recv_tcp_and_send_back(int sockfd) {
    char buf[1024];
    int numbytes;

    if ((numbytes = recv(sockfd, buf, 1024, 0)) == -1) {
        perror("recv");
        exit(1);
    }

    printf("listener: got packet from %s\n", buf);

    if (send(sockfd, buf, numbytes, 0) == -1) {
        perror("send");
        exit(1);
    }

    return 0;
}

int listen_udp_and_send_back(const char *port) {
    struct addrinfo hints, *servinfo, *p;
    int sockfd, rv;
    int numbytes;
    char buf[1024];
    struct sockaddr_storage their_addr;
    socklen_t addr_len;

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    if ((rv = getaddrinfo(NULL, port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
        return 1;
    }
    print_addrinfo(servinfo);

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
    // listen_udp_and_send_back(argv[1]);
    int sockfd = listen_tcp(argv[1]);
    while (1) {
        recv_tcp_and_send_back(sockfd);
    }

    pause();
    return 0;
}
