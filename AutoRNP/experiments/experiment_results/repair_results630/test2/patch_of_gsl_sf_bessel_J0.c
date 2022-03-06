static double array_x_sf_bessel_J0_0[17] = {
2.002770881328723647e+02,
2.002771219631023882e+02,
2.002771219631023882e+02,
2.002771388782173858e+02,
2.002771473357748846e+02,
2.002771515645536624e+02,
2.002771536789430229e+02,
2.002771557933324118e+02,
2.002771557933324118e+02,
2.002771578295005384e+02,
2.002771598656686365e+02,
2.002771639380048327e+02,
2.002771720826772821e+02,
2.002771802273497315e+02,
2.002771883720221524e+02,
2.002771971424706408e+02,
2.002772059129191575e+02,
};
static double array_y_sf_bessel_J0_0[17] = {
-3.814697019043062274e-06,
-1.907348349520529999e-06,
-1.907348349520529999e-06,
-9.536741354243614489e-07,
-4.768370584616226285e-07,
-2.384185259140953083e-07,
-1.192092631286772286e-07,
1.159668494172413755e-18,
1.159668494172413755e-18,
1.147991475625698872e-07,
2.295982923539539352e-07,
4.591965784319872897e-07,
9.183931397606204045e-07,
1.377589682354183439e-06,
1.836786204579801324e-06,
2.331263952102846444e-06,
2.825741679395039225e-06,
};
static double array_e_y_sf_bessel_J0_0[17] = {
-2.861022643616909221e-06,
-2.861022643616909221e-06,
-1.430511232455366168e-06,
-1.430511232455366168e-06,
-9.536741354243614489e-07,
-4.768370584616226285e-07,
-2.384185259140953083e-07,
-1.192092631286772286e-07,
1.147991475625698872e-07,
2.295982923539539352e-07,
4.591965784319872897e-07,
9.183931397606204045e-07,
1.377589682354183439e-06,
1.836786204579801324e-06,
2.331263952102846444e-06,
2.825741679395039225e-06,
3.814697068327484574e-06,
};
static double array_detla_sf_bessel_J0_0[17] = {
1.602416297372461889e-15,
1.602416163410157159e-15,
1.602416062651889086e-15,
1.602415995326890199e-15,
1.602415927887275147e-15,
1.602415877235929469e-15,
1.602415851885184166e-15,
1.602415834975136164e-15,
1.602415818370935056e-15,
1.602415802072927943e-15,
1.602415777612631080e-15,
1.602415728645534398e-15,
1.602415663267494909e-15,
1.602415597783163710e-15,
1.602415529669965180e-15,
1.602415458916594351e-15,
1.602415352540029724e-15,
};
static double array_idx_sf_bessel_J0_0[18] = {
0.000000000000000000e+00,
5.951477010000000000e+08,
1.190295401000000000e+09,
1.487869251000000000e+09,
1.785443101000000000e+09,
2.083016951000000000e+09,
2.231803877000000000e+09,
2.306197339000000000e+09,
2.380590802000000000e+09,
2.452232099000000000e+09,
2.523873395000000000e+09,
2.667155987000000000e+09,
2.953721173000000000e+09,
3.240286359000000000e+09,
3.526851544000000000e+09,
3.835434267000000000e+09,
4.144016991000000000e+09,
4.761182439000000000e+09,
};
static double array_maxE_sf_bessel_J0_0[17] = {
-1.390860862035668978e-04,
-1.395629005350359760e-04,
-1.399204990914876766e-04,
-1.401589178651220513e-04,
-1.403973247971564869e-04,
-1.405761310669521088e-04,
-1.406655389271271774e-04,
-1.407251339172707648e-04,
-1.407836341914086274e-04,
-1.408410342713020799e-04,
-1.409271221113430109e-04,
-1.410993149752314154e-04,
-1.413288931862090216e-04,
-1.415584787695973882e-04,
-1.417969014227386402e-04,
-1.420441144923677323e-04,
-1.424149574988598172e-04,
};
double accuracy_improve_patch_of_gsl_sf_bessel_J0_0(double x)
{
 long int n = 4761182440;
 int len_glob = 17;
 double ulp_x = 2.842170943040401e-14;
 double x_0 = 200.27708813287236;
 double compen = 0.0;
 double n_x = ((x-x_0)/ulp_x);
 int idx = floor(n_x*len_glob/n);
 while((idx>=0)&&(idx<len_glob)){
     if((n_x>array_idx_sf_bessel_J0_0[idx])&&(n_x<array_idx_sf_bessel_J0_0[idx+1])){
         compen = ulp_x*ulp_x * (n_x-array_idx_sf_bessel_J0_0[idx+1])*(n_x-array_idx_sf_bessel_J0_0[idx])*array_maxE_sf_bessel_J0_0[idx];
         return (x-array_x_sf_bessel_J0_0[idx])/ulp_x*array_detla_sf_bessel_J0_0[idx]+array_y_sf_bessel_J0_0[idx]+compen;
     }
     else if(n_x<array_idx_sf_bessel_J0_0[idx]){
         idx = idx - 1;
     }
     else if(n_x>array_idx_sf_bessel_J0_0[idx+1]){
         idx = idx + 1;
     }
     else if(x==array_x_sf_bessel_J0_0[idx]){
         return array_y_sf_bessel_J0_0[idx];
     }
     else{
         return array_e_y_sf_bessel_J0_0[idx];
     }
 }
}
double accuracy_improve_patch_of_gsl_sf_bessel_J0(double x)
{
if(x<=200.2772234538162){
 return accuracy_improve_patch_of_gsl_sf_bessel_J0_0(x);
}
}
