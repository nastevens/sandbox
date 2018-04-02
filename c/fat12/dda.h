/*
 * dda.h
 * by Charles Lehman
 * #define's for porting Andy's FAT project between Linux & Windows NT/2k/XP
 *
 * Usage:
 *   #include this file, then use open() or fopen() with the following macros:
 *   DISK_FDD0    First floppy disk (/dev/fd0 or A:)
 *   DISK_FDD1    Second floppy disk
 *   DISK_HDD0    First hard disk (/dev/hda or C:)
 *   DISK_HDD1    Second hard disk
 *   DISK_HDD2    Third hard disk
 *   DISK_HDD3    Fourth hard disk
 *
 * Examples:
 *   FILE *floppy = fopen(DISK_FDD0, "rb");
 *   int ifloppy = open(DISK_FDD0, O_RDWR);
 *
 */

#if !defined(__DDA_H)            //make sure we aren't repeating ourselves...

#if defined(__WIN32__)           //all Win32 compilers should define this macro
#define __DDA_H WINDOWS
#define DISK_FDD0   "\\\\.\\A:"
#define DISK_FDD1   "\\\\.\\B:"
#define DISK_HDD0   "\\\\.\\C:"
#define DISK_HDD1   "\\\\.\\D:"
#define DISK_HDD2   "\\\\.\\E:"
#define DISK_HDD3   "\\\\.\\F:"
#endif //defined(__WIN32__)

#if defined(__GNUC__)            //gcc defines this macro
#define __DDA_H LINUX
#define DISK_FDD0   "/dev/fd0"
#define DISK_FDD1   "/dev/fd1"
#define DISK_HDD0   "/dev/hda"
#define DISK_HDD1   "/dev/hdb"
#define DISK_HDD2   "/dev/hdc"
#define DISK_HDD3   "/dev/hdd"
#endif //defined(__GNUC__)

#if !defined(__DDA_H)            //make sure we identified a platform
#error Cannot determine platform: Please define either __WIN32__ or __GNUC__
#endif //!defined(__DDA_H)

#endif //!defined(__DDA_H)
