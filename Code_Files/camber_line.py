"""
Function File: camber_line.py
------------------------
What it does:
    - Computes and plots the camber line (y vs x) of a airfoil whose camber line function is provided or is a NACA airfoil

Inputs to compute_camber_line and plot_camber_line:
    - m : maximum camber (as a fraction)
    - p : position of maximum camber (as a fraction)
    - input_type : specifies the type of camber line as NACA(1) or user defined(2)
    - user_defined_camber : If user defined camber is used, this contains the values of the userdefined function at various x.
    - num_points : Used to define the number of points along x axis taken whose corresponding y heights are stored in the variable y


Other variables:
    - x : array of evenly spaced numbers between 0 and 1 (camber x coordinates)
    - y : heights of the camber-line corresponding to x
    - max_idx : maximum camber height

Outputs:
    - compute_camber_line : returns x and y as desribed above.
    - plot_camber_line : Plot of camber line saved as camber_line.png

Assumptions:
    - Normalized chord: leading edge at x=0, trailing edge at x=1
    - Numerical differentiation used for slope (works for any camber function)
"""

import numpy as np
import matplotlib.pyplot as plt

# Function: compute_camber_line
# Purpose:
# Computes the camber line coordinates of a normalised airfoil.
# The camber line can either be:
# 1) Standard NACA-type camber line defined by parameters m and p
# 2) A user-defined camber function
def compute_camber_line(m, p, input_type, user_defined_camber, num_points=10000):

    x = np.linspace(0, 1, num_points)  # Array of chordwise positions from leading edge (0) to trailing edge (1)
    y = np.zeros(num_points)           # Array to store camber line vertical coordinates at each x location

    # Case 1: Use standard NACA camber line formulation
    # m = maximum camber (fraction of chord)
    # p = location of maximum camber (fraction of chord)
    if input_type == 1:

        for i in range(len(x)):  # Loop through each chordwise point
            if x[i] <= p:  # Region before maximum camber location
                y[i] = (m / p**2) * (2*p*x[i] - x[i]**2)  # Camber line equation for front section of airfoil
            else:  # Region after maximum camber location
                y[i] = (m / (1-p)**2) * (1 - 2*p + 2*p*x[i] - x[i]**2)  # Camber line equation for rear section of airfoil

    # Case 2: Use user-defined camber line function
    # The function must take x as input and return camber values
    elif input_type == 2:

        y = user_defined_camber(x)  # Evaluate the user-defined camber function over the x array

    # Error handling if invalid input_type is provided
    else:
        raise ValueError("input_type must be 1 or 2")

    return x, y  # Return chordwise positions and corresponding camber line values


# Function: plot_camber_line
# Purpose:
# Generates and displays a plot of the airfoil camber line.
# Also highlights the location of maximum camber on the plot.
def plot_camber_line(m, p, input_type, user_defined_camber):

    x, y = compute_camber_line(m, p, input_type, user_defined_camber)  # Compute camber line coordinates

    plt.figure(figsize=(10, 4))  # Create a new figure with specified size
    plt.plot(x, y, 'b-', linewidth=2, label='Camber Line')  # Plot camber line as a blue curve

    max_idx = np.argmax(y)  # Index of the maximum camber value in the y array

    # Plot a red marker indicating the maximum camber point
    plt.plot(x[max_idx], y[max_idx], 'ro',
             label=f'Max camber at x={x[max_idx]:.3f} m')

    plt.xlabel('x (in meters)')  # Label for horizontal axis representing chordwise distance
    plt.ylabel('y (in meters)')  # Label for vertical axis representing camber height

    # Set plot title depending on camber line type
    if input_type == 1:
        plt.title(f'Camber Line for Normalised Airfoil | Max Camber={m*100:.1f}%, Camber Position={p*100:.1f}%')
    else:
        plt.title('User Defined Camber Line for Normalised Airfoil')

    plt.axis('equal')  # Ensures equal scaling on both axes for accurate geometric representation
    plt.grid(True, linestyle='--', alpha=0.6)  # Add dashed grid lines for readability
    plt.legend()  # Display legend identifying plot elements
    plt.tight_layout()  # Automatically adjust spacing to prevent label overlap

    plt.savefig('camber_line.png', dpi=150)  # Save the plot as an image file with specified resolution
    plt.show()  # Display the plot on screen