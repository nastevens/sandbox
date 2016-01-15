#include <fcntl.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>


int main(int argc, char *argv[])
{
    int fd = -1;

    fd = open("/dev/ttys/xbee", O_RDWR);
    if (fd < 0)
    {
        perror("open");
        goto error;
    }

    printf("Setting break condition\n");
    if (ioctl(fd, TIOCSBRK) < 0)
    {
        perror("set break");
        goto error;
    }

    sleep(5);

    printf("Clearing break condition\n");
    if (ioctl(fd, TIOCCBRK) < 0)
    {
        perror("clear break");
        goto error;
    }

    close(fd);

    return 0;

error:
    if (fd >= 0)
    {
        close(fd);
    }
    return 1;
}
