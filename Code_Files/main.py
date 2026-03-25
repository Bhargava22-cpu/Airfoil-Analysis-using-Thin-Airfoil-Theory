"""
Function File: main.py
------------------------
What it does:
    - Serves as the main driver script that executes the complete thin airfoil analysis workflow.
    - Calls different modules to compute the camber line, camber slope, Fourier coefficients, circulation distribution,
      velocity field around the airfoil, and total circulation.

Procedure / Flow of the Program:
    1. User-defined airfoil parameters and angle of attack are imported from the input file.
    2. The camber line of the airfoil is computed and plotted.
    3. The slope of the camber line is computed and plotted.
    4. Fourier coefficients are calculated using thin airfoil theory to determine the aerodynamic properties.
    5. Lift coefficient and moment coefficient about the leading edge are computed and displayed.
    6. A higher-order Fourier expansion is used to obtain a smooth circulation distribution along the airfoil.
    7. The circulation distribution is computed and plotted.
    8. Total circulation around the airfoil is calculated by integrating the circulation distribution.
    9. The velocity field around the airfoil is computed using the Biot–Savart law and visualized.
    10. Circulation is independently computed by performing a line integral of the velocity around a closed contour.
    11. The two circulation values are printed to verify consistency with theoretical expectations.

Theory Used:
    - Thin Airfoil Theory for aerodynamic coefficient and circulation distribution computation.
    - Fourier series representation of vortex sheet strength along the airfoil.
    - Biot–Savart law to compute induced velocity due to vortex elements.
    - Circulation theorem where circulation can be obtained either from vortex strength distribution
      or from the line integral of velocity around a closed contour.

Outputs:
    - Camber line plot
    - Camber slope plot
    - Circulation distribution plot
    - Velocity field visualization
    - Printed values of Fourier coefficients, lift coefficient, moment coefficient,
      and circulation computed using two independent methods.

Assumptions:
    - Thin airfoil theory assumptions apply.
    - Flow is inviscid, incompressible, and steady.
    - Airfoil chord is normalized between leading edge (x = 0) and trailing edge (x = 1).
"""

from camber_line import plot_camber_line, compute_camber_line
from camber_slope import plot_camber_slope, compute_camber_slope
from user_input import m, p, input_type, alpha_deg, user_defined_camber
from fourier_cl_cm import fourier_coeff
from circulation_distribution import circ_dist, circ_dist_plot
from net_circulation import net_circ_calc
from velocity_vector_field import velocity_plot, compute_circ

# Compute camber slope
x, dydx = compute_camber_slope(m, p, input_type, user_defined_camber)

# x : chordwise locations along airfoil (0 to 1)
# dydx : slope of camber line (dy/dx) at each x location

# Compute camber line coordinates

xdash, camber_line = compute_camber_line(m, p, input_type, user_defined_camber)

# xdash : chordwise coordinate used for camber line plotting
# camber_line : vertical coordinate of camber line at each x location

# Plot geometry results


plot_camber_line(m, p, input_type, user_defined_camber)
# plots camber line shape of the airfoil

plot_camber_slope(m, p, input_type, user_defined_camber)
# plots slope of camber line vs chord location


# Fourier series solution using few coefficients

A, Cl, Cm = fourier_coeff(x, dydx, alpha_deg, 3)

# A : array containing Fourier coefficients [A0, A1, A2]
# Cl : lift coefficient computed from thin airfoil theory
# Cm : moment coefficient about the leading edge

print("First Fourier Coefficent A0 =", A[0])
print("Second Fourier Coefficent A1 =", A[1])
print("Third Fourier Coefficent A2 =", A[2])

print("Lift Coefficient Cl =", Cl)
print("Coefficient of Moment about leading edge Cm =", Cm)

# Fourier solution using many coefficients for circulation

A_for_circ, Cldash, Cmdash = fourier_coeff(x, dydx, alpha_deg, 100)

# A_for_circ : Fourier coefficients using higher number of terms
# Cldash : lift coefficient recomputed using many Fourier terms
# Cmdash : moment coefficient recomputed using many Fourier terms

# Circulation distribution along airfoil

theta, gamma = circ_dist(A_for_circ, x)

# theta : transformed coordinate used in thin airfoil theory
# gamma : circulation distribution along the airfoil surface


circ_dist_plot(theta, gamma)
# plots circulation distribution vs theta

# Net circulation from integrating gamma

net_circ = net_circ_calc(A_for_circ, x, dydx, camber_line)

# net_circ : total circulation obtained by integrating circulation distribution

print("Total Circulation through integration of circulation distributuion=", net_circ,"m^2/s")


 
# Velocity field method

velocity_plot()
# plots velocity vector field around the airfoil

print("Total Circulation through line integration of velocity =", compute_circ(), "m^2/s")

# compute_circ() : calculates circulation using line integral of velocity around a closed loop