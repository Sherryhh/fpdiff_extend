static double array_x_sf_bessel_J1_0[21] = {
3.831554430727186045e+00,
3.831573373162227014e+00,
3.831592315597267540e+00,
3.831630200467349034e+00,
3.831630200467349034e+00,
3.831668085337430529e+00,
3.831687027772471055e+00,
3.831696498989991539e+00,
3.831701234598751782e+00,
3.831705970207512024e+00,
3.831705970207512024e+00,
3.831708706978431245e+00,
3.831711443749350465e+00,
3.831716917291188462e+00,
3.831727864374864900e+00,
3.831749758542218220e+00,
3.831771652709571541e+00,
3.831793546876924417e+00,
3.831815441044277293e+00,
3.831837335211630613e+00,
3.831859229378983933e+00,
};
static double array_y_sf_bessel_J1_0[21] = {
6.103515624600311580e-05,
5.340562974745081585e-05,
4.577614094978584979e-05,
3.051727646511536387e-05,
3.051727646511536387e-05,
1.525856280941738056e-05,
7.629262547967974575e-06,
3.814626559684327835e-06,
1.907312101294243254e-06,
1.173630282272863872e-16,
1.173630282272863872e-16,
-1.102259807842055794e-06,
-2.204518828512768686e-06,
-4.409034507782940054e-06,
-8.818056418748639475e-06,
-1.763606244837346673e-05,
-2.645401808521502499e-05,
-3.527192332573124271e-05,
-4.408977816673781132e-05,
-5.290758260505043243e-05,
-6.172533663712711919e-05,
};
static double array_e_y_sf_bessel_J1_0[21] = {
5.340562974745081585e-05,
4.577614094978584979e-05,
3.814668985500758129e-05,
3.814668985500758129e-05,
2.288790078246628014e-05,
2.288790078246628014e-05,
1.525856280941738056e-05,
7.629262547967974575e-06,
3.814626559684327835e-06,
1.907312101294243254e-06,
-1.102259807842055794e-06,
-2.204518828512768686e-06,
-4.409034507782940054e-06,
-8.818056418748639475e-06,
-1.763606244837346673e-05,
-2.645401808521502499e-05,
-3.527192332573124271e-05,
-4.408977816673781132e-05,
-5.290758260505043243e-05,
-6.172533663712711919e-05,
-7.054304025942595251e-05,
};
static double array_detla_sf_bessel_J1_0[21] = {
-1.788677319966565508e-16,
-1.788668481357486105e-16,
-1.788659642237738828e-16,
-1.788650802607327128e-16,
-1.788641962466250758e-16,
-1.788633121814517360e-16,
-1.788624280652129401e-16,
-1.788617649461180778e-16,
-1.788614333754002776e-16,
-1.788612123239996248e-16,
-1.788610379218719623e-16,
-1.788609101704343553e-16,
-1.788607185411460729e-16,
-1.788603352751080672e-16,
-1.788595687131866621e-16,
-1.788585465737765219e-16,
-1.788575243661487966e-16,
-1.788565020903044726e-16,
-1.788554797462437468e-16,
-1.788544573339671864e-16,
-1.788534348534760240e-16,
};
static double array_idx_sf_bessel_J1_0[22] = {
0.000000000000000000e+00,
4.265457169600000000e+10,
8.530914339100000000e+10,
1.279637150860000000e+11,
1.706182867820000000e+11,
2.132728584780000000e+11,
2.559274301730000000e+11,
2.985820018680000000e+11,
3.199092877160000000e+11,
3.305729306400000000e+11,
3.412365735640000000e+11,
3.473992338100000000e+11,
3.535618940560000000e+11,
3.658872145470000000e+11,
3.905378555300000000e+11,
4.398391374970000000e+11,
4.891404194640000000e+11,
5.384417014300000000e+11,
5.877429833960000000e+11,
6.370442653630000000e+11,
6.863455473300000000e+11,
7.356468292960000000e+11,
};
static double array_maxE_sf_bessel_J1_0[21] = {
5.253338147579217354e-02,
5.253641668725362451e-02,
5.253945204733246471e-02,
5.254248740494767145e-02,
5.254552261394578039e-02,
5.254855786317794847e-02,
5.255159307217620313e-02,
5.255386947646072116e-02,
5.255500775537531172e-02,
5.255576646319946865e-02,
5.255636506681757997e-02,
5.255680357249151169e-02,
5.255746136780323902e-02,
5.255877696537830657e-02,
5.256140802556232700e-02,
5.256491609922639419e-02,
5.256842417502299164e-02,
5.257193216386985002e-02,
5.257544009403899987e-02,
5.257894813943062018e-02,
5.258245596077575079e-02,
};
double accuracy_improve_patch_of_gsl_sf_bessel_J1_0(double x)
{
 long int n = 735646829297;
 int len_glob = 21;
 double ulp_x = 4.440892098500626e-16;
 double x_0 = 3.831554430727186;
 double compen = 0.0;
 double n_x = ((x-x_0)/ulp_x);
 int idx = floor(n_x*len_glob/n);
 while((idx>=0)&&(idx<len_glob)){
     if((n_x>array_idx_sf_bessel_J1_0[idx])&&(n_x<array_idx_sf_bessel_J1_0[idx+1])){
         compen = ulp_x*ulp_x * (n_x-array_idx_sf_bessel_J1_0[idx+1])*(n_x-array_idx_sf_bessel_J1_0[idx])*array_maxE_sf_bessel_J1_0[idx];
         return (x-array_x_sf_bessel_J1_0[idx])/ulp_x*array_detla_sf_bessel_J1_0[idx]+array_y_sf_bessel_J1_0[idx]+compen;
     }
     else if(n_x<array_idx_sf_bessel_J1_0[idx]){
         idx = idx - 1;
     }
     else if(n_x>array_idx_sf_bessel_J1_0[idx+1]){
         idx = idx + 1;
     }
     else if(x==array_x_sf_bessel_J1_0[idx]){
         return array_y_sf_bessel_J1_0[idx];
     }
     else{
         return array_e_y_sf_bessel_J1_0[idx];
     }
 }
}
double accuracy_improve_patch_of_gsl_sf_bessel_J1(double x)
{
if(x<=3.831881123546337){
 return accuracy_improve_patch_of_gsl_sf_bessel_J1_0(x);
}
}