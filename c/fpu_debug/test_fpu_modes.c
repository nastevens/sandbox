#include <math.h>
#include <stdint.h>
#include <stdio.h>

void print_double_components(const unsigned char* val)
{
	int exp;

	exp = (int)val[0];
	exp <<= 8;
	exp |= (int)val[1];
	exp >>= 4;
	exp &= 0x07FF;
	exp -= 1023;

	uint64_t mant;
	mant = (uint64_t)val[1] & 0x0F;
	mant = (mant << 8) | val[2];
	mant = (mant << 8) | val[3];
	mant = (mant << 8) | val[4];
	mant = (mant << 8) | val[5];
	mant = (mant << 8) | val[6];
	mant = (mant << 8) | val[7];

	printf("Exp: %d  |  Mant: %llu\n", exp, mant);
}

void raw_double(double* val, unsigned char* result)
{
    unsigned char* idx = (unsigned char*)val;
    int i;

    for(i = 7; i >= 0; i--)
    {
        result[i] = *idx;
        ++idx;
    }
}

void raw_extended(long double* val, unsigned char* result)
{
    unsigned char* idx = (unsigned char*)val;
    int i;

    for(i = 9; i >= 0; i--)
    {
        result[i] = *idx;
        ++idx;
    }
}

void print_raw(const unsigned char* val, size_t n)
{
	int i;
	for(i = 0; i < n; i++)
	{
		printf("%02x ", val[i]);
	}
	printf("\n");
}

void set_fpu (unsigned int mode)
{
    asm ("fldcw %0" : : "m" (*&mode));
}

void fpu_extended_routine()
{
    const size_t szExtended = 10;
    long double a = powl(2,63) + 1;
    long double b = 1.0;
    long double z;
    unsigned char a_raw[szExtended];
    unsigned char b_raw[szExtended];
    unsigned char z_raw[szExtended];

    raw_extended(&a, a_raw);
    printf("a: ");
    print_raw(a_raw, szExtended);

    raw_extended(&b, b_raw);
    printf("b: ");
    print_raw(b_raw, szExtended);

    z = a * b;

    raw_extended(&z, z_raw);
    printf("z: ");
    print_raw(z_raw, szExtended);
}

void fpu_double_routine()
{
    const size_t szDouble = 8;
    double a = pow(2,53) + 1;
    double b = 1.0;
    double z;
    unsigned char a_raw[szDouble];
    unsigned char b_raw[szDouble];
    unsigned char z_raw[szDouble];

    raw_double(&a, a_raw);
    printf("a: ");
    print_raw(a_raw, szDouble);

    raw_double(&b, b_raw);
    printf("b: ");
    print_raw(b_raw, szDouble);

    z = a * b;

    raw_double(&z, z_raw);
    printf("z: ");
    print_raw(z_raw, szDouble);
}	

int main()
{
    printf("\n\n");
    printf("FPU in 64-bit mode, double type\n");
    printf("===============================\n");
    set_fpu(0x137f);
    fpu_double_routine();

    printf("\n\n");
    printf("FPU in 64-bit mode, extended type\n");
    printf("=================================\n");
    set_fpu(0x137f);
    fpu_extended_routine();

    printf("\n\n");
    printf("FPU in 53-bit mode, double type\n");
    printf("===============================\n");
    set_fpu(0x127f);
    fpu_double_routine();

    printf("\n\n");
    printf("FPU in 53-bit mode, extended type\n");
    printf("=================================\n");
    set_fpu(0x127f);
    fpu_extended_routine();
}
