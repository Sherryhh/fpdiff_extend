import scipy.special as sc
import scipy.special.orthogonal as orth
import scipy.special._ufuncs as cephes
import scipy.special as sp
from scipy.special._testutils import FuncData
from scipy.special._testutils import check_version
from scipy.special._testutils import MissingModule
from scipy.special._precompute.expn_asy import generate_A
from scipy.special import lambertw
from scipy.special._ufuncs import _sinpi
from scipy.special._ufuncs import _cospi
from scipy._lib._numpy_compat import suppress_warnings
from scipy.special import logsumexp
from scipy.special import softmax
from scipy.special._mptestutils import Arg
from scipy.special._mptestutils import IntArg
from scipy.special._mptestutils import mp_assert_allclose
from scipy.special._mptestutils import assert_mpmath_equal
from scipy.special._precompute.gammainc_asy import compute_g
from scipy.special._precompute.gammainc_asy import compute_alpha
from scipy.special._precompute.gammainc_asy import compute_d
from scipy.special._precompute.gammainc_data import gammainc
from scipy.special._precompute.gammainc_data import gammaincc
from scipy.special import kolmogorov
from scipy.special import kolmogi
from scipy.special import smirnov
from scipy.special import smirnovi
from scipy.special._ufuncs import _kolmogc
from scipy.special._ufuncs import _kolmogci
from scipy.special._ufuncs import _kolmogp
from scipy.special._ufuncs import _smirnovc
from scipy.special._ufuncs import _smirnovci
from scipy.special._ufuncs import _smirnovp
from scipy._lib.six import with_metaclass
from scipy.special._testutils import assert_func_equal
from scipy.special._mptestutils import FixedArg
from scipy.special._mptestutils import ComplexArg
from scipy.special._mptestutils import nonfunctional_tooslow
from scipy.special._mptestutils import trace_args
from scipy.special._mptestutils import time_limited
from scipy.special._mptestutils import exception_to_nan
from scipy.special._mptestutils import inf_to_nan
from scipy.special._ufuncs import _lgam1p
from scipy.special._ufuncs import _lanczos_sum_expg_scaled
from scipy.special._ufuncs import _log1pmx
from scipy.special._ufuncs import _igam_fac
from scipy import special
from scipy.special import cython_special
from scipy.special import lpn
from scipy.special import lpmn
from scipy.special import lpmv
from scipy.special import lqn
from scipy.special import lqmn
from scipy.special import sph_harm
from scipy.special import eval_legendre
from scipy.special import eval_hermite
from scipy.special import eval_laguerre
from scipy.special import eval_genlaguerre
from scipy.special import binom
from scipy.special import cbrt
from scipy.special import expm1
from scipy.special import log1p
from scipy.special import zeta
from scipy.special import jn
from scipy.special import jv
from scipy.special import yn
from scipy.special import yv
from scipy.special import iv
from scipy.special import kv
from scipy.special import kn
from scipy.special import gamma
from scipy.special import gammaln
from scipy.special import gammainc
from scipy.special import gammaincc
from scipy.special import gammaincinv
from scipy.special import gammainccinv
from scipy.special import digamma
from scipy.special import beta
from scipy.special import betainc
from scipy.special import betaincinv
from scipy.special import poch
from scipy.special import ellipe
from scipy.special import ellipeinc
from scipy.special import ellipk
from scipy.special import ellipkm1
from scipy.special import ellipkinc
from scipy.special import ellipj
from scipy.special import erf
from scipy.special import erfc
from scipy.special import erfinv
from scipy.special import erfcinv
from scipy.special import exp1
from scipy.special import expi
from scipy.special import expn
from scipy.special import bdtrik
from scipy.special import btdtr
from scipy.special import btdtri
from scipy.special import btdtria
from scipy.special import btdtrib
from scipy.special import chndtr
from scipy.special import gdtr
from scipy.special import gdtrc
from scipy.special import gdtrix
from scipy.special import gdtrib
from scipy.special import nbdtrik
from scipy.special import pdtrik
from scipy.special import owens_t
from scipy.special import mathieu_a
from scipy.special import mathieu_b
from scipy.special import mathieu_cem
from scipy.special import mathieu_sem
from scipy.special import mathieu_modcem1
from scipy.special import mathieu_modsem1
from scipy.special import mathieu_modcem2
from scipy.special import mathieu_modsem2
from scipy.special import ellip_harm
from scipy.special import ellip_harm_2
from scipy.special import spherical_jn
from scipy.special import spherical_yn
from scipy.integrate import IntegrationWarning
from scipy.special import loggamma
from scipy._lib.six import xrange
from scipy import integrate
from scipy.special import multigammaln
from scipy.special import boxcox
from scipy.special import boxcox1p
from scipy.special import inv_boxcox
from scipy.special import inv_boxcox1p
from scipy.special._ufuncs import _sf_error_test_function
from scipy.special._testutils import with_special_errors
from scipy._lib._version import NumpyVersion
from scipy.special import logit
from scipy.special import expit
from scipy.special import ellip_normal
from scipy.special._mptestutils import get_args
from scipy.special._mptestutils import mpf2float
from scipy.special import spherical_in
from scipy.special import spherical_kn
from scipy.integrate import quad
from scipy.special._precompute.utils import lagrange_inversion
from scipy.special import _test_round
from scipy.special import spence
import scipy
import numpy as np

print('scipy version: {}'.format(scipy.__version__))
print(special.j1(10000000000.0))

