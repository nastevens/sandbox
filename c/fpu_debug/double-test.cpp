/*
* double-test.cpp
*
* Created on: Sep 6, 2012
* Author: schuringb
*/

#include <iostream>
#include <stdio.h>
#include <math.h>
#include <fenv.h>

double getSig( double value ) {

int temp;
double answer = frexp( value, &temp );

return answer;

}

int getExp( double value ) {

int temp;

frexp( value, &temp );

return temp;

}

long double getLSig( long double value ) {

int temp;
long double answer = frexpl( value, &temp );

return answer;

}

int getLExp( long double value ) {

int temp;

frexpl( value, &temp );

return temp;

}

void set_fpu (unsigned int mode)
{
  asm ("fldcw %0" : : "m" (*&mode));
}


int main()
{

	fenv_t fe_environment;

	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

    set_fpu(0x127f);
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

	double answer;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	double original_val = 169.785;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	long double val = original_val;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	long double powVal=100;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

	long double temp1 = val * powVal;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	long double temp2 = temp1 + .5;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	long double temp3 = floorl(temp2);
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	long double temp4 = temp3/powVal;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);
	double temp5 = (double)temp4;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

	answer = floorl( (val * powVal) + 0.5) / powVal;
	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

	std::cout << "Testing using std::cout." << std::endl;
	std::cout << "d = " << original_val << std::endl;
	std::cout << "ld = " << val << std::endl;
	std::cout << "answer = " << answer << std::endl;

	std::cout << "Testing using printf." << std::endl;
	printf("d = %f\n", original_val);
	printf("ld = %Lf\n", val);
	printf("answer = %f\n", answer);

	fegetenv(&fe_environment);
	printf("CW: %x\n", fe_environment.__control_word);

		

	return 0;
}
