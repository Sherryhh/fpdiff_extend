#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_ellint_RC(GSL_POSINF, 2.2738632088209076, GSL_PREC_DOUBLE);

	printf("%f\n", out);}