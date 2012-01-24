#ifndef FPSETLIB_H

#ifndef LINUX_BLD
#define DLL_EXPORT __declspec(dllexport) __cdecl
#else
#define DLL_EXPORT
#endif

DLL_EXPORT void set_fpu(unsigned int mode);
DLL_EXPORT unsigned int get_fpu(void);

#endif
