int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Invalid usage");
        return 1;
    }

    FILE* file = fopen(argv[1], "r");
    char buff[512];
    
    while(fgets(buff, sizeof buff, file) != NULL) {
        printf("%s", buff);
    }

    return 0;
}