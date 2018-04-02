#include <stdio.h>
#include "util.h"
#include "err.h"

int main() {
  char path[260];
  int FLC;

  init_util();
  get_wd(path,&FLC);
  printf("%s\n",&path);
  kill_util();
  return 1;
}
  
