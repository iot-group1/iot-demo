#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h>

#include "command.h"
#include "uart.h"
#include "utility.h"

bool read_single_tag(int uart_fd, char *value, char *output, int output_size) {
    bool result = true;
    
    char command[] = { 0xBB, 0x00, 0x22, 0x00, 0x00, 0x22, 0x7E };
    int received_size = 0;
    char *buffer, *pOutput = output;

    if (!(result &= uart_send(uart_fd, command, sizeof(command), &received_size)))
    {
        LOG_DEBUG("[DEBUG] SENDING COMMAND %s TIMEOUT", command);
    }

    uart_flush_send(uart_fd);

    buffer = (char *)malloc(output_size * sizeof(char));
    
    memset(output, 0, output_size);
    memset(buffer, 0, output_size);

    int i = 0, j = 0;

    if (!(result &= uart_receive_till_mark(uart_fd, buffer, output_size, "OK", UART_STRING_COMPARE_END_WITH, 1, 3, &received_size))) {
        LOG_DEBUG("[DEBUG] RECEIVED RESULT TIMEOUT.", output);
    }

    struct com_frame *com_data;
    struct tag_frame *tag_data;
    struct err_frame *err_data;

    for (i = 0; i < received_size; ) {
        if (buffer[i] == 0xBB) {
             com_data = (struct com_frame *) (buffer + i);

             if (com_data->command == 0x22) {
                 tag_data = (struct tag_frame *) com_data;

                 for (j = 0; j < sizeof(tag_data->data); j++) {
                     pOutput += sprintf(pOutput, "%02X ", *(tag_data->data + j));
                 }

                 pOutput += sprintf(pOutput, "\n");

                 i += sizeof(struct tag_frame);
             } else if (com_data->command == 0xFF) {
                 err_data = (struct err_frame *) com_data;

                 pOutput += sprintf(pOutput, "%s\n", "inventory fail");

                 i += sizeof(struct err_frame);
             } else {
                 i += 1;
             }
        }
    }

    *pOutput = '\0';

    free(buffer);

    return result;
}
