"""
Function File: camber_slope.py
------------------------
What it does:
    - Computes and plots the slope (dy/dx vs x)of the airfoil (NACA or custom) using numerical differentiation


Inputs to compute_camber_slope and plot_camber_slope:
    - m : maximum camber (as a fraction)
    - p : position of maximum camber (as a fraction)
    - input_type : specifies the type of camber line as NACA(1) or user defined(2)
    - user_defined_camber : If user defined camber is used, this contains the values of the userdefined function at various x.
    - num_points : Used to define the number of points along x axis taken whose corresponding y heights are stored in the variable y

Other variables:
    - x : array of evenly spaced numbers between 0 and 1 (camber x coordiantes)
    - y : heights of the camber-line corresponding to x
    - dydx : stores the values of camber slope at various x

Outputs:
    - compute_camber_slope : returns x and dydx as desribed above.
    - plot_camber_line : Plot of camber slope vs x saved as camber_slope.png

Assumptions:
    - Normalized chord: leading edge at x=0, trailing edge at x=1
    - Numerical differentiation used for slope (works for any camber function)
"""

import numpy as np
import matplotlib.pyplot as plt
from camber_line import compute_camber_line

# Function: compute_camber_slope
# Purpose:
# Computes the slope of the camber line (dy/dx) along the airfoil
# chord using finite difference numerical differentiation.
def compute_camber_slope(m, p, input_type, user_defined_camber, num_points=10000):

    # Obtain camber line coordinates
    x, y = compute_camber_line(m, p, input_type, user_defined_camber, num_points)  
    # x : array of chordwise coordinates along the airfoil
    # y : camber line height values corresponding to each x location

    dydx = np.zeros(num_points)  # Array to store slope (dy/dx) values at each x location

    # Forward difference scheme used to compute slope at the
    # leading edge (first point), since central difference cannot
    # be applied at the boundary.
    dydx[0] = (y[1] - y[0]) / (x[1] - x[0])

    # Central difference scheme used for interior points
    # Provides a more accurate estimate of the derivative
    # using neighbouring points on both sides.
    for i in range(1, num_points - 1):  # Loop over all interior points
        dydx[i] = (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])  # Central difference derivative approximation

    # Backward difference scheme used for the trailing edge
    # because forward/central differences cannot be applied
    # at the final boundary point.
    dydx[-1] = (y[-1] - y[-2]) / (x[-1] - x[-2])
    
    return x, dydx  # Return chordwise locations and corresponding slope values


# Function: plot_camber_slope
# Purpose:
# Generates a plot of the camber line slope (dy/dx) along the
# airfoil chord and saves the resulting figure.
def plot_camber_slope(m, p, input_type, user_defined_camber):

    x, dydx = compute_camber_slope(m, p, input_type, user_defined_camber)
    # x : chordwise coordinate positions
    # dydx : slope of camber line at each x location

    plt.figure(figsize=(10, 4))  # Create a new figure with specified dimensions
    plt.plot(x, dydx, 'r-', linewidth=2, label='dy/dx')  # Plot slope distribution along the chord

    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')  # Draw horizontal reference line at dy/dx = 0

    plt.xlabel('x (in meters)')  # Label for horizontal axis representing chordwise distance
    plt.ylabel('dy/dx')  # Label for vertical axis representing camber slope

    # Set plot title depending on the camber definition used
    if input_type == 1:
        plt.title(f'Camber Line Slope for Normalised Airfoil | Max Camber={m*100:.1f}%, Camber Position={p*100:.1f}%')
    else:
        plt.title('User Defined Camber Slope for Normalsied Airfoil')

    plt.grid(True, linestyle='--', alpha=0.6)  # Add dashed grid lines for easier visual interpretation
    plt.legend()  # Display legend identifying plotted curve
    plt.tight_layout()  # Adjust layout spacing to prevent overlap

    plt.savefig('camber_slope.png', dpi=150)  # Save plot as image file with specified resolution
    plt.show()  # Display the plot