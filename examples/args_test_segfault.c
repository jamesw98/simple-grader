#include <stdio.h>
#include <signal.h>

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Invalid usage");
        return 1;
    }

    FILE* file = fopen(argv[1], "r");
    char buff[512];
    
    int i = 0;
    while(fgets(buff, sizeof buff, file) != NULL) {
        
        printf("%s", buff);

        if (i++ == 8) {
            raise(SIGSEGV);
        }
    }

    return 0;
}