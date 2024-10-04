#include <stdio.h>

int main(void){
  char input;
  printf("Input a character [a-z]: ");
  scanf("%c", &input);
  printf("%d\n", 'z' - input);

  return 0;
}
