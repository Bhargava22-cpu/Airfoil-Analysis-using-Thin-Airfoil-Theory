================================================================================
         PRESSURE DISTRIBUTION AROUND THE AIRFOIL
                        README & USER GUIDE
================================================================================

Contributor : Addepalli Bhargava Sarma
Description : Computes and visualizes the static pressure field around a NACA
              or user-defined airfoil using Bernoulli's equation applied to
              the velocity field obtained from the vortex sheet formulation.

================================================================================
TABLE OF CONTENTS
================================================================================

  1.  Overview
  2.  File Requirements
  3.  How to Configure the Airfoil
  4.  How to Run
  5.  Output
  6.  Theory
  7.  Default Parameters

================================================================================
1. OVERVIEW
================================================================================

This script extends the main thin airfoil analysis by computing the
static pressure at every point in the flow field around the airfoil. The
pressure is derived from the velocity field using Bernoulli's equation.

The airfoil geometry and angle of attack are taken directly from user_input.py,
so any NACA or user-defined airfoil configured there will be used here as well.

This script is run SEPARATELY from main.py because it requires a finer
computational grid (dx = 0.01, dy = 0.01) for a smooth pressure contour,
which would significantly slow down the main workflow if included there.

================================================================================
2. FILE REQUIREMENTS
================================================================================

All of the following files must be present in the SAME folder:

  ThinAirfoilAnalysis/
  |
  |-- pressure_distribution.py     <- Run this file for pressure plot
  |-- user_input.py                <- Airfoil configuration (edit this)
  |-- velocity_vector_field.py     <- Velocity field computation
  |-- camber_line.py               <- Camber line computation
  |-- camber_slope.py              <- Camber slope computation
  |-- fourier_cl_cm.py             <- Fourier coefficients
  |-- circulation_distribution.py  <- Circulation distribution
  |-- README_pressure_distribution.txt  <- This file

  pressure_distribution.py imports from velocity_vector_field.py, which in
  turn imports from all the other modules listed above. All files must be
  present even though only pressure_distribution.py is run directly.

================================================================================
3. HOW TO CONFIGURE THE AIRFOIL
================================================================================

Open user_input.py and set your desired airfoil and flight condition.
The pressure distribution will be computed for whatever is configured there.

  For a NACA airfoil (input_type = 1):
      input_type              = 1
      max_camber_percent      = 4.3    # Max camber as % of chord
      camber_position_percent = 33.5   # Position of max camber as % of chord
      alpha_deg               = 3.0    # Angle of attack in degrees

  For a user-defined camber (input_type = 2):
      input_type = 2
      Edit the user_defined_camber function in user_input.py with your
      camber function y = f(x), where x is between 0 and 1.
      Also set alpha_deg to your desired angle of attack.

================================================================================
4. HOW TO RUN
================================================================================

Step 1: Configure your airfoil in user_input.py (see Section 3 above).

Step 2: Open velocity_vector_field.py and change the grid resolution
        to the following values for a smoother pressure contour:

            dx = 0.01
            dy = 0.01

        NOTE: This finer grid significantly increases computation time.
        The coarser default (dx = 0.10, dy = 0.10) can be used for a
        quick preview, but the contour will appear less smooth.

Step 3: Open a terminal / command prompt and navigate to the folder
        containing all the .py files using the 'cd' command.

Step 4: Run the script directly:

            python pressure_distribution.py

Step 5: The pressure contour plot will be displayed on screen and saved
        to the same directory as Pressure_distribution.png.

  IMPORTANT: After running pressure_distribution.py, remember to revert
  dx and dy back to 0.10 in velocity_vector_field.py if you intend to
  run main.py again, to avoid long runtimes in the main workflow.

================================================================================
5. OUTPUT
================================================================================

  File saved: Pressure_distribution.png

  The plot shows:
    - A filled contour map of static pressure (in Pascals) across the
      flow field around the airfoil.
    - The rotated camber line of the airfoil overlaid in black, oriented
      at the specified angle of attack.
    - A colorbar indicating pressure magnitude (jet colormap).
      Lower pressure appears above the airfoil and higher pressure below,
      consistent with lift generation as predicted by Bernoulli's equation.

  Plot domain:
    - x : -1 to 3 meters
    - y : -1.5 to 1.5 meters

================================================================================
6. THEORY
================================================================================

  Velocity Field:
      The velocity at each grid point is computed by superimposing the
      freestream velocity and the velocity induced by the vortex sheet
      (obtained from thin airfoil theory via the Biot-Savart law).

  Bernoulli's Equation (incompressible, inviscid flow):

      p + (1/2) * rho * V^2  =  p_inf + (1/2) * rho * U_inf^2

  Rearranged for static pressure:

      p  =  p_inf + (1/2) * rho * (U_inf^2 - V^2)

  where:
      p     = local static pressure (Pa)
      p_inf = freestream static pressure (Pa)
      rho   = air density (kg/m^3)
      U_inf = freestream velocity magnitude (m/s)
      V     = local velocity magnitude at each grid point (m/s)

================================================================================
7. DEFAULT PARAMETERS
================================================================================

  These can be changed inside pressure_distribution.py if needed:

      U_inf = 20       (m/s)      Freestream velocity
      rho   = 1.225    (kg/m^3)   Air density at sea level (ISA conditions)
      p_inf = 101325   (Pa)       Freestream static pressure at sea level

================================================================================
END OF README
================================================================================
