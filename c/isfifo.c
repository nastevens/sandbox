#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

static void
handle_error(const char *const command, const int e)
{
    fprintf(stderr, "`%s` failed: %s (%d)\n", command, strerror(e), e);
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage:\n\t%s <path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char* const path = argv[1];
    int fd;
    if ((fd = open(path, O_RDONLY)) == -1)
    {
        handle_error("open", errno);
    }

    struct stat buf;
    if (fstat(fd, &buf) == -1)
    {
        handle_error("fstat", errno);
    }

    printf("buf.st_mod=0x%08x\n", (int)buf.st_mode);
    if (S_ISFIFO(buf.st_mode))
    {
        fprintf(stdout, "%s is a FIFO\n", path);
    }
    else
    {
        fprintf(stdout, "%s is not a FIFO\n", path);
    }

    close(fd);

    return EXIT_SUCCESS;
}
