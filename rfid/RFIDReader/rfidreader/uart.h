#ifndef UART_H
#define UART_H

#define SERIAL_DEVICE_NAME "/dev/ttyUSB0"

#include "utility.h"

bool uart_open(int* fd, char* port);

bool uart_config(int fd, int speed, int flow_ctrl, int databits, int stopbits, int parity);

void uart_flush_send(int fd);

void uart_flush_receive(int fd);

void uart_flush_both(int fd);

bool uart_send(int fd, char* send_buf, int data_len, int * sent_len);

int uart_receive(int fd, char* rcv_buf, int data_len, int timeout_seconds, int timeout_milliseconds);

void uart_close(int fd);

#endif
