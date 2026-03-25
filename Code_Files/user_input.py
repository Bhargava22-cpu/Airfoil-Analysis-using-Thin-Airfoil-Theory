"""
Function File: user_input.py
-----------------------------
What it does:
    - Contains all user-defined design details and flight conditions
    - Change values here to simulate different airfoils

Inputs:
    - None (user edits this file directly)

Outputs:
    - Variables used by all other functions

Assumptions:
    - NACA 4-digit airfoil
    - Chord length normalized to 1
"""
# ---------------- INPUT TYPE ----------------
# input_type decides how the camber line will be generated
#
# 1 -> NACA 4-digit airfoil camber line
# 2 -> User-defined camber function y = f(x)

input_type = 1  # Enter the required value here from the legend above.


# ---------------- AIRFOIL SELECTION (used if input_type = 1) ----------------
max_camber_percent = 4.3       # Maximum camber (% of chord)
camber_position_percent = 33.5  # Location of max camber (% of chord)


# ---------------- FLIGHT CONDITION ----------------
alpha_deg = 3     # Angle of attack (degrees)


# ---------------- CONVERSION (do not change) ----------------
m = max_camber_percent / 100   # Maximum camber (decimal)
p = camber_position_percent / 100  # Camber location (decimal)


# ---------------- USER DEFINED FUNCTION (used if input_type = 2) ----------------
# Define your own camber line here.
# The function must take x as input and return y = f(x).
# x will typically be a numpy array of values between 0 and 1.

def user_defined_camber(x):
    """
    Example user-defined camber function.
    Parameters
    ----------
    x : float or numpy array
        chordwise position (0 <= x <= 1)
    Returns
    -------
    y : float or numpy array
        camber value
    """

    import numpy as np
    # Example: sinusoidal camber distribution
    # Replace this RHS with the function f(x) as per requirement.
    y = 0.08 * np.sin(np.pi * x)*(1-x)
    # y = 0.16*x*(1-x)
    # y = 0.3*x*(1-x)**3
    return y
