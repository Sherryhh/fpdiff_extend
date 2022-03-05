#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_bessel_Kn_scaled(0, -0.0);

	printf("%f\n", out);}