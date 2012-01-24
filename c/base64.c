#include <stdlib.h>
#include <stdio.h>

void print_values(long, char*);

int main()
{
    char *base64;
    long value;

    // Demonstrate long -> base64
    value = 0xDEADBEEF; // 47 59 27 43 30 3 = j v P f S 1
    base64 = l64a(value);
    print_values(value, base64);

    // Demonstrate base64 -> long
    base64 = "abcd";  // 41*64^3 + 40*64^2 + 39*64^1 + 38*64^0 = 10914278
    value = a64l(base64);
    print_values(value, base64);

    printf("%s %d %s\n", __FILE__, __LINE__, __func__);
}

void print_values(long value, char *base64)
{
    printf("Long: %ld\nBase64: %s\n\n", value, base64);
}
