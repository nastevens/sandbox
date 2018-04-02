/**************************************************************************************
 *
 * Authors of template:  Andy Kinley, Archana Chidanandan, David Mutchler and others.  March, 2004.
 *
 * Author of printBootSector: Lissa Avery, December 16, 2004 
 **************************************************************************************/

#include <stdio.h>
#include <strings.h>
#include "dda.h"
#include "bootSector.h"

#define BYTES_TO_READ_IN_BOOT_SECTOR 13     // 13 is NOT the correct number -- you fix it!

/**************************************************************************************
 * You must set these global variables:
 *    FILE_SYSTEM_ID -- the file id for the file system (here, the floppy disk filesystem)
 *    BYTES_PER_SECTOR -- the number of bytes in each sector of the filesystem
 *
 * You may use these support functions (defined in FatSupport.c)
 *    read_sector
 *    write_sector
 *    get_fat_entry
 *    set_fat_entry
 **************************************************************************************/

FILE* FILE_SYSTEM_ID;
int BYTES_PER_SECTOR;
BootSector bootSector;

extern int read_sector(int sector_number, char* buffer);
extern int write_sector(int sector_number, char* buffer);

extern int  get_fat_entry(int fat_entry_number, char* fat);
extern void set_fat_entry(int fat_entry_number, int value, char* fat);

void ReadBootSector();
void PrintBootSectorValues();

/***********************************************************************************
 * main: an example of reading an item in the boot sector
 ***********************************************************************************/

int main() {
    unsigned char* boot;            // example buffer

    int mostSignificantBits;
    int leastSignificantBits;
    int bytesPerSector;

    // You must set two global variables for the disk access functions:
    //      FILE_SYSTEM_ID         BYTES_PER_SECTOR

//  FILE_SYSTEM_ID = fopen(DISK_FDD0, "r+"); // Use this for the real floppy drive
    FILE_SYSTEM_ID = fopen("floppy1", "r+"); // Use this for an image of a floppy drive

    if (FILE_SYSTEM_ID == NULL) {
        printf("Could not open the floppy drive or image.\n");
        exit(1);
    }

    BYTES_PER_SECTOR = BYTES_TO_READ_IN_BOOT_SECTOR;  // Set it to this only to read the boot sector
                                                      // Then reset it per the value in the boot sector

    boot = (unsigned char*) malloc(BYTES_PER_SECTOR * sizeof(unsigned char));

    if (read_sector(0, boot) == -1) {
        printf("Something has gone wrong -- could not read the boot sector\n");
    }
 
    mostSignificantBits  = ( ( (int) boot[12] ) << 8 ) & 0x0000ff00;  // 12 (not 11) because little endian
    leastSignificantBits =   ( (int) boot[11] )        & 0x000000ff;
    bootSector.bytesPerSector = mostSignificantBits | leastSignificantBits;

    BYTES_PER_SECTOR = bootSector.bytesPerSector;
	
    ReadBootSector(boot);

    PrintBootSectorValues();
}


void ReadBootSector()
{
  unsigned char* boot;

  int sectorNumber;

  int bytesRead;
  int mostSigBit;
  int leastSigBit;

  int counter;

  sectorNumber = 0;

  boot = (unsigned char*) malloc (BYTES_PER_SECTOR * sizeof(unsigned char));

  bytesRead = read_sector(sectorNumber, boot);

  bootSector.sectorsPerCluster = ( (int) boot[13] );

  // Number reserved sectors [14-15]
  mostSigBit  = ( ( (int) boot[15] ) << 8 ) & 0x0000ff00;  
  leastSigBit =   ( (int) boot[14] )        & 0x000000ff;
  bootSector.numberReservedSectors = mostSigBit | leastSigBit;

  bootSector.numberOfFATs = ( (int) boot[16] );

  // root entries [17-18]
  mostSigBit  = ( ( (int) boot[18] ) << 8 ) & 0x0000ff00;  
  leastSigBit =   ( (int) boot[17] )        & 0x000000ff;
  bootSector.maxNumberRootEntries = mostSigBit | leastSigBit;

  // sector count [19-20]
  mostSigBit  = ( ( (int) boot[20] ) << 8 ) & 0x0000ff00; 
  leastSigBit =   ( (int) boot[19] )        & 0x000000ff;
  bootSector.totalSectorCount = mostSigBit | leastSigBit;

  // sectors per fat [22-23]
  mostSigBit  = ( ( (int) boot[23] ) << 8 ) & 0x0000ff00; 
  leastSigBit =   ( (int) boot[22] )        & 0x000000ff;
  bootSector.sectorsPerFAT = mostSigBit | leastSigBit;

  // sectors per track [24-25]
  mostSigBit  = ( ( (int) boot[25] ) << 8 ) & 0x0000ff00;  
  leastSigBit =   ( (int) boot[24] )        & 0x000000ff;
  bootSector.sectorsPerTrack = mostSigBit | leastSigBit;

  // number heads [26-27]
  mostSigBit  = ( ( (int) boot[27] ) << 8 ) & 0x0000ff00;
  leastSigBit =   ( (int) boot[26] )        & 0x000000ff;
  bootSector.numberHeads = mostSigBit | leastSigBit;

  // sector count for FAT 32 [32-35]
  mostSigBit  = ( ( (int) boot[35] ) << 24 ) & 0xff000000;
  leastSigBit = ( ( (int) boot[34] ) << 16 ) & 0x00ff0000;
  mostSigBit = mostSigBit | leastSigBit;
  leastSigBit = ( ( (int) boot[33] ) <<  8 ) & 0x0000ff00;
  mostSigBit = mostSigBit | leastSigBit;
  leastSigBit =   ( (int) boot[32] )         & 0x000000ff;
  bootSector.sectorCountFAT32 = mostSigBit | leastSigBit;

  bootSector.bootSig = ( (int) boot[38] );

  // volume id [39-42]
  mostSigBit  = ( ( (int) boot[42] )   << 24 ) & 0xff000000;
  leastSigBit = ( ( (int) boot[41] ) << 16 ) & 0x00ff0000;
  mostSigBit = mostSigBit | leastSigBit;
  leastSigBit = ( ( (int) boot[40] ) <<  8 ) & 0x0000ff00;
  mostSigBit = mostSigBit | leastSigBit;
  leastSigBit =   ( (int) boot[39] )         & 0x000000ff;
  bootSector.volumeID = mostSigBit | leastSigBit;

  // volume label [43-53]
  for (counter = 0; counter < 11; counter ++)
    {
      bootSector.volumeLabel[counter] = boot[43 + counter];
    }
  bootSector.volumeLabel[11] = '\0';

  // system type [54-61]
  for (counter = 0; counter < 8; counter ++)
    {
      bootSector.fileSysType[counter] = boot[54 + counter];
    }
  bootSector.fileSysType[8] = '\0';

}

void PrintBootSectorValues()
{
  /* 
   * All we need to do here is pring the boot sector values, with care to format nicely.
   */

  printf("Bytes per sector\t\t= %i\n", bootSector.bytesPerSector);
  printf("Sectors per cluster\t\t= %i\n", bootSector.sectorsPerCluster);
  printf("Number of FATs\t\t\t= %i\n", bootSector.numberOfFATs);
  printf("Number of reserved sectors\t= %i\n", bootSector.numberReservedSectors);
  printf("Number of root entries\t\t= %i\n", bootSector.maxNumberRootEntries);
  printf("Total sector count\t\t= %i\n", bootSector.totalSectorCount);
  printf("Sectors per FAT\t\t\t= %i\n", bootSector.sectorsPerFAT);
  printf("Sectors per track\t\t= %i\n", bootSector.sectorsPerTrack);
  printf("Number of heads\t\t\t= %i\n", bootSector.numberHeads);
  printf("Boot signature (in hex)\t\t= %p\n", bootSector.bootSig);
  printf("Volume ID (in hex)\t\t= %p\n", bootSector.volumeID);
  printf("Volume label\t\t\t= %s\n", bootSector.volumeLabel);
  printf("File system type\t\t= %s\n", bootSector.fileSysType);

}





