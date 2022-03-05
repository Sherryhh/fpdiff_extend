#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_lnbeta(GSL_POSINF, 2.2738632088209076);

	printf("%f\n", out);}