#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_ellint_RC(2.533265554575144, -0.0, GSL_PREC_DOUBLE);

	printf("%f\n", out);}