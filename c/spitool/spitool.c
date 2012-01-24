/*
 * Copyright (c) 2014, Etherios, Inc.  All rights reserved.
 * Etherios, Inc. is a Division of Digi International.
 */

#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>
#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>
#include <stdbool.h>

#define CHIP_ID0 (0x00)
#define CHIP_ID1 (0x01)
#define START_SWITCH_MASK (0x01)
#define READ_DATA (0x03)
#define WRITE_DATA (0x02)

#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))

static void pabort(const char *s)
{
    perror(s);
    abort();
}

static const char *device = "/dev/spidev1.1";
static uint8_t mode;
static uint8_t bits = 8;
static uint32_t speed = 500000;
static uint16_t delay;
static bool read_mode;
static bool write_mode;

static uint8_t address;
static uint8_t count_or_value;

static void transfer(int fd)
{
    int ret;
    uint8_t tx[3];
    uint8_t* rx = NULL;
    if (read_mode)
    {
        rx = (uint8_t*)calloc(count_or_value, sizeof(uint8_t));
        tx[0] = READ_DATA;
        tx[1] = address;
        struct spi_ioc_transfer tr[] = {
            {
                .tx_buf = (unsigned long)tx,
                .rx_buf = (unsigned long)NULL,
                .len = 2,
                .delay_usecs = delay,
                .speed_hz = speed,
                .bits_per_word = bits,
            },
            {
                .tx_buf = (unsigned long)NULL,
                .rx_buf = (unsigned long)rx,
                .len = count_or_value,
                .delay_usecs = delay,
                .speed_hz = speed,
                .bits_per_word = bits,
            }
        };
        ret = ioctl(fd, SPI_IOC_MESSAGE(2), tr);
        if (ret < 1)
            pabort("can't send spi message");
        for (ret = 0; ret < count_or_value; ret++)
        {
            if (!(ret % 6))
                puts("");
            printf("%.2X ", rx[ret]);
        }

        free(rx);
    }
    else if (write_mode)
    {
        tx[0] = WRITE_DATA;
        tx[1] = address;
        tx[2] = count_or_value;
        struct spi_ioc_transfer tr0 = {
                    .tx_buf = (unsigned long)tx,
                    .rx_buf = (unsigned long)NULL,
                    .len = 3,
                    .delay_usecs = delay,
                    .speed_hz = speed,
                    .bits_per_word = bits,
                };
        ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr0);
        if (ret < 1)
            pabort("can't send spi message");
        printf("write 1 byte\n");
    }
    else
    {
        pabort("not write or read mode");
    }
}

static void print_usage(const char *prog)
{
    printf("Usage: %s [-DsbdlHOLC3]\n", prog);
    puts("  -D --device   device to use (default /dev/spidev1.1)\n"
         "  -s --speed    max speed (Hz)\n"
         "  -d --delay    delay (usec)\n"
         "  -b --bpw      bits per word \n"
         "  -l --loop     loopback\n"
         "  -H --cpha     clock phase\n"
         "  -O --cpol     clock polarity\n"
         "  -L --lsb      least significant bit first\n"
         "  -C --cs-high  chip select active high\n"
         "  -3 --3wire    SI/SO signals shared\n"
         "  -r --read     read mode\n"
         "  -w --write    write mode\n");
    exit(1);
}

static void parse_opts(int argc, char *argv[])
{
    while (1) {
        static const struct option lopts[] = {
            { "device",  1, 0, 'D' },
            { "speed",   1, 0, 's' },
            { "delay",   1, 0, 'd' },
            { "bpw",     1, 0, 'b' },
            { "loop",    0, 0, 'l' },
            { "cpha",    0, 0, 'H' },
            { "cpol",    0, 0, 'O' },
            { "lsb",     0, 0, 'L' },
            { "cs-high", 0, 0, 'C' },
            { "3wire",   0, 0, '3' },
            { "no-cs",   0, 0, 'N' },
            { "ready",   0, 0, 'R' },
            { "read",    0, 0, 'r' },
            { "write",   0, 0, 'w' },
            { NULL, 0, 0, 0 },
        };
        int c;

        c = getopt_long(argc, argv, "D:s:d:b:lHOLC3NRrw", lopts, NULL);

        if (c == -1)
            break;

        switch (c) {
        case 'D':
            device = optarg;
            break;
        case 's':
            speed = atoi(optarg);
            break;
        case 'd':
            delay = atoi(optarg);
            break;
        case 'b':
            bits = atoi(optarg);
            break;
        case 'l':
            mode |= SPI_LOOP;
            break;
        case 'H':
            mode |= SPI_CPHA;
            break;
        case 'O':
            mode |= SPI_CPOL;
            break;
        case 'L':
            mode |= SPI_LSB_FIRST;
            break;
        case 'C':
            mode |= SPI_CS_HIGH;
            break;
        case '3':
            mode |= SPI_3WIRE;
            break;
        case 'N':
            mode |= SPI_NO_CS;
            break;
        case 'R':
            mode |= SPI_READY;
            break;
        case 'r':
            read_mode = true;
            break;
        case 'w':
            write_mode = true;
            break;
        default:
            print_usage(argv[0]);
            break;
        }
    }

    if (2 != (argc - optind))
    {
        pabort("must specify {ADDRESS NUM | ADDRESS VALUE}");
    }

    address = atoi(argv[optind]);
    count_or_value = atoi(argv[optind+1]);
}

int main(int argc, char *argv[])
{
    int ret = 0;
    int fd;

    parse_opts(argc, argv);

    fd = open(device, O_RDWR);
    if (fd < 0)
        pabort("can't open device");

    /*
     * spi mode
     */
    ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
    if (ret == -1)
        pabort("can't set spi mode");

    ret = ioctl(fd, SPI_IOC_RD_MODE, &mode);
    if (ret == -1)
        pabort("can't get spi mode");

    /*
     * bits per word
     */
    ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    if (ret == -1)
        pabort("can't set bits per word");

    ret = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
    if (ret == -1)
        pabort("can't get bits per word");

    /*
     * max speed hz
     */
    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret == -1)
        pabort("can't set max speed hz");

    ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
    if (ret == -1)
        pabort("can't get max speed hz");

    printf("spi mode: %d\n", mode);
    printf("bits per word: %d\n", bits);
    printf("max speed: %d Hz (%d KHz)\n", speed, speed/1000);

    transfer(fd);

    close(fd);

    return ret;
}

