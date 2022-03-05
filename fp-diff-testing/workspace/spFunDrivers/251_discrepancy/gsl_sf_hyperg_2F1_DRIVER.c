#include <gsl/gsl_sf.h>
#include <gsl/gsl_errno.h>
#include <stdio.h>

#include <gsl/gsl_math.h>
int main (void){
	double out;
	out = gsl_sf_hyperg_2F1(0.40309273233720366, 2.542301210811698, 2.291323856929842, GSL_NAN);

	printf("%f\n", out);}