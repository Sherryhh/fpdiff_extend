#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_beta_inc(GSL_NAN, 2.2738632088209076, 1.261714742492535);

	printf("%f\n", out);}