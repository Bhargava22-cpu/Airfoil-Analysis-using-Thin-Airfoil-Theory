"""
Function File: net_circulation.py
------------------------
What it does:
    - Computes the net circulation around the airfoil by integrating the local circulation distribution along the chord.
    - Uses the circulation distribution obtained from thin airfoil theory and evaluates the total bound circulation.
    - Performs numerical integration over the transformed angular coordinate.

Theory Used:
    - Thin Airfoil Theory.
    - The circulation distribution along the airfoil represents the vortex sheet strength.
    - The total circulation around the airfoil is obtained by integrating this vortex sheet strength along the airfoil surface.
    - The coordinate transformation between chordwise coordinate x and angular coordinate theta introduces a Jacobian term, which is accounted for in the numerical integration.

Inputs to net_circ_calc:
    - A : Array of Fourier coefficients obtained from thin airfoil analysis
    - x : Array of chordwise positions along the airfoil
    - dydx : Slope of the camber line with respect to x
    - camber_line : Camber line heights corresponding to x

Other variables:
    - theta : Angular coordinate corresponding to chordwise positions
    - gamma : Circulation distribution along the airfoil
    - net_circ : Total bound circulation around the airfoil
    - integral.simpson : Numerical integration method used to compute the circulation

Outputs:
    - net_circ_calc : Returns the net circulation around the airfoil

Assumptions:
    - Airfoil chord is normalized from x = 0 (leading edge) to x = 1 (trailing edge)
    - Thin airfoil theory assumptions apply (small camber and small angle of attack)
    - Numerical integration using Simpson's rule provides sufficient accuracy for the circulation integral
"""

import numpy as np
from circulation_distribution import circ_dist
import scipy
import scipy.integrate as integral

# Function: net_circ_calc
# Purpose:
# Computes the total (net) circulation around the airfoil by
# numerically integrating the circulation distribution 
# obtained from Thin Airfoil Theory.
def net_circ_calc(A, x, dydx, camber_line):

    # Compute angular coordinate (theta) and circulation distribution (gamma)
    # A : Fourier coefficients defining the circulation distribution
    # x : chordwise coordinate array
    theta , gamma = circ_dist(A, x)

    # Perform numerical integration of the circulation distribution
    # using Simpson's rule to obtain the net circulation.
    # The term sin(theta)/2 comes from the transformation
    # between chordwise coordinate x and angular coordinate theta.
    net_circ = integral.simpson(gamma * np.sin(theta)/2,theta)

    # Adjust sign convention for circulation
    net_circ *=-1

    return net_circ  # Return total circulation around the airfoil
     
    
