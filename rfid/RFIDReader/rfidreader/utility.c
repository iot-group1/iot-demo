#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 
#include <string.h>

#include "utility.h"

char* str_trim_start(char* value) {
    while(*value != '\0' && (*value == ' ' || *value == '\t' || *value == '\n' || *value == '\r')) value++;

    return value;
}

void str_trim_end(char* value) {
    char* p_value = value;

    while (*(p_value++) != '\0');

    while(p_value -- != value)
    {
        if (*p_value == '\0' || *p_value == ' ' || *p_value == '\t' || *p_value == '\n' || *p_value == '\r')
            *p_value = '\0';
        else
            break;
    }
}

void http_params_resolve(char* params, char* target, char* action, char* name, char* value) {
    char *p, *param_name, *param_value;
    int len;

    p = params;
    len = strlen(params);

    while(strsep(&p, "&"));

    for (p = params; p < (params + len);) {
        param_value = param_name = p;

        for (p += strlen(p); p < (params + len) && !*p; p++);
 
        param_name = strsep(&param_value, "=");

        if (strcmp(param_name, "target") == 0) {
            strcpy(target, param_value);
        } else if (strcmp(param_name, "action") == 0) {
            strcpy(action, param_value);
        }  else if (strcmp(param_name, "name") == 0) {
            strcpy(name, param_value);
        }  else if (strcmp(param_name, "value") == 0) {
            strcpy(value, param_value);
        } 
    }
}

bool uart_receive_till_mark(
    int uart_fd,
    char* content,
    int content_size,
    char* mark,
    int compare_method,
    int timeout_seconds,
    int retries,
    int* received_size)
{
    bool result = true; 
    char buffer_receive[1024];
    int buffer_index = 0;
    int buffer_received_size = 0;

    uart_flush_both(uart_fd);

    *received_size = 0;

    do 
    {
        memset(buffer_receive, 0, sizeof(buffer_receive));

        buffer_received_size = uart_receive(uart_fd, buffer_receive, sizeof(buffer_receive), timeout_seconds, 0);

	if (buffer_received_size >= 0) {
	    *received_size += buffer_received_size;
	}

        if (buffer_received_size > 0)
        {
	    memcpy(content + buffer_index, buffer_receive, buffer_received_size);

            buffer_index += buffer_received_size;

            if (buffer_index >= content_size)
            {
                buffer_index = 0;

		return false;
            }
        }
        else
        {
            LOG_DEBUG("NO MORE DATA RECEIVED BEFORE TIMEOUT");

	    break;
        }
    } while (buffer_received_size > 0);

    LOG_DEBUG("RECEIVED BYTES: %d", *received_size);

lbl_cleanup:
    return result;
}
  
int url_decode(char *url)
{
    int i = 0;

    while(*(url + i))
    {  
        if ((*url = *(url + i)) == '%')
        {  
            *url = *(url + i + 1) >= 'A' ? ((*(url + i + 1) & 0XDF) - 'A') + 10 : (*(url + i + 1) - '0');
            *url = (*url) * 16;
            *url += *(url + i + 2) >= 'A' ? ((*(url + i + 2) & 0XDF) - 'A') + 10 : (*(url + i + 2) - '0');
            i += 2;
        }  
        else if (*(url + i)=='+')
        {
            *url = ' ';
        }
        url ++;
    }

    *url = '\0';
}

