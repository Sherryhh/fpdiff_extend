#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_bessel_zero_Jnu(1, 0.40309273233720366);

	printf("%f\n", out);}