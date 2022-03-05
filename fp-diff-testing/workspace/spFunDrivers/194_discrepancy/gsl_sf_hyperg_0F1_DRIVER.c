#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_hyperg_0F1(-0.0, 2.2738632088209076);

	printf("%f\n", out);}