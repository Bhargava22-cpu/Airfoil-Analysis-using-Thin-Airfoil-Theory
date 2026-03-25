"""
Function File: velocity_vector_field.py
------------------------
What it does:
    - Computes the velocity field around an airfoil using the circulation distribution obtained from thin airfoil theory.
    - Models the airfoil as a continuous vortex sheet whose strength is given by the circulation distribution.
    - Uses the Biot–Savart law to compute the velocity induced by each vortex element at points in the surrounding flow field.
    - Generates a velocity vector field visualization around the airfoil.
    - Allows computation of velocity at any arbitrary point in the flow.
    - Computes circulation around a rectangular control contour.

Theory Used:
    - Thin Airfoil Theory to obtain the vortex sheet strength distribution along the airfoil.
    - Biot–Savart Law to compute the velocity induced at a point due to a vortex element.
    - Coordinate transformation between chordwise coordinate x and angular coordinate theta.
    - Superposition principle where freestream velocity and induced velocity are combined.
    - Circulation computed as the line integral of velocity around a closed contour.

Inputs (from user_input and dependent modules):
    - m : Maximum camber of the airfoil (fraction of chord)
    - p : Position of maximum camber (fraction of chord)
    - input_type : Specifies NACA camber line (1) or user-defined camber (2)
    - user_defined_camber : Function defining the camber line if user-defined option is selected
    - alpha_deg : Angle of attack in degrees

Other variables:
    - x : Chordwise coordinates along the airfoil
    - dydx : Slope of the camber line
    - xi, zi : Coordinates of the camber line
    - theta : Angular coordinate used in thin airfoil theory
    - gamma : Circulation (vortex sheet strength) distribution along the airfoil
    - X, Y : Meshgrid defining the computational grid around the airfoil
    - U, V : Velocity components at grid points
    - speed : Magnitude of velocity at each grid point
    - x_rot, z_rot : Camber line coordinates rotated to represent the airfoil at angle of attack

Functions:
    - velocity_field : Computes velocity components on the entire computational grid due to freestream and vortex sheet.
    - velocity_plot : Generates and saves a vector plot of the velocity field around the airfoil.
    - velocity_point : Computes velocity components at a single specified point.
    - compute_circ : Computes circulation around a rectangular contour using numerical line integration.

Outputs:
    - velocity_plot : Velocity field visualization saved as Velocity_field.png
    - velocity_field : Returns velocity components U and V across the grid
    - velocity_point : Returns velocity components at a specified point
    - compute_circ : Returns circulation around the specified rectangular contour

Assumptions:
    - Airfoil chord is normalized from x = 0 (leading edge) to x = 1 (trailing edge)
    - Thin airfoil theory assumptions apply (small camber and small angle of attack)
    - Flow is incompressible and inviscid
    - Vortex sheet strength represents bound circulation on the airfoil
    - Numerical discretization of the vortex sheet approximates the continuous circulation distribution
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from user_input import m, p, input_type, user_defined_camber, alpha_deg
from camber_line import compute_camber_line
from camber_slope import compute_camber_slope
from fourier_cl_cm import fourier_coeff
from circulation_distribution import circ_dist

 
# Compute camber slope distribution along the airfoil chord
 
x, dydx = compute_camber_slope(m, p, input_type, user_defined_camber)
# x : chordwise coordinate points along the airfoil
# dydx : slope of camber line at each chordwise point

 
# Compute Fourier coefficients and aerodynamic coefficients
 
A_for_circ, Cldash, Cmdash = fourier_coeff(x, dydx, alpha_deg, 100)
# A_for_circ : Fourier coefficients used for circulation distribution
# Cldash : lift coefficient obtained from thin airfoil theory
# Cmdash : moment coefficient obtained from thin airfoil theory

 
# Compute circulation distribution along the airfoil
 
theta, gamma = circ_dist(A_for_circ, x)
# theta : angular coordinate corresponding to chordwise positions
# gamma : vortex sheet strength (circulation distribution)

 
# Define computational grid around the airfoil for velocity field
 
dx = 0.10  # grid spacing in x-direction
dy = 0.10  # grid spacing in y-direction

x_grid = np.arange(-1, 3+dx, dx)  # x-coordinates of grid points
y_grid = np.arange(-1.5, 1.5+dy, dy)  # y-coordinates of grid points

X, Y = np.meshgrid(x_grid, y_grid)  
# X, Y : 2D arrays representing coordinates of grid points

 
# Compute camber line coordinates for plotting
 
xi , zi = compute_camber_line(m, p, input_type, user_defined_camber, num_points=10000)
# xi : chordwise coordinates of camber line
# zi : camber line vertical coordinates

alpha = np.radians(alpha_deg)  # convert angle of attack from degrees to radians

 
# Rotate camber line by angle of attack for visualization
 
x_rot = xi*np.cos(alpha) + zi*np.sin(alpha)  # rotated x-coordinate
z_rot = -xi*np.sin(alpha) + zi*np.cos(alpha) # rotated z-coordinate


 
# Function: velocity_field
# Purpose:
# Computes the velocity field at each grid point induced by
# the airfoil vortex sheet using the Biot-Savart law.
 
def velocity_field(U_inf=20):

    U = np.full_like(X, U_inf)  # initialize x-velocity with freestream velocity
    V = np.full_like(Y, 0)      # initialize y-velocity to zero

    N = len(xi)  # number of discretization points along camber line

    # Loop through each vortex element along the airfoil
    for i in range(len(theta)-1):

        # Coordinates of vortex element after airfoil rotation
        x_i = (1/2)*(1 - np.cos(theta[i]))*np.cos(alpha) + zi[i]*np.sin(alpha)
        y_i = -(1/2)*(1 - np.cos(theta[i]))*np.sin(alpha) + zi[i]*np.cos(alpha)

        dtheta = theta[i+1] - theta[i]  # angular segment size

        # Differential circulation element
        dGamma = gamma[i]*(1/2)*np.sin(theta[i])*dtheta * np.sqrt(1 + dydx[i]**2)

        # Distance squared from vortex element to grid point
        r2 = (X-x_i)**2 + (Y-y_i)**2 + 1e-5  # small term added to avoid singularity

        # Biot-Savart law contribution to velocity
        U += dGamma/(2*np.pi) * (Y-y_i)/r2
        V += -dGamma/(2*np.pi) * (X-x_i)/r2

    return U, V


 
# Compute velocity field across grid
 
U, V = velocity_field(U_inf=20)

speed = np.sqrt(U**2 + V**2) + 1e-8  # velocity magnitude

# Normalized velocity vectors for quiver plotting
U_plot = U / speed
V_plot = V / speed


 
# Function: velocity_plot
# Purpose:
# Visualizes velocity vector field around the airfoil
 
def velocity_plot():

    plt.figure(figsize=(12, 8))

    norm = Normalize(vmin=np.min(speed), vmax=np.max(speed))
    # Normalize velocity magnitude for color scaling

    q = plt.quiver(X, Y, U_plot, V_plot, speed,
               cmap="jet",
               norm=norm,
               width=0.00275,
               scale=45)
    # Quiver plot showing direction and magnitude of velocity vectors

    plt.plot(x_rot, z_rot,color='red',linewidth=2,label="Camber Line")
    # Plot rotated camber line

    plt.colorbar(q, label="Velocity Magnitude (in m/s)")
    plt.xlim(-1, 3)
    plt.ylim(-1.5, 1.5)

    plt.xlabel("x (in meters)")
    plt.ylabel("y (in meters)")
    plt.title("Velocity Field Around the airfoil")

    plt.legend()
    plt.axis('equal')

    plt.savefig("Velocity_field.png", dpi =300)
    plt.show()


 
# Function: velocity_point
# Purpose:
# Computes velocity induced by airfoil at a single point
 
def velocity_point(xp, yp, U_inf=20):

    U = U_inf  # freestream x velocity
    V = 0      # freestream y velocity

    for i in range(len(theta)-1):

        # Coordinates of vortex element
        x_i = (0.5)*(1 - np.cos(theta[i]))*np.cos(alpha) + zi[i]*np.sin(alpha)
        y_i = -(0.5)*(1 - np.cos(theta[i]))*np.sin(alpha) + zi[i]*np.cos(alpha)

        dtheta = theta[i+1] - theta[i]

        # Differential circulation element
        dGamma = gamma[i] * 0.5 * np.sin(theta[i]) * dtheta * np.sqrt(1 + dydx[i]**2)

        # Distance squared between point and vortex element
        r2 = (xp-x_i)**2 + (yp-y_i)**2 + 1e-10

        # Biot-Savart velocity contribution
        U += dGamma/(2*np.pi) * (yp-y_i)/r2
        V += -dGamma/(2*np.pi) * (xp-x_i)/r2

    return U, V


 
# Function: compute_circ
# Purpose:
# Computes circulation around a rectangular contour by
# performing the line integral ∮ V · dl
 
def compute_circ(xmin=-0.5, xmax=1.5, ymin=-0.5, ymax=0.5):

    circ = 0  # total circulation
    N = 400   # number of integration segments per edge

     
    # Bottom edge integration
     
    x_vals = np.linspace(xmin, xmax, N)
    for i in range(N-1):
        x = x_vals[i]
        dx = x_vals[i+1] - x_vals[i]

        U_loc, V_loc = velocity_point(x, ymin)
        circ += U_loc * dx

     
    # Right edge integration
     
    y_vals = np.linspace(ymin, ymax, N)
    for i in range(N-1):
        y = y_vals[i]
        dy = y_vals[i+1] - y_vals[i]

        U_loc, V_loc = velocity_point(xmax, y)
        circ += V_loc * dy

     
    # Top edge integration
     
    x_vals = np.linspace(xmax, xmin, N)
    for i in range(N-1):
        x = x_vals[i]
        dx = x_vals[i+1] - x_vals[i]

        U_loc, V_loc = velocity_point(x, ymax)
        circ += U_loc * dx

     
    # Left edge integration
     
    y_vals = np.linspace(ymax, ymin, N)
    for i in range(N-1):
        y = y_vals[i]
        dy = y_vals[i+1] - y_vals[i]

        U_loc, V_loc = velocity_point(xmin, y)
        circ += V_loc * dy

    return circ  # return total circulation