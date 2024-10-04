#include <stdio.h>

int main(void){
  int num;
  printf("Input an integer (>=0): ");
  scanf("%d", &num);
  printf("%c\n", 'a' + num%('z' - 'a' + 1));

  return 0;
}
