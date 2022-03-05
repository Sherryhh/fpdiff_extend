/* Program to convert an input from quad precision to double precision*/

#include <stdio.h>
#include <quadmath.h>
#include <stdlib.h>
#include <assert.h>

int main(int argc, char *argv[])
{
  assert(argc == 3);

  double outData[100];
  int i;

  /* open infile and outfile */
  FILE * infile = fopen(argv[1], "r");
  FILE * outfile = fopen(argv[2], "w");
  assert(infile != NULL && outfile != NULL);

  __float128 buffer;
  i = 0;
  
  /* read in data */
  while (fread(&buffer, sizeof(__float128), 1, infile) == 1){
    outData[i] = (double)buffer;
    i++;
  }fclose(infile);

  /* write it back out */
  fwrite(&outData, sizeof(__float128), i, outfile);
  fclose(outfile);

  return 0;
}
