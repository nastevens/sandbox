default: Makefile ls.o cat.o mkdir.o rm.o cd.o rmdir.o pwd.o shell.o util.o printBootSector.o printFatEntries.o fatsupport.o df.o touch.o
	gcc -o cat cat.o util.o  fat_support.o
	gcc -o ls ls.o util.o fat_support.o
	gcc -o mkdir mkdir.o util.o fat_support.o
	gcc -o rm rm.o util.o fat_support.o
	gcc -o rmdir rmdir.o util.o fat_support.o
	gcc -o cd cd.o util.o fat_support.o
	gcc -o pwd pwd.o util.o fat_support.o
	gcc -o shell shell.o util.o fat_support.o
	gcc -o df df.o util.o fat_support.o
	gcc -o touch touch.o util.o fat_support.o
	gcc -o printBootSector printBootSector.o fat_support.o
	gcc -o printFatEntries printFatEntries.o fat_support.o
	rm *.o
	@echo
	@echo "Please type ./shell floppyx (where x is a number) to start the shell."
	@echo "Valid commands in shell: ls cat mkdir rm cd rmdir pwd df touch"


ls.o: ls.c err.h util.h
	gcc -c -o ls.o ls.c

cat.o: cat.c err.h util.h
	gcc -c -o cat.o cat.c

mkdir.o: mkdir.c err.h util.h
	gcc -c -o mkdir.o mkdir.c

rm.o: rm.c err.h util.h
	gcc -c -o rm.o rm.c

rmdir.o: rmdir.c err.h util.h
	gcc -c -o rmdir.o rmdir.c

cd.o: cd.c err.h util.h
	gcc -c -o cd.o cd.c

pwd.o: pwd.c err.h util.h
	gcc -c -o pwd.o pwd.c
	
df.o: df.c err.h util.h 
	gcc -c -o df.o df.c

touch.o: touch.c err.h util.h
	gcc -c -o touch.o touch.c
	
shell.o: shell.c err.h util.h
	gcc -c -o shell.o shell.c

util.o: util.c fat_support.c fat_support.h util.h dda.h err.h
	gcc -c -o util.o util.c

printBootSector.o: printBootSector.c 
	gcc -c -o printBootSector.o printBootSector.c

printFatEntries.o: printFatEntries.c 
	gcc -c -o printFatEntries.o printFatEntries.c

fatsupport.o: fat_support.c
	gcc -c -o fat_support.o fat_support.c
	
clean:
	rm printBootSector printFatEntries ls cat mkdir rm shell rmdir cd pwd df touch

.PHONY: clean
