/* Programs to print quad precision data to the stdout*/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <quadmath.h>

int main(int argc, char *argv[])
{
  assert(argc == 2);

  __float128 buffer;

  /* open infile */
  FILE * infile = fopen(argv[1], "r");
  if (infile){
    /* read in data */
    while (fread(&buffer, sizeof(__float128), 1, infile) == 1){
      printf("%.10e\n", (double)buffer);
    }fclose(infile);
  }
  return 0;
}