#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_hyperg_1F1(1.0, 1000000.5, 1001000.5);

	printf("%f\n", out);}