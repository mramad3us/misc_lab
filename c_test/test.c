#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    FILE* f;
    char start[15] = "";
    char end[15] = "";

    f = fopen("toto.txt","r");

    if (!f)
        return 1;

    if (!fgets(start,12,f)) //Get first line
        return 1;

    printf("First line in file : %s",start);
    fseek(f,-9,SEEK_END);

    if (!fgets(end,8,f)) //Get last line
        return 1;

    printf("\nLast line in file : %s",end);

    fclose(f);
    return 0;
}
