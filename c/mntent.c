#include <stdio.h>
#include <stdlib.h>
#include <mntent.h>

int main(int argc, char *argv[])
{
    struct mntent * ent;
    FILE * file;

    file = setmntent("/etc/mtab", "r");
    if (NULL == file)
    {
        perror("setmntent");
        exit(1);
    }

    while (NULL != (ent = getmntent(file)))
    {
        printf("%s %s\n", ent->mnt_fsname, ent->mnt_dir);
    }

    endmntent(file);

    return 0;
}
