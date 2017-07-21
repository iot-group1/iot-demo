#ifndef _COMMAND_h
#define _COMMAND_h

#include "utility.h"

struct com_frame {
	unsigned char header;
	unsigned char type;
	unsigned char command;
};

struct tag_frame {
	unsigned char header;
	unsigned char type;
	unsigned char command;
	unsigned char pl;
	unsigned char rssi;
	unsigned char data[14];
	unsigned char crc[2];
	unsigned char checksum;
	unsigned char end;
};

struct err_frame {
	unsigned char header;
	unsigned char type;
	unsigned char command;
	unsigned char pl[2];
	unsigned char parameter;
	unsigned char checksum;
	unsigned char end;
};

bool read_single_tag(int uart_fd, char *value, char *output, int output_size);

#endif


