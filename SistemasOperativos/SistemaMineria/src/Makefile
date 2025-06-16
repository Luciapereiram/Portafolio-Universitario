CC = gcc
CFLAGS = -Wall -g -Wextra -pedantic -ansi
LIBS = -lm -lpthread -lrt
OBJECTS = miner.o monitor.o pow.o utils.o

.PHONY: all clean

all: miner monitor

miner: miner.o pow.o utils.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

monitor: monitor.o pow.o utils.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

%.o: %.c %.h
	$(CC) $(CFLAGS) -c $< -o $@	

clean: 
	rm $(OBJECTS) miner monitor *.log
