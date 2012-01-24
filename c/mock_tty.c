#define _XOPEN_SOURCE
#include <errno.h>
#include <signal.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/select.h>


static uint8_t buffer[1024];

volatile bool shutdown = false;

static inline void
handle_error (
        const char *const msg,
        const int e )
{
    fprintf(stderr, "`%s` failed: %s (%d)\n", msg, strerror(e), e);
    exit(EXIT_FAILURE);
}

static void sig_handler(int signum)
{
    if (signum == SIGINT)
    {
        shutdown = true;
    }
}

int main(int argc, char* argv[])
{
    int pt;

    signal(SIGINT, sig_handler);

    pt = open("/dev/ptmx", O_RDWR | O_NOCTTY);
    if (pt < 0)
    {
        perror("open /dev/ptmx");
        return 1;
    }

    grantpt(pt);
    unlockpt(pt);

    fprintf(stderr, "Slave device: %s\n", ptsname(pt));

    bool do_write = false;
    uint8_t message[] = {0x01, 0x03, 0x02, 0x00, 0x01, 0x79, 0x84};
    while(!shutdown)
    {
        fd_set rd, wr;
        FD_ZERO(&rd);
        FD_ZERO(&wr);

        FD_SET(pt, &rd);

        if (do_write)
        {
            FD_SET(pt, &wr);
        }

        int selected = select(pt + 1, &rd, &wr, NULL, NULL);
        printf("selected\n");

        if (selected == -1 && errno == EINTR)
        {
            continue;
        }

        if (selected == -1)
        {
            handle_error("select()", errno);
        }

        if (FD_ISSET(pt, &rd))
        {
            int n = read(pt, buffer, sizeof buffer);
            for (int i = 0; i < n; ++i)
            {
                fprintf(stdout, "%02X ", buffer[i]);
                fflush(stdout);
                do_write = true;
            }
            fprintf(stdout, "\n");
        }

        if (FD_ISSET(pt, &wr))
        {
            int n = write(pt, message, sizeof message);
            fprintf(stdout, "Wrote message\n");
            fflush(stdout);
            do_write = false;
        }
    }

    close(pt);
    return 0;
}
