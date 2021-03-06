import numpy as np
import sto
import gto
import time

verbose = False
MAXITER = 40  # Maximum SCF iterations
E_conv = 1.0e-6  # Energy convergence criterion


def run_hf(fs, Z):
    """
    Run restricted hartree fock for a single atom.

    INPUT:
        fs: basis functions
        Z: nuclear charge of the atom
    """
    # num of electron = nuclear charege (since it's atom)
    N = Z
    start = time.time()

    # initialization
    H = sto.H_matrix(fs, Z)
    S = sto.S_matrix(fs)
    e, Co = sto.secular_eqn(H, S)
    P = sto.P_matrix(Co, N)
    hf_e = sto.energy_tot(e, P, H)

    stop = time.time()
    print('------------------------------', "Initialization", '------------------------------')
    print('-------------------------', "Ignore repulsion integral", '------------------------')
    sto.print_info(e, Co, hf_e, start, stop, verbose=verbose)
    print('-----------', "Caculating Electron Repulsion Integral (takes time)", '------------')
    R = sto.R_matrix(fs)
    delta_e = 1
    ITER = 0
    previous_e = hf_e

    # Iterations
    while(delta_e > E_conv and ITER < MAXITER):
        print('------------------------------', "Iteration", ITER + 1, '------------------------------')
        start = time.time()

        # important scf steps
        G = sto.G_matrix(P, R)
        F = H + G
        e, Co = sto.secular_eqn(F, S)
        P = sto.P_matrix(Co, N)
        hf_e = sto.energy_tot(e, P, H)

        delta_e = np.abs(hf_e - previous_e)
        previous_e = hf_e
        ITER += 1
        stop = time.time()
        sto.print_info(e, Co, hf_e, start, stop, delta_e, verbose)

    return hf_e


def test1():
    """
    Test of He (1s)
    """
    # Use 2 Slator Type ourbital to represent Helium 1s orbital.
    # The final Helium 1s orbital is a linear combination of these two STO.
    f1s_1 = sto.STO(zeta=1.45363, n=1)
    f1s_2 = sto.STO(zeta=2.91093, n=1)

    # all basis functions
    fs = [f1s_1, f1s_2]

    #  nuclear charge of He
    Z = 2

    # run hartree fock
    hf_e = run_hf(fs, Z)

    # compare result with reference
    ref_hf_e = -2.8616726
    sto.compare(hf_e, ref_hf_e)


def test2():
    """
    Test of Be (1s, 2s)
    """
    # Use 2 STO to represent Be 1s orbital and another 2 STO for 2s orbital
    # The final 1s orbital is a linear combination of these 4 STO.
    # Same for 2s orbital.
    f1s_1 = sto.STO(zeta=5.59108, n=1)
    f1s_2 = sto.STO(zeta=3.35538, n=1)
    f2s_1 = sto.STO(zeta=1.01122, n=2)
    f2s_2 = sto.STO(zeta=0.61000, n=2)

    # all basis functions
    fs = [f1s_1, f1s_2, f2s_1, f2s_2]

    # nuclear charge of Be
    Z = 4

    # run hartree fock
    hf_e = run_hf(fs, Z)

    # compare result with reference
    ref_hf_e = -14.572369
    sto.compare(hf_e, ref_hf_e)


def test3():
    """
    Test of He (1s)
    """
    # Use 2 Slator Type ourbital to represent Helium 1s orbital.
    # The final Helium 1s orbital is a linear combination of these two STO.
    f1s_1 = gto.CGF(zeta=1.45363, n=1, coordinates=[0, 0, 0]).cgf
    f1s_2 = gto.CGF(zeta=2.91093, n=1, coordinates=[0, 0, 0]).cgf

    # all basis functions
    fs = [f1s_1, f1s_2]

    #  nuclear charge of He
    Z = 2

    # run hartree fock
    hf_e = run_hf(fs, Z)

    # compare result with reference
    ref_hf_e = -2.8616726
    sto.compare(hf_e, ref_hf_e)


if __name__ == "__main__":
    test1()
    # test2()
    test3()
