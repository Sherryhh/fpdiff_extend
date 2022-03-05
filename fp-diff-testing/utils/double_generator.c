/* Program to generate an input of a specified number of doubles in a specified range
 * */

#include <time.h>
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>
#include <unistd.h>

int main (int argc, const char * argv[])
{
    /* Usage: ./matVec_gen outfile randomSeed numberOfDoubles lower upper */
    assert(argc == 6);

    double buffer;
    int N;
    int seed;
    int i;
    double lower;
    double upper;

    /* grab K and randomSeed from CL, seed number generator */
    seed = atoi(argv[2]);
    N = atoi(argv[3]);
    lower = atof(argv[4]);
    upper = atof(argv[5]);
    srand(seed);

    /* write random doubles to outfile */
    FILE * outfile = fopen(argv[1], "w");
    for (i = 0; i < N; i++) {
      buffer = ( (double)rand() * ( upper - lower ) ) / (double)RAND_MAX + lower;
      fwrite(&buffer, sizeof(double), 1, outfile);
    }fclose(outfile);

    return 0;
}
