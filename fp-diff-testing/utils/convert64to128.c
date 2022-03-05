/* Program to convert an input from double precision to quad precision*/

#include <stdio.h>
#include <quadmath.h>
#include <stdlib.h>
#include <assert.h>

/* dimensions of the square matrix input */
#ifndef K
#define K 4
#endif

int main(int argc, char *argv[])
{
  assert(argc == 3);

  const char * inName;
  const char *outName;
  double inData[K*K+K];
  __float128 outData[K*K+K];
  int i;

  /* grab infile and outfile names from CL */
  inName = argv[1];
  outName = argv[2];

  /* open infile and outfile */
  FILE * infile = fopen(inName, "r");
  FILE * outfile = fopen(outName, "w");
  assert(infile != NULL && outfile != NULL);

  /* read in data */
  for (i = 0; i < K*K+K; i++){
    double buffer;
    fread(&buffer, sizeof(double), 1, infile);
    inData[i] = buffer;
  }fclose(infile);

  /* convert data to quad precision */
  for (i = 0; i < K*K+K; i++){
    outData[i] = (__float128) inData[i];
  }

  for (i = 0; i < K*K+K; i++){
    printf("double: %.12lf\n",inData[i]);
    printf("quad  : %.12lf\n",(double)outData[i]);
  }

  /* write it back out */
  fwrite(&outData, sizeof(__float128), K*K+K, outfile);
  fclose(outfile);

  return 0;
}