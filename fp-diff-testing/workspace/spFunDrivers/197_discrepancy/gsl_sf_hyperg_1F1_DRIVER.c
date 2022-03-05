#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_hyperg_1F1(2.533265554575144, GSL_POSINF, 1.261714742492535);

	printf("%f\n", out);}