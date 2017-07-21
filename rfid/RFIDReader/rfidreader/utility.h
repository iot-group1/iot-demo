#ifndef _UTILITY_h
#define _UTILITY_h

#ifdef ENABLE_LOG_DEBUG
#define LOG_DEBUG(...)\
    fprintf(stderr," - ");\
    fprintf(stderr, __VA_ARGS__);\
    fprintf(stderr,"\n");
#else
#define LOG_DEBUG(...) ;
#endif

enum UART_STRING_COMPARE
{
    UART_STRING_COMPARE_FULL_EQU,
    UART_STRING_COMPARE_END_WITH
};

typedef enum __bool {
    false = 0,
    true = 1,
} bool;

void str_trim_end(char* value);

char* str_trim_start(char* value);

void http_params_resolve(char* params, char* target, char* action, char* name, char* value);

bool uart_receive_till_mark(int uart_fd, char* content, int content_size, char* mark, int compare_method, int timeout_seconds, int retries, int* received_size);

int url_decode(char* url);  

#endif

