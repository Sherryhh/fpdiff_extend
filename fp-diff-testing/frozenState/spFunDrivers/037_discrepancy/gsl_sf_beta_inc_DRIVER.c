#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_beta_inc(0.5, 101.5, 0.999457);

	printf("%f\n", out);}