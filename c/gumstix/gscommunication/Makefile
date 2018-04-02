#Uncomment to compile for ARM
GCC=arm-linux-gcc
STRIP=arm-linux-strip
PREFIX=src

#Uncomment to compile for x86
#GCC=gcc
#STRIP=strip

default:
	make gscomd gscomtest
	${STRIP} gscomd gscomtest

debug:
	make gscomd gscomtest

gscomd: comdaemon.o uc_comm.o m_convert.o rtc.o Makefile
	${GCC} comdaemon.o uc_comm.o m_convert.o rtc.o -o gscomd

gscomtest: comtest.o uc_comm.o m_convert.o rtc.o Makefile
	${GCC} comtest.o uc_comm.o m_convert.o rtc.o -o gscomtest

comdaemon.o: ${PREFIX}/comdaemon.c Makefile
	${GCC} -c ${PREFIX}/comdaemon.c -o comdaemon.o

comtest.o: ${PREFIX}/comtest.c Makefile
	${GCC} -c ${PREFIX}/comtest.c -o comtest.o

uc_comm.o: ${PREFIX}/uc_comm.c ${PREFIX}/uc_comm.h Makefile
	${GCC} -c ${PREFIX}/uc_comm.c -o uc_comm.o

m_convert.o: ${PREFIX}/m_convert.c ${PREFIX}/m_convert.h Makefile
	${GCC} -c ${PREFIX}/m_convert.c -o m_convert.o

rtc.o: ${PREFIX}/rtc.c ${PREFIX}/rtc.h Makefile
	${GCC} -c ${PREFIX}/rtc.c -o rtc.o

clean:
	rm -f *.o core gscomd gscomtest

.PHONY: all clean
