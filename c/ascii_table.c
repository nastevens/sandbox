#include <stdio.h>

main() {
    int i;

    /* Print the ASCII table */
    for (i=30; i<=51; i++) {
        if (i < 32) {
            printf("| %3d %3x %3s\t", i, i, " ");
        } else {
            printf("| %3d %3x %3c\t", i, i, i);
        }

        printf("| %3d %3x %3c\t| %3d %3x %3c\t" , i+51, i+51, i+51, i+102,
                i+102, i+102);

        printf("| %3d %3x %3c\t| %3d %3x %3c\t|\n" , i+153, i+153, i+153,
                i+204, i+204, i+204);
   }

   return(0);
}
