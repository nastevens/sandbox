/* CSSE332 FAT12 Implementation - util.h
 * Header file containing function prototypes and structures for use
 * in implementing the FAT12 filesystem.  Function definitions are contained
 * in util.c
 */

#include <stdio.h>

#define T_SUBDIR 1
#define T_FILE 0
#define T_FAT12 1
#define T_NFAT12 0
#define SHM_KEY 6543
#define PATH_FOUND 1
#define VALID_FILENAME 1
#define INVALID_FILENAME 0

/* Data Structures */
struct fileinfo {
  char filename[9]; // Stored as null-termed string
  char ext[4];      // " " " " "
  char attrib;
  char ctime[2];
  char cdate[2];
  char atime[2];
  char wtime[2];
  char wdate[2];
  int  FLC;
  int  fsize;
};

struct shared_info {
    char path[260];
    int FLC;
    int stream;
};

/* Function prototypes */
void init_util();
void kill_util();
void get_abs_path(char* buffer, char* path);
int parse_path (char* path, int* FLC, int* index);
int cleanup_path(char* path, char* newpath);
int check_filename (char* filename);
struct fileinfo get_file_info (int FLC, int index);
int get_file_type (struct fileinfo info);
int get_dir_list (struct fileinfo* list, int max, int FLC, int index);
void set_wd (char* path, int FLC);
void get_wd (char* path, int *FLC);
void get_free_space (long* blocks, int* block_size);
int get_free_block (void);
void allocate_block (int free_FLC, struct fileinfo info, int root_FLC, int* FLC, int* index);
void fileinfo_to_dentry(struct fileinfo info, char* buffer);
int unlink_entry (int FLC, int index);
int open_file(struct fileinfo info);
int read_file (char* buffer, int max);
void close_file();


