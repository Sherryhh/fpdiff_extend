#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_ellint_RJ(GSL_NAN, 2.2738632088209076, 1.261714742492535, 0.77675025087889, GSL_PREC_DOUBLE);

	printf("%f\n", out);}