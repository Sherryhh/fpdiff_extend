#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_bessel_Inu_scaled(2.533265554575144, GSL_POSINF);

	printf("%f\n", out);}