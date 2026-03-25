"""
fourier_cl_cm.py

Computes Fourier coefficients A0, A1, ...., An-1 and  Cl (Lift Coefficient) and Cm (Moment Coefficient about leading edge).

Inputs:
    x           -> chordwise 1000 points
    dydx        -> slope dy/dx
    alpha_deg   -> angle of attack (degree)
    n           -> number of Fourier terms

Outputs:
    A          ->  Array containing first n Fourier coefficients
    Cl         -> Lift coefficient
    Cm         -> Moment coefficient about leading edge

Theory Used:
    Standard thin airfoil theory transformation:
    x = (1 - cos(theta)) / 2
"""
import numpy as np
import scipy
import scipy.integrate as integral

# Function: fourier_coeff
# Purpose:
# Computes the Fourier coefficients of the vortex sheet strength
# distribution used in Thin Airfoil Theory. These coefficients are
# used to determine circulation distribution, lift coefficient (Cl),
# and pitching moment coefficient (Cm).
def fourier_coeff(x, dydx, alpha_deg, n):

    alpha_rad = alpha_deg*np.pi/180  # Convert angle of attack from degrees to radians

    theta = np.arccos(1 - 2*x)  # Transform chordwise coordinate x into angular coordinate theta

    A = np.zeros(n)  # Array to store the first n Fourier coefficients

    # Compute zeroth Fourier coefficient (A0)
    # This term represents the baseline circulation contribution
    # including the effect of angle of attack and camber slope.
    A[0] = alpha_rad - 1/np.pi * integral.simpson(dydx, theta)

    # Compute higher-order Fourier coefficients (A1, A2, ..., An)
    # These coefficients capture the influence of camber slope
    # variations along the airfoil.
    for i in range(1,n):
        A[i] = 2/np.pi * integral.simpson(dydx * np.cos(i * theta), theta)

    # Compute lift coefficient using Thin Airfoil Theory relation
    # Cl = π(2A0 + A1)
    Cl = np.pi * (2 * A[0] + A[1])

    # Compute pitching moment coefficient about the leading edge
    # using Thin Airfoil Theory relation.
    Cm = - np.pi/2 * (A[0] + A[1] - A[2]/2)

    return A, Cl, Cm  # Return Fourier coefficients, lift coefficient, and moment coefficient