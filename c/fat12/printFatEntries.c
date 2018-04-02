/********************************************************************
 * printFatEnries.c v. 0.0
 * NAME: Nicholas Stevens
 * GROUP: Melissa Avery, Jennifer Cain, Kellen Wampler
 * DATE: 12/15/04
 *******************************************************************/

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include "dda.h"
#include "fat_support.h"

/**************************************************************************************
 * You must set these global variables:
 *    FILE_SYSTEM_ID -- the file id for the file system (here, the floppy disk filesystem)
 *    BYTES_PER_SECTOR -- the number of bytes in each sector of the filesystem
 *
 * Define FLOPPY below as desired:
 *    An appropriate file (for testing), or the real floppy drive
 *
 * You may use these support functions (defined in FatSupport.c)
 *    read_sector    write_sector    get_fat_entry    set_fat_entry
 **************************************************************************************/

FILE *FILE_SYSTEM_ID;
int  BYTES_PER_SECTOR;

#define FLOPPY "floppy3"    /* Use any file that simulates a floppy disk */
//#define FLOPPY DISK_FDD0    /* Use this for the real floppy drive */

/******************************************************************** 
 * Main 
 ********************************************************************/
int main(int argc, char** argv) {
  int low, high, i;         /* High and low record values */
  unsigned char *sect;      /* Sector buffer */
  BYTES_PER_SECTOR = 512;

  
  /* Verify command line arguments are correct, read entries */
  if ( ((argc == 3) || (argc == 4))
       && ((low = atoi(argv[1])) <= (high = atoi(argv[2])))
	   && (atoi(argv[2]) < BYTES_PER_SECTOR*9*2/3) ) {

    /* You must set these global variables for the disk access functions */
    FILE_SYSTEM_ID = fopen(argc == 4 ? argv[3] : FLOPPY, "rw");
    
	/* Read the FAT table into memory */
    sect = (char*) malloc(9*BYTES_PER_SECTOR*sizeof(char));

    /* Read the sectors containing the FAT table */
    for (i = 1; i <= 9; i++)
    {    
      read_sector(i, sect+BYTES_PER_SECTOR*(i-1));
    }

	/* Print the fat entries specified */
    for(i = low; i < high; i++)
    {
      printf("Entry %d:\t%X\n", i, get_fat_entry(i, sect));
    } 
	
  } else {
    printf("Usage: %s low high [filename]\n", argv[0]);
	printf("\nUnless [filename] is specified, prints FAT table entries 'low' to 'high\n");
	printf("from file 'floppy1' in current directory.  If [filename] is specified,\n");
	printf("prints from file [filename]\n\nFAT12 max FAT entries: %d\n", BYTES_PER_SECTOR*9*2/3);
    exit(EXIT_SUCCESS);
  }
}
