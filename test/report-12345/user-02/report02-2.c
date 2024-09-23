#include <stdio.h>

int main(void){
  int num;
  printf("Input an integer (>=0): ");
  scanf("%c", &num);
  printf("%c\n", 'a' + num%('a' - 'z' + 1));

  return 0;
}
