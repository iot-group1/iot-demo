TARGET = ../build-rfidreader-debug/rfidreader
OBJS = uart.o utility.o command.o main.o
CC = gcc
CFLAGS =

$(TARGET): $(OBJS)
	$(CC) -Wall -ggdb $(OBJS) -L. -o $(TARGET)

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

test: $(OBJS)
	$(CC) -Wall -ggdb $(OBJS) -L. -o $(TARGET)

clean:
	rm -f $(OBJS)
	rm -f $(TARGET)
