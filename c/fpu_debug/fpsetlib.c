#ifndef LINUX_BLD
#include <windows.h>
#include <float.h>
#endif

#include <fenv.h>
#include <stdio.h>

#include "fpsetlib.h"

DLL_EXPORT void set_fpu(unsigned int mode)
{
    asm ("fldcw %0" : : "m" (*&mode));
}

DLL_EXPORT unsigned int get_fpu(void)
{
    fenv_t environment;
    fegetenv(&environment);
    return (unsigned int)environment.__control_word;
}

#ifndef LINUX_BLD
BOOL WINAPI DllMain(HANDLE h, ULONG fdwReason, LPVOID lp)
{

    if (fdwReason == DLL_PROCESS_ATTACH)
    {
        printf("|DLLPrAtt|get|%#4x\n", get_fpu());
	printf("|DLLPrAtt|set|0x127f\n");
	set_fpu(0x127f);
    }
    else if (fdwReason == DLL_THREAD_ATTACH)
    {
        printf("|DLLThAtt|get|%#4x\n", get_fpu());
	printf("|DLLThAtt|set|0x127f\n");
	set_fpu(0x127f);
    }
    else if (fdwReason == DLL_PROCESS_DETACH)
    {
        printf("|DLLPrDet|get|%#4x\n", get_fpu());
    }
    else if (fdwReason == DLL_THREAD_DETACH)
    {
        printf("|DLLThDet|get|%#4x\n", get_fpu());
    }
     
    return (BOOL)1;
}
#else
void __attribute__ ((constructor)) so_load(void);
void __attribute__ ((destructor)) so_unload(void);

void so_load(void)
{
	printf("|SOConst |get|%#4x\n", get_fpu());
	printf("|SOConst |set|0x127f\n");
	set_fpu(0x127f);
}

void so_unload(void)
{
	printf("|SODestr |get|%#4x\n", get_fpu());
}
#endif


