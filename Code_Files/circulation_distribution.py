
"""
Function File: circulation_distribution.py
------------------------
What it does:
    - Computes the circulation distribution along the airfoil using the Fourier coefficients obtained from thin airfoil theory.
    - Converts chordwise coordinate x into the angular coordinate theta used in thin airfoil formulation.
    - Computes the vortex sheet strength (circulation distribution) along the airfoil.
    - Plots the circulation distribution as a function of theta.

Theory Used:
    - Thin Airfoil Theory.
    - The circulation distribution along the airfoil is represented using a Fourier series expansion in terms of the angular coordinate theta.
    - The coordinate transformation x = (1 - cos(theta)) / 2 is used to map the chordwise coordinate to the angular coordinate.
    - Fourier coefficients obtained from the camber line slope are used to reconstruct the vortex sheet strength distribution.

Inputs to circ_dist:
    - A : Array containing Fourier coefficients obtained from thin airfoil analysis
    - x : Array of chordwise coordinates along the airfoil
    - U_inf : Freestream velocity (default = 20 m/s)

Inputs to circ_dist_plot:
    - theta : Angular coordinate corresponding to chordwise positions
    - gamma : Circulation distribution along the airfoil

Other variables:
    - theta : Angular coordinate obtained from the thin airfoil coordinate transformation
    - gamma : Circulation distribution (vortex sheet strength) along the airfoil
    - epsilon : Small numerical correction used to avoid singularities at the leading and trailing edges

Outputs:
    - circ_dist : Returns theta and gamma as described above
    - circ_dist_plot : Plot of circulation distribution saved as Circulation_distribution.png

Assumptions:
    - Airfoil chord is normalized from x = 0 (leading edge) to x = 1 (trailing edge)
    - Thin airfoil theory assumptions apply (small camber and small angle of attack)
    - Freestream velocity is constant along the airfoil
    - Small numerical offset is introduced at the endpoints to avoid singularities in tan(theta/2)
"""

import numpy as np
import matplotlib.pyplot as plt

# Function: circ_dist
# Purpose:
# Computes the circulation (vortex sheet strength) distribution
# along the airfoil using the Fourier coefficients obtained
# from Thin Airfoil Theory.
def circ_dist(A, x, U_inf = 20):
    
    epsilon = 1e-6  # Small numerical offset used to avoid singularities at theta = 0 and theta = pi

    # Convert chordwise coordinate x to angular coordinate theta
    # using the standard thin airfoil transformation
    # x = (1 - cos(theta))/2
    theta = np.arccos(1 - 2*x)  # Angular coordinate corresponding to each chordwise position

    # Slightly adjust boundary values to avoid division by zero
    theta[0] = theta[0] + epsilon   # Prevent singularity at leading edge
    theta[-1] = theta[-1] - epsilon # Prevent singularity at trailing edge

    gamma = np.full_like(x, 0)  # Array to store circulation distribution along the airfoil

    # First term of Fourier expansion for circulation distribution
    # Corresponds to A0 term in thin airfoil theory
    gamma += A[0] / np.tan(theta/2)

    # Remaining Fourier terms contributing to circulation
    for i in range (1, len(A)):  # Loop through remaining Fourier coefficients
        gamma += A[i] * np.sin(i * theta)  # Add contribution of each harmonic term

    # Multiply by freestream velocity factor from thin airfoil theory
    gamma = gamma * 2 * U_inf  # Final circulation distribution along the chord

    return theta, gamma  # Return angular coordinate and circulation distribution


# Function: circ_dist_plot
# Purpose:
# Plots the circulation distribution as a function of theta
# and saves the figure.
def circ_dist_plot(theta, gamma):

    plt.figure(figsize= (10,5))  # Create figure for plotting

    # Plot circulation distribution excluding the first point
    # (often removed to avoid numerical spike near theta = 0)
    plt.plot(theta[1:], gamma[1:], label='Circulation Distribution')

    plt.title('Circualtion Distribution as a function of theta')  # Plot title
    plt.xlabel('theta (in radians)')  # Angular coordinate label
    plt.ylabel('Circulation Distribution Gamma (in m/s)')  # Circulation strength label

    plt.grid()  # Add grid for readability
    plt.legend()  # Display legend

    plt.savefig("Circulation_distribution.png")  # Save plot to file
    plt.show()  # Display plot