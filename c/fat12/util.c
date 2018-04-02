/* CSSE332 FAT12 Implementation - util.c
 * Contains various functions that handle the low-level accessing of files
 * and directories within a FAT12 filesystem.
 * 
 * Functions in this file can be accessed by including util.h in
 * other functions and then compiling with util.c.  Function 
 * prototypes are also included in util.h.
 */


/* Standard libraries */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <errno.h>

/* User includes */
#include "util.h"
#include "fat_support.h"
#include "dda.h"
#include "err.h"

/* Global variables */
struct shared_info* sinfo;
int    BYTES_PER_SECTOR = 512;
FILE*  FILE_SYSTEM_ID;
FILE*  gstream;

/* Global variables for opening and reading files */
static int file_open;
static int file_seek;
static int file_FLC;




/* Called to initialize util.c's connection to the floppy
 * drive or floppy image through file pointer stored in 
 * shared memory
 */
void init_util()
{
  int shm_id;
  
  shm_id = shmget(SHM_KEY, sizeof(struct shared_info), 0666);
  sinfo = (struct shared_info*)shmat(shm_id, NULL, 0);
  gstream = fdopen(sinfo->stream, "r+");
  FILE_SYSTEM_ID = gstream;
}




/* Called when the caller of util.c is about to exit.  
   Detatches util.c from the shared memory */
void kill_util()
{
  shmdt(sinfo);
}




/* Given a buffer long enough to store a full absolute path
   (i.e. 260 characters in our implementation), and a relative 
   or absolute pathname, concatentates the names to form an 
   absolute path, returned in buffer */
void get_abs_path(char* buffer, char* path)
{
  char   cwd[260];             /* Set hard-coded CWD, otherwise set */ 
  int    cwd_FLC;              /* CWD's FLC */
  
  
  /* Check to see if the path specified is an absolute or relative path.
     Depending on results, either pass path straight through or prepend
     the current working directory to the path */
  if (path[0] != '/')
  {
    get_wd(cwd, &cwd_FLC);
    strcpy(buffer, cwd);
    //if (path[strlen(path)-1] != '/') strcat(path, "/");
    strcat(buffer, path);
  }
  else 
  {
    //if (path[strlen(path)-1] != '/') strcat(path, "/");
    strcpy(buffer, path);
  }

  return;
}




/* Parses the path and returns the FLC of the *directory entry*
 * that contains the file or subdirectory, plus the 
 * index within that directory entry  that denotes
 * the fileinfo for the path 
 *
 * Note that parse_path *DOES NOT* return the FLC of the file
 * or subdirectory itself!  This is because all of the fileinfo
 * for the file or subdirectory is contained in the directory 
 * entry for the parent, not at the FLC of the actual file or
 * subdirectory!
 */
int parse_path (char* path, int* FLC, int* index)
{
  char   **path_tok = NULL;    /* Tokenized path name */
  char   *buffer, *path_buf;   /* Buffers to work with return values */
  char   tmp_buf[12];          /* Buffer for FAT12 filenames */
  int    i, j, pos;            /* Counters for iterations */
  int    mlen = 1;             /* Number of string pointers malloc'ed */
  int    retval;               /* Value returned by parse_path */
  FILE   *stream;              /* File stream */
  int    seek;                 /* Buffer for forming file seek value */
  char   *tmp_name;            /* Name in path_tok we're looking for */
  int    found = 0;            /* Path entries found */
  int    tmp_FLC;              /* Working FLC for recursing from root */
  int    next_FLC;             /* Next FLC when looking at multi-FAT directories */
  char   attrib;               /* File attributes read from dir entry */
  char   found_entry;          /* Flag for when entry is found */
  unsigned char fat[512*9];    /* FAT table memory */
  
  /* Temporary until shared memory set up correctly */
  char   cwd[260];             /* Set hard-coded CWD, otherwise set */ 
  int    cwd_FLC;              /* CWD's FLC */
  get_wd(cwd, &cwd_FLC);
  
  /* The root directory "/" by itself needs a special case, since 
     it will always be FLC 0.  However, it really has no index or 
     fileinfo, so it will return -1 so that other functions can check
     for it and not try and get fileinfo on it */
  if ((strcmp(path, "/") == 0) || (strcmp(path, "") == 0))
  {
    *FLC = 0;
    *index = -1;

    #ifdef DEBUG_CODE
      printf("Pathname passed was ROOT.  FLC will be 0 and index -1\n");
    #endif
    
    return PATH_FOUND;
  }
  
  /* Check to see if the path specified is an absolute or relative path.
     Depending on results, either pass path straight through or prepend
     the current working directory to the path */
  path_buf = (char*)malloc(strlen(path)+strlen(cwd)+1);
  strcpy(path_buf, cwd);
  if (path[0] != '/')
  {
    if (path[strlen(path)-1] != '/') strcat(path_buf, "/");
    strcat(path_buf, path);
  }
  else 
    strcpy(path_buf, path);
  
  /* Convert the path string to all upper case */
  for(i=0; i<strlen(path_buf); i++) 
    path_buf[i] = (char)toupper((char)path_buf[i]);

  #ifdef DEBUG_CODE
    printf("Pathname as passed to parse_path: %s\n", path_buf);
  #endif
  
  /* Tokenize the path using strtok.  Dynamically expand the pointer to
     pointers represented by path_tok, and malloc space for the pathnames
     as needed.  mlen is the total number of entries malloced for path_tok. */
  for (buffer = strtok(path_buf, "/"); buffer != NULL; mlen++)
  {
    path_tok = (char**)realloc(path_tok, mlen*sizeof(char*));
    path_tok[mlen-1] = (char*)malloc(strlen(buffer)+1);
    strcpy(path_tok[mlen-1], buffer);
    buffer = strtok(NULL, "/");
	
    #ifdef DEBUG_CODE
      printf("Tokenized string #%d: |%s|\n", mlen, path_tok[mlen-1]);
    #endif
  } 

  if (mlen == 0) 
  {
    *FLC = 0;
    *index = -1;

    #ifdef DEBUG_CODE
      printf("Pathname passed was ROOT.  FLC will be 0 and index -1\n");
    #endif
    
    return PATH_FOUND;
  }
 
  /* Decrement mlen to remove counter from NULL strtok */
  mlen--;

  /* Check if all the tokenized file names are valid */
  for (i=0; i<mlen; i++)
    if(check_filename(path_tok[i]) == INVALID_FILENAME) return E_INVALID_PATH;
  
  /* Expand all file names into full 11 byte values 
     ***Note*** The expand routine below DEPENDS on valid FAT12 filename! */
  for (i=0; i<mlen; i++)
  {
    /* These special cases for . and .. are needed because the name is 
       tokenized based on the . in the file to get extension */
    if (!strncmp(path_tok[i], "..", 2)) strcpy(path_tok[i], "..         ");
    else if (!strncmp(path_tok[i], ".", 1)) strcpy(path_tok[i], ".          ");

    /* If not . or .., pad with spaces */
    else {
      pos = (int)strcspn(path_tok[i], "."); /* Find relative position of "." */
      strncpy(tmp_buf, path_tok[i], pos);   /* Read filename sans extension */
      tmp_buf[pos]='\0';                    /* Null terminate string */
      for (j=0; j<11-pos; j++)
        strcat(tmp_buf, " ");               /* Pad with spaces */
      for (j=pos+1; j<strlen(path_tok[i]); j++) 
        tmp_buf[j-pos+7] = path_tok[i][j];  /* Move extension to end of name */
      path_tok[i] = realloc(path_tok[i], 12);
      strcpy(path_tok[i], tmp_buf);
    }

    #ifdef DEBUG_CODE
      printf("Padded, tokenized path: |%s|\n", path_tok[i]);
    #endif
  }
  
  /* Open connection to floppy/floppy image */
  stream = gstream;
  
  /* Read the FAT table into memory */
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);

  /* Start looking for first token at root directory */
  tmp_name = path_tok[0];
  tmp_FLC = 0; 
  found_entry = 0;
  
  /* Continue traversing file structure until we've found strings contained
     in str_tok, otherwise break if a string isn't found or the following string
     isn't a directort */
  while (found < mlen)
  {
    /* Special case for seeking in the root directory, which can have 224 entries */
    if((tmp_FLC == 0) || (tmp_FLC == 1))
    {
      /* Loop until we've checked all 224 entries or found entry we're looking for */
      for (j=0; j<224; j++)
      {
        seek = BYTES_PER_SECTOR * 19 + j * 32;
        fseek(stream, seek, SEEK_SET);
        fread(tmp_buf, 11, 1, stream);
        tmp_buf[11]='\0';
        
        if (!strcmp(tmp_buf, tmp_name)) 
        {
          #ifdef DEBUG_CODE
            printf("Matched |%s| in root dir -- index=%d\n", tmp_buf, j);
          #endif
          found++;
          found_entry = 1;
          break;  /* Exit for loop, found entry */
        }
        
        #ifdef DEBUG_CODE
          printf("Root dir search: index=%d -- name_found=|%s| -- search_name=|%s|\n", j, tmp_buf, tmp_name);
        #endif
      }
      
    }

    /* If we're anywhere other than the root directory seek using this code */
    else
    {
      /* Before we enter the next loop, need to preset next_FLC */
      next_FLC = tmp_FLC;

      /* Loops through the directory entry until it finds the entry we're looking for or has
         exhausted all searchable space.  Will traverse multiple FAT entries if the directory 
         entry covers them, by using combination of next_FLC and tmp_FLC. */
      do
      {
        tmp_FLC = next_FLC;
        next_FLC = get_fat_entry(tmp_FLC, fat);
        
        /* Since we're not in the root directory, there are 16 entries per block. 
           Try all 16 entries before moving to the next block in the FAT, or erroring
           with a file not found */
        for (j=0; j<16; j++)
        {
          seek = 512*(tmp_FLC+31)+j*32;
          fseek(stream, seek, SEEK_SET);
          fread(tmp_buf, 11, 1, stream);
          tmp_buf[11]='\0';
          
          /* Compare string read from entry to search string */
          if(!strcmp(tmp_buf, tmp_name))
          {
	    #ifdef DEBUG_CODE
	      printf("Matched |%s| -- index=%d\n", tmp_name, j);
	    #endif
	    found++;
            found_entry = 1;
            break; /* Exit loop: for(j=0..16) */
	  }
          
	  #ifdef DEBUG_CODE
	    printf("index=%d -- name_found=|%s| -- search_name=|%s|\n", j, tmp_buf, tmp_name);
	  #endif
	}
        
        /* There's no need to read additional FAT entries if we found our file */
        if(found_entry) break; 

      } while (next_FLC & 0xFF0 ^ 0xFF0);
      
    } 
    
    /* Special case for . and .. in root directory */
    if ((tmp_FLC == 0 || tmp_FLC == 1) && (tmp_name[0] == '.' || tmp_name[1] == '.'))
    {
      found++;
      found_entry = 1;
      tmp_name = path_tok[found];
      j = -1;
      continue;
    }
    
    /* See if either section (for root directory or otherwise) completed
       without find entry.  If so, then exit with error. */
    if(!found_entry)
    {
      #ifdef DEBUG_CODE
        printf("No match for %s\n", tmp_name);
      #endif
      retval = E_NOTEXIST;
      break; /* Exit loop: while (found < mlem); */
    }

    
    /* So long as we haven't found the full string (found == mlen), adjust
       tmp_FLC to the next FLC to look for the directory entry in.
       Check and make sure that we're not trying to go to a file instead
       of a subdirectory */
    if (found != mlen)
    {
      /* Check and make sure we're not treating a file as a dir */
      if((tmp_FLC == 0) || (tmp_FLC == 1)) seek = 512*19+j*32+11;
      else seek = 512*(tmp_FLC+31)+j*32+11;
      fread(&attrib, 1, 1, stream);
      if (attrib & 0x10 > 0)
      {
        #ifdef DEBUG_CODE
          printf("Trying to treat file %s as a directory!\n", tmp_name);
        #endif
        retval = E_NOTEXIST;
        break;
      }
      
      /* Read the FLC of the next step, and continue looping */
      if((tmp_FLC == 0) || (tmp_FLC == 1)) seek = 512*19+j*32+26;
      else seek = 512*(tmp_FLC+31)+j*32+26;
      fseek(stream, seek, SEEK_SET);
      fread(tmp_buf, 2, 1, stream);
      tmp_name = path_tok[found];
      tmp_FLC = tmp_buf[0]+tmp_buf[1]*256;
    }

    /* Reset found_entry for looking for the next string */
    found_entry = 0;
  
  }
  
  /* If we exited with found==mlen, it means all entries were matched
     and we're okay to return the FLC and the index.  Otherwise the
     return value will take care of not using FLC and index below */
  if (found == mlen)
  { 
    #ifdef DEBUG_CODE
      printf("Found the full matching entry\n");
    #endif
    
    *FLC = tmp_FLC;
    *index = j;
    retval = PATH_FOUND;
  }
  
  /* Free space malloced for path strings */
  for (i=0; i<mlen; i++) free(path_tok[i]);
  free(path_tok);
  free(path_buf);

  /* Return final value */
  return retval;

}




/* Given an FLC and and index of a file, returns the fileinfo
 * associated with that file.  See util.h for more information
 * about the fileinfo structure.
 */
struct fileinfo get_file_info (int FLC, int index)
{
  FILE* stream;             /* File stream to read from */
  char  buffer[32];         /* Buffer of file info */
  char  name_buffer[9];      /* Buffer for copying name info */
  struct fileinfo info;     /* Structure of file info to return */
  int   seek;               /* Buffer for constructing seek length */
  int   len;                /* Length of actual name minus spaces */
  
  /* Mock entry for root directory (FLC:0 index:-1)*/
  if(((FLC == 0) || (FLC == 1)) && (index == -1))
  {
    strcpy(info.filename, "ROOT");
    strcpy(info.ext, "");
    info.attrib = '\x10';
    info.FLC = 0;
    info.fsize = 0;

    return info;
  }
  
  /* Read the fileinfo for the entry from the stream */
  else 
  {
    if ((FLC == 0) || (FLC == 1)) seek = 512*19+32*index;
    else seek = 512*(FLC+31)+32*index;
    stream = gstream;
    fseek(stream, seek, SEEK_SET);
    fread(buffer, 32, 1, stream);
  
    /* Parse the filename and extension */
    strncpy(name_buffer, buffer, 8);
    name_buffer[8] = '\0';
    len=strcspn(name_buffer, " ");
    strncpy(info.filename, name_buffer, len);
    info.filename[len] = '\0';

    strncpy(name_buffer, buffer+8, 3);
    name_buffer[3] = '\0';
    len=strcspn(name_buffer, " ");
    strncpy(info.ext, name_buffer, len);
    info.ext[len] = '\0';
  
    /* Parse the remaining fields */
    info.attrib = buffer[11];
    strncpy(info.ctime, buffer+14, 2);
    strncpy(info.cdate, buffer+16, 2);
    strncpy(info.atime, buffer+18, 2);
    strncpy(info.wtime, buffer+22, 2);
    strncpy(info.wdate, buffer+24, 2);
    info.FLC = (int)(buffer[27]*256+buffer[26]);
    info.fsize = (int)(buffer[31]*256*256*256+buffer[30]*256*256+buffer[29]*256+buffer[28]);
  
    return info;
  }
}




/* Using a fileinfo structure, determines if the file in question is a 
 * file or a subdirectory, and returns a constant indicating the result
 */
int get_file_type (struct fileinfo info)
{
  if(info.attrib & '\x10') return T_SUBDIR;
  else return T_FILE;
}




/* Returns in the array pointed to by list, the directory information 
 * for a given FLC/index pair.  Will view the entire directory, but
 * will only store up to max entries into the list array */
int get_dir_list (struct fileinfo* list, int max, int FLC, int index)
{
  struct fileinfo fibuf;
  int i = 0;
  int base_FLC;
  int lindex = 0;
  int entries = 0;
  int next_FLC = 0;
  unsigned char fat[512*9];    /* FAT table memory */
  FILE* stream;

  /* Open connection to floppy/floppy image */
  stream = gstream;
  
  /* Read the FAT table into memory */
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);
 
  /* Don't need to worry about FAT for root directory */
  if ((FLC == 0) && (index == -1))
  {
    i = 0;
    for (fibuf = get_file_info(FLC, i); (i < 224 && fibuf.filename[0] != '\x00'); i++)
    {
      fibuf = get_file_info(FLC, i);
      if ((fibuf.filename[0] != '\x00') && (fibuf.filename[0] != '\xE5') && (fibuf.attrib != '\x08'))
      {
        if (lindex < max)
        {
          list[lindex] = fibuf;
          lindex++;
        }

        entries++;
      }
    }
  
    return entries;
  }  
  else
  {
    fibuf=get_file_info(FLC, index);
    if (get_file_type(fibuf) == T_FILE) return -1;
    base_FLC = fibuf.FLC;
  }  
  
  /* Since directory entries are added and deleted such that empty 
     spots can be left, we need to iterate over all directory entries,
     or at the very least, until we reach a 0x00.  This code also 
     iterates over all of the FAT entries that the directory uses */
  next_FLC = base_FLC;
  do
  {
    base_FLC = next_FLC;
    next_FLC = get_fat_entry(base_FLC, fat);

    i = 0;
    for (fibuf = get_file_info(base_FLC, i); (i < 16 && fibuf.filename[0] != '\x00'); i++)
    {
      fibuf = get_file_info(base_FLC, i);
      if ((fibuf.filename[0] != '\x00') && (fibuf.filename[0] != '\xE5') && (fibuf.filename[0] != '\x20'))
      {
        if (lindex < max)
        {
          list[lindex] = fibuf;
          lindex++;
        }

        entries++;
      }
    }
    if ((i == 16) && !(next_FLC & 0xFF0 ^ 0xFF0)) 
    {
      return entries;
    }
      

  } while((base_FLC & 0xFF0 ^ 0xFF0));
  
  return entries;
}



/* Sets the working directory in shared memory with the value in path */
void set_wd (char* path, int FLC)
{
  char newpath[260];
  cleanup_path(path, newpath);
  strcpy(sinfo->path, newpath);
  sinfo->FLC = FLC;
}



/* Stores the current working directory in shared memory into the path buffer */
void get_wd (char* path, int* FLC)
{
  strcpy(path, sinfo->path);
  *FLC = sinfo->FLC;
}




/* Returns the number of free blocks on the device.  Works by 
 * iterating over FAT table and counting the number of blocks marked 
 * with 0x00
 */
void get_free_space (long* blocks, int* block_size)
{
  unsigned char fat[512*9];
  FILE* stream;
  int fat_entry, i;
  
  stream = gstream;
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);
  
  *blocks=0;
  *block_size=512;
  for(i=2; i<2849; i++) (*blocks) += (get_fat_entry(i, fat) == 0);
  
}




/* Returns the FLC of a free block that can be used to store 
 * a new file, directory, etc.
 */
int get_free_block (void)
{
  unsigned char fat[512*9];
  int fat_entry, i = 1;
  FILE* stream;
  
  stream = gstream;
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);
  
  /* Iterate through disk umtil free entry found or end of 
     file is reached, indicating a full disk */
  do {
    i++;
    fat_entry = get_fat_entry(i, fat);
  } while ((fat_entry != 0) && (i != 2849));

  if (i == 2849)
  {
    return E_DISKFULL;
  } 
  else
  {
    return i;
  }  
}




/* Given a free block free_FLC and a structure containing file information, allocates
 * memory and a FAT entry for storing data.  If free_FLC is 0 it's assumed that info
 * contains information about an already established FLC (i.e., this could be used to implement
 * the . and .. directory entries).  root_FLC are the directory entries for where
 * the newly allocated entries should be stored.  Note that root_FLC=0 will
 * put the new entry into the root directory.  FLC and index return where the directory entry 
 * was placed
 */
void allocate_block (int free_FLC, struct fileinfo info, int root_FLC, int* FLC, int* index)
{
  unsigned char fat[512*9];
  FILE* stream;
  int i, free_index, seek, next_FLC, found_entry;
  char buffer[32];
  int new_block, dirlen;
  
  stream = gstream;
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);
  
  /* If free_FLC isn't 0, change the info.FLC to the free_FLC */
  if (free_FLC != 0) info.FLC = free_FLC;

  /* Update the FAT table with passed free block */
  set_fat_entry(free_FLC, (int)0xFFF, fat);
  fseek(stream, 512, SEEK_SET);
  fwrite(fat, 512, 9, stream);

  do
  {
    found_entry = 0;
    
    /* Check to see if root_FLC has a free directory entry in it */
    /* Special case for making files in the root directory */
    if((root_FLC == 0) || (root_FLC == 1))
    {
      seek = 512*19;
      dirlen = 124;
    }
    else 
    {
      seek = 512*(root_FLC+31);
      dirlen = 16;
    }
    fseek(stream, seek, SEEK_SET);
    for (i = 0; i < dirlen; i++)
    {
      fread(buffer, 32, 1, stream);
      if(buffer[0] == '\xE5' || buffer[0] == '\x00')
      {
        found_entry = 1;
        break;
      }
    }

    if(found_entry) break;
  
    /* TODO: Have this make a new block instead of returning */
    /* No free entries were found in the first block, check the FAT
       tables to see if the dentry continues at another block */
    if ((i==16) && (found_entry != 1))
    {
      next_FLC = get_fat_entry(root_FLC, fat);

      /* Allocate a new entry block */
      if(!(next_FLC & 0xFF0 ^ 0xFF0))
      {
        new_block = get_free_block();
        seek = 512*(new_block+31);
        fseek(stream, seek, SEEK_SET);
        for(i=0; i<512; i++) fwrite("\0", 1, 1, stream);
        set_fat_entry(root_FLC, new_block, fat);
        set_fat_entry(new_block, 0xFFF, fat);
        root_FLC = new_block;
        found_entry = 1;
        i = 0;
        #ifdef DEBUG_CODE
          printf("Making a new directory entry at FLC %d\n", new_block);
        #endif
      }
    
      /* Continue to next block and try again */
      else 
      {
        root_FLC = next_FLC;
        #ifdef DEBUG_CODE
          printf("Continuing directory entry at FLC %d\n", next_FLC);
        #endif
      }

   }  
  
  if ((i==124) && (found_entry != 1))
  {
    printf("ERROR: Root directory full (Max 124 entries)\n");
    exit(-1);
    //return E_DISKFULL;
  }
     /* Save the free index as found by for loop */
  } while (!found_entry);
  
  
  free_index = i;
  
  #ifdef DEBUG_CODE
    printf("Found a free index at root_FLC index %d\n", free_index);
    printf("allocate_block -- info.filename: %s info.ext: %s\n", info.filename, info.ext);
  #endif
  
  /* Make sure that free_FLC starts as all 0's */
  seek = 512*(free_FLC+31);
  fseek(stream, seek, SEEK_SET);
  for(i=0; i<512; i++) fwrite("\0", 1, 1, stream);

  /* Convert the fileinfo structure to a 32 byte array */
  fileinfo_to_dentry(info, buffer);
 
  /* Seek to the correct location in floppy image to place
     directory entry */
  if((root_FLC == 0) || (root_FLC == 1)) seek = 512*19+32*free_index;
  else seek = 512*(root_FLC+31)+32*free_index;
  fseek(stream, seek, SEEK_SET);
  fwrite(buffer, 32, 1, stream);

  /* Final update of FAT table */
  fseek(stream, 512, SEEK_SET);
  fwrite(fat, 512, 9, stream);

  /* Return the locations where everything actually ended up */
  *FLC = root_FLC;
  *index = free_index;
}



/* Given an FLC and an index, unlinks the entry at the given 
 * location, removing all traces of it from existance, kinda
 */
int unlink_entry (int FLC, int index)
{

  unsigned char fat[512*9];
  FILE* stream;
  int i, seek;
  struct fileinfo info;
  
  /* Open the stream and read the FAT table */
  stream = gstream;
  fseek(stream,512, SEEK_SET);
  fread(fat, 512, 9, stream);
  
  /* Begin by removing the FAT entry */
  info = get_file_info(FLC, index);
  if(info.FLC > 1) set_fat_entry(info.FLC, (int)0x000, fat);
  fseek(stream, 512, SEEK_SET);
  fwrite(fat, 512, 9, stream);

  /* Next remove the directory entry */
  if((FLC == 0) || (FLC == 1)) seek = 512*19 + 32 * index;
  else seek = 512*(FLC+31) + 32 * index;
  fseek(stream, seek, SEEK_SET);
  fwrite("\xE5", 1, 1, stream);

}




/* Opens a file and sets permissions such that only one file
   can be open at a time.  Allows multiple calls to read_file
   to read bytes starting at a seek value */
int open_file(struct fileinfo info)
{
  if (file_open == 1) return -1;
  else
  {
    file_open = 1;
    file_seek = 0;
    file_FLC = info.FLC;
  }
  
}




/* Reads _max_ bytes from the file opened by open_file.  Updates
   seek to indicate where the read left off.  Continues to read
   until it either reaches the maximum number to read or 
   encounters a null character */
/* FIXME: Currently doesn't follow the FAT table for entries */
int read_file (char* buffer, int max)
{
  FILE* stream;
  int seek;
  int numread = 0;
  
  stream = gstream;
  seek = 512*(file_FLC+31) + file_seek;
  fseek(stream, seek, SEEK_SET);
  numread = fread(buffer, 1, max, stream);
  buffer[max] = '\0';
  numread = strcspn(buffer, "\0");
  file_seek += numread;
  #ifdef DEBUG_CODE
    printf("read_file values: seek: %d stream: %d file_seek: %d file_FLC: %d\n", seek, stream, file_seek, file_FLC);
    printf("Read %d bytes\n", numread);
  #endif

  return numread;
}




/* Closes the file opened by open_file, freeing its resources
   and allowing a new file to be opened */
void close_file()
{
  file_open = 0;
  file_seek = 0;
  file_FLC  = 0;
}



/* Given a fileinfo structure, properly converts to a 32 byte
   directory entry.  Buffer should be 32 bytes long */
void fileinfo_to_dentry(struct fileinfo info, char* buffer)
{
  int eos = 0;   /* Flag indicating end of string reached */
  int i;
  
  /* Pad the pathname with spaces and convert to upper case */
  for (i=0; i<8; i++)
  {
    if (info.filename[i] == '\0') eos = 1;
    if (eos == 1) info.filename[i] = ' ';
    else info.filename[i] = (char)toupper((char)info.filename[i]);
    buffer[i] = info.filename[i];
  }

  /* Pad the extension with spaces and convert to upper case */
  eos = 0;
  for (i=0; i<3; i++)
  {
    if (info.ext[i] == '\0') eos = 1;
    if (eos == 1) info.ext[i] = ' ';
    else info.ext[i] = (char)toupper((char)info.ext[i]);
    buffer[i+8] = info.ext[i];
  }

  /* Save the attributes bytes */
  buffer[11] = info.attrib;

  /* Clear reserved bytes */
  buffer[12] = 0;
  buffer[13] = 0;

  /* Store creation and access times */
  for (i=14; i<16; i++) buffer[i] = info.ctime[i-14];
  for (i=16; i<18; i++) buffer[i] = info.cdate[i-16];
  for (i=18; i<20; i++) buffer[i] = info.atime[i-18];
  for (i=22; i<24; i++) buffer[i] = info.wtime[i-22];
  for (i=24; i<26; i++) buffer[i] = info.wdate[i-24];

  /* Parse and store the FLC */
  buffer[26] = (char)(info.FLC & 0x000000FF);
  buffer[27] = (char)((info.FLC & 0x0000FF00) >> 8);

  /* Parse and store the filesize */
  buffer[28] = (char)(info.fsize & 0x000000FF);
  buffer[29] = (char)((info.fsize & 0x0000FF00) >> 8);
  buffer[30] = (char)((info.fsize & 0x00FF0000) >> 16);
  buffer[31] = (char)((info.fsize & 0xFF000000) >> 24);

  /* Done - Return */
  return;
}




/* TODO Valid filename can only contain at most 1 dot */
int check_filename (char* filename)
{

  if(strlen(filename) > 11) return INVALID_FILENAME;
  return VALID_FILENAME;

}



/* Cleans up the path by removing .'s and ..'s */
int cleanup_path(char* path, char* newpath) {

  char* new = newpath;
  int i = 0;
  int count = 0;
  char* dirlist[15];
  char newdir[100];
  if (!strcmp(path, "/"))
  {
    strcpy(newpath, "/");
    return 1;
  }
  strcpy(new, strtok(path, "/"));
  for(i = 0; i < 15; i++) {
    dirlist[i] = NULL;
  }

  i = 0;

  while(new != NULL) {
 
    count++;
   
    if(!strcmp(new, ".")) {
    } else if(!strcmp(new, "..")) {
      if(i == 0) {
	printf("Error: Improper path. Root has no parent directory.");
	return -1;
      }
      i--;
      dirlist[i] = NULL;
    } else {
      dirlist[i] = new;
      i++;
    }

    new = strtok(NULL, "/");

  }

  strcpy(newdir, "/");
  for(i = 0; i < count; i++) {
    if(dirlist[i] != NULL) {
      strcat(newdir, dirlist[i]);
      strcat(newdir, "/");
    }
  }

  strcpy(newpath, newdir);
  return 1;
}
