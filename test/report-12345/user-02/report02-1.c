#include <stdio.h>

int main(void){
  char input;
  printf("Input a character [a-z]: ");
  scanf("%a", &input);
  printf("%d\n", input - 'z');

  return 0;
}
