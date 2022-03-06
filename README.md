# FPDiff-Extend: Automated Differential Testing for Numerical Libraries
FPDiff-Extend is a tool extends on FPDiff by integrating the floating-point error-inducing inputs from AutoRNP in the step of adversarial input injection.
This project aims at leveraging the high floating-point error detection ability of the original work. 
It includes following parts:
1) Extended version of FPDiff - FPDiff-Extend
2) Original work of AutoRNP with generated results
3) Sample results for references

## Requirements
* Set up environment with docker 
     
     `docker pull ucdavisplse/sp-diff-testing`

### AutoRNP
* python 2.7.14. 

    You can install it by following commands (on Ubuntu):
    
    ```
        sudo add-apt-repository ppa:jonathonf/python-2.7        
        sudo apt-get update        
        sudo apt-get install python2.7
        python --version
     ```

* gsl-2.1 

    Download from the link below and install (on Ubuntu)::


        http://mirrors.ustc.edu.cn/gnu/gsl/
        ./configure | make | make install

* mpfr 3.1.2-1

    Install:
    
        sudo apt-get install libmpfr-dev
    

* pygsl-2.3.0 

    Download from the link below:


        https://sourceforge.net/projects/pygsl/files/pygsl/


* Into the root directory, and run "./autofig.sh" to 
install the required python package (see details in file "requirements.txt") and configure the benchmarks.

* Install pygsl-2.3.0 (on Ubuntu), and note that gsl must be installed before installing pygsl:

```
        python setup.py config
        python setup.py build
        sudo python setup.py install
```
        
### FPDiff
Environment is satisfied with Docker.

## Running
After running docker container: <br>
```
git clone https://github.com/Sherryhh/fpdiff_extend
cd fpdiff_extend
./run.sh
```

