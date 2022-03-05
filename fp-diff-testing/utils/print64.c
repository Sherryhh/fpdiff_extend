/* Programs to print double data to the stdout*/

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int main(int argc, char *argv[])
{
  assert(argc == 2);

  double buffer;

  /* open infile */
  FILE * infile = fopen(argv[1], "r");
  if (infile){
    /* read in data */
    while (fread(&buffer, sizeof(double), 1, infile) == 1){
      printf("%.10e\n", (double)buffer);
    }fclose(infile);
  }
  return 0;
}