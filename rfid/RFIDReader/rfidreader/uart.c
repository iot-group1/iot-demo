#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>

#include "uart.h"

bool uart_open(int* fd, char* port)
{
    bool result = false;

    *fd = open(port, O_RDWR | O_NOCTTY | O_NDELAY);
 
    if (-1 == *fd)
    {
        LOG_DEBUG("uart - can not open port [%s].", port);

        result = false;
        goto lbl_cleanup;
    }

    if (fcntl(*fd, F_SETFL, 0) < 0)
    {
        LOG_DEBUG("uart - set port fl to block failed.");

        result = false;
        goto lbl_cleanup;
    }

    /*
    if (0 == isatty(STDIN_FILENO))
    {
        LOG_DEBUG("uart - port is not a terminal device.");

        result = false;
        goto lbl_cleanup;
    }
    */

    result = true;

lbl_cleanup:
    if (!result && *fd > 0)
    {
        close(*fd);
    }
    else if (result)
    {
        LOG_DEBUG("UART - OPEN DEVICE [%s] OK.", port);
    }

    return result;
}

bool uart_config(int fd, int speed, int flow_ctrl, int databits, int stopbits, int parity)
{
    int i, status;
    int speed_arr[] = { B115200, B19200, B9600, B4800, B2400, B1200, B300 };
    int name_arr[] = { 115200,  19200,  9600,  4800,  2400,  1200,  300 };

    struct termios options;

    if (tcgetattr(fd, &options) !=  0)
    {
        LOG_DEBUG("uart - config failed.");

        return false;
    }

    for (i = 0;  i < sizeof(speed_arr) / sizeof(int);  i++)
    {
        if  (speed == name_arr[i])
        {
            cfsetispeed(&options, speed_arr[i]);
            cfsetospeed(&options, speed_arr[i]);
        }
    }

    options.c_cflag |= CLOCAL;
    options.c_cflag |= CREAD;

    switch (flow_ctrl)
    {
    case 0:
        options.c_cflag &= ~CRTSCTS;
        break;
    case 1:
        options.c_cflag |= CRTSCTS;
        break;
    case 2:
        options.c_cflag |= IXON | IXOFF | IXANY;
        break;
    }

    options.c_cflag &= ~CSIZE;

    switch (databits)
    {
    case 5:
        options.c_cflag |= CS5;
        break;
    case 6:
        options.c_cflag |= CS6;
        break;
    case 7:
        options.c_cflag |= CS7;
        break;
    case 8:
        options.c_cflag |= CS8;
        break;
    default:
        LOG_DEBUG("uart - unsupported data size.");
        return false;
    }

    switch (parity)
    {
    case 'n':
    case 'N':
        options.c_cflag &= ~PARENB;
        options.c_iflag &= ~INPCK;
        break;
    case 'o':
    case 'O':
        options.c_cflag |= (PARODD | PARENB);
        options.c_iflag |= INPCK;
        break;
    case 'e':
    case 'E':
        options.c_cflag |= PARENB;
        options.c_cflag &= ~PARODD;
        options.c_iflag |= INPCK;
        break;
    case 's':
    case 'S':
        options.c_cflag &= ~PARENB;
        options.c_cflag &= ~CSTOPB;
        break;
    default:
        LOG_DEBUG("uart - unsupported parity.");
        return false;
    }

    switch (stopbits)
    {
    case 1:
        options.c_cflag &= ~CSTOPB;
        break;
    case 2:
        options.c_cflag |= CSTOPB;
        break;
    default:
        LOG_DEBUG("uart - unsupported stop bits.");
        return false;
    }

    options.c_oflag &= ~OPOST;

    options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    options.c_cc[VTIME] = 1;
    options.c_cc[VMIN] = 1;

    tcflush(fd, TCIFLUSH);

    if (tcsetattr(fd, TCSANOW, &options) != 0)
    {
        LOG_DEBUG("uart - com set error.");
        return false;
    }

    return true;
}

void uart_flush_send(int fd)
{
    tcflush(fd, TCOFLUSH);
}

void uart_flush_receive(int fd)
{
    tcflush(fd, TCIFLUSH);
}

void uart_flush_both(int fd)
{
    tcflush(fd, TCIOFLUSH);
}

int uart_receive(int fd, char* rcv_buf, int data_len, int timeout_seconds, int timeout_milliseconds)
{
    fd_set fs_read;
    int len, fs_sel;
    struct timeval timeout;

    FD_ZERO(&fs_read);
    FD_SET(fd, &fs_read);

    timeout.tv_sec = timeout_seconds;
    timeout.tv_usec = timeout_milliseconds;

    fs_sel = select(fd + 1, &fs_read, NULL, NULL, &timeout);

    if (fs_sel)
    {
        len = read(fd, rcv_buf, data_len);

        return len;
    }
    else
    {
        return -1;
    }
}

bool uart_send(int fd, char* send_buf, int data_len, int* sent_len)
{
    *sent_len = write(fd, send_buf, data_len);

    if (*sent_len != data_len)
    {
        uart_flush_send(fd);

        return false;
    }

    return true;
}

void uart_close(int fd)
{
    close(fd);
}

