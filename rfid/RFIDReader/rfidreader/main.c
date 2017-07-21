#include <stdio.h>

#include "uart.h"
#include "command.h"
#include "utility.h"

bool initialize_uart(int* uart_fd, char* device_name);

void finalize_uart(int uart_fd);

int main(void)
{
    int uart_fd = -1;
    int index = 0;
    char output[1024];

    if (initialize_uart(&uart_fd, SERIAL_DEVICE_NAME)) {
        if (read_single_tag(uart_fd, output, output, sizeof(output))) {
			printf("%s\n", output);

			LOG_DEBUG("READ RFID TAGS SUCCESSFUL!");
        } else {
			LOG_DEBUG("CANNOT OPEN SERIAL PORT [%s]", SERIAL_DEVICE_NAME); 
        }
    }

    finalize_uart(uart_fd);
}

bool initialize_uart(int* uart_fd, char* device_name) {
    bool result = true;

    if (result && !(result &= uart_open(uart_fd, device_name)))
    {
        LOG_DEBUG("FAILED TO OPEN DEVICE [%s].", device_name);
    }

    if (result && !(result &= uart_config(*uart_fd, 115200, 0, 8, 1, 'N')))
    {
        LOG_DEBUG("FAILED TO CONFIGURE DEVICE [%s] WITH PARAMETER 9600 N 8 1.", device_name);
    }

    return result;
}

void finalize_uart(int uart_fd) {
    if (uart_fd > 0)
        uart_close(uart_fd);
}
