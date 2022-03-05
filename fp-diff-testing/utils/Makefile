CC = gcc
CFLAGS = -Wall -g

default: print64 print128 convert64to128 convert128to64 double_generator

print128: print128.c
	$(CC) $(CFLAGS) print128.c -o print128

print64: print64.c
	$(CC) $(CFLAGS) print64.c -o print64

convert64to128: convert64to128.c
	$(CC) $(CFLAGS) convert64to128.c -o convert64to128

convert128to64: convert128to64.c
	$(CC) $(CFLAGS) convert128to64.c -o convert128to64

double_generator: double_generator.c
	$(CC) $(CFLAGS) double_generator.c -o double_generator

clean:
	rm -f double_generator print64 print128 convert128to64 convert64to128 *.o
