#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_airy_Ai(GSL_POSINF, GSL_PREC_DOUBLE);

	printf("%f\n", out);}