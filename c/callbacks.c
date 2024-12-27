#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int (*callback_handler)(void);

struct callback_entry {
  char *text;
  callback_handler handler;
};

int foo_handler(void) {
    printf("Got a 'foo'\n");
    return 1;
}

int bar_handler(void) {
    printf("Got a 'bar'\n");
    return 2;
}

static struct callback_entry CALLBACKS[] = {
    {.text = "foo", .handler = foo_handler},
    {.text = "bar", .handler = bar_handler},
};

#define CALLBACK_LEN (sizeof CALLBACKS / sizeof CALLBACKS[0])

int main(int argc, char *argv[]) {
  if (argc != 2) {
      fprintf(stderr, "Expected one argument\n");
      return EXIT_FAILURE;
  }

  for (int i = 0; i < CALLBACK_LEN; i++) {
      if (0 == strcmp(CALLBACKS[i].text, argv[1])) {
          int retval = (CALLBACKS[i].handler)();
          printf("Return value: %d\n", retval);
          return EXIT_SUCCESS;
      }
  }

  printf("No match for %s\n", argv[1]);
  return EXIT_FAILURE;
}
