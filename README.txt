================================================================================
             AERODYNAMIC ANALYSIS USING THIN AIRFOIL THEORY
================================================================================

Contributors: Addepalli Bhargava Sarma, Rahul Dutta, Rishiraaj Khurma
Description : Computes aerodynamic properties of NACA and user-defined airfoils
              using Thin Airfoil Theory, including camber line, camber slope,
              Fourier coefficients, lift/moment coefficients, circulation
              distribution, and velocity field around the airfoil.

================================================================================
TABLE OF CONTENTS
================================================================================

  1.  Overview
  2.  Requirements & Installation
  3.  Project File Structure
  4.  How to Run the Code
  5.  How to Configure Your Airfoil (user_input.py)
       5a. Using a NACA 4-Digit Airfoil
       5b. Using a User-Defined Camber Function
  6.  Module Descriptions
  7.  Outputs Generated
  8.  Theoretical Background
  9.  Example Run (Step-by-Step)

================================================================================
1. OVERVIEW
================================================================================

This toolkit implements Thin Airfoil Theory to analyze 2D airfoil
aerodynamics. Given an airfoil geometry and angle of attack, the code will:

  - Compute and plot the camber line (y vs x)
  - Compute and plot the camber line slope (dy/dx vs x)
  - Calculate Fourier coefficients A0, A1, A2, ... An
  - Compute the Lift Coefficient (Cl) and Moment Coefficient (Cm)
  - Compute and plot the circulation distribution along the airfoil
  - Compute the net (total) bound circulation
  - Compute and visualize the velocity vector field around the airfoil
  - Verify circulation using an independent closed-contour line integral

================================================================================
2. REQUIREMENTS & INSTALLATION
================================================================================

Python Version:
  Python 3.8 or higher is recommended.
  Suppose 'simpson' is throwing some error (it may in some older python versions), it will have to be replaced by 'simp'. This is unlikely to be an issue though. 

Required Libraries:
  - numpy
  - matplotlib
  - scipy

Installation (if not already installed):
  Run the following command in your terminal or command prompt:

      pip install numpy matplotlib scipy

  OR if using conda:

      conda install numpy matplotlib scipy

To verify installations, open Python and run:

      import numpy, matplotlib, scipy
      print(numpy.__version__, matplotlib.__version__, scipy.__version__)

================================================================================
3. PROJECT FILE STRUCTURE
================================================================================

Place ALL the following files in the SAME folder/directory:

  ThinAirfoilAnalysis/
  |
  |-- main.py                      <- MAIN script (run this)
  |-- user_input.py                <- USER CONFIGURATION FILE (edit this)
  |-- camber_line.py               <- Computes and plots camber line
  |-- camber_slope.py              <- Computes and plots camber slope
  |-- fourier_cl_cm.py             <- Computes Fourier coefficients, Cl, Cm
  |-- circulation_distribution.py  <- Computes and plots circulation distribution
  |-- net_circulation.py           <- Computes total bound circulation
  |-- velocity_vector_field.py     <- Computes and plots velocity field
  |-- README.txt                   <- This file

  IMPORTANT: All .py files must be in the same directory. Do NOT separate them
  into subfolders, as the modules import each other using direct names.

================================================================================
4. HOW TO RUN THE CODE
================================================================================

Step 1: Configure your airfoil in user_input.py (see Section 5 below).

Step 2: Open a terminal / command prompt.

Step 3: Navigate to the folder containing all the .py files using the
        'cd' command in your terminal. 

Step 4: Run the main script:

        python main.py

Step 5: The program will:
        - Display plots on screen one by one (close each to continue)
        - Save output images to the same directory
        - Print aerodynamic values to the terminal

================================================================================
5. HOW TO CONFIGURE YOUR AIRFOIL (user_input.py)
================================================================================

Open user_input.py in any text editor (Notepad, VS Code, etc.) and edit
the values as described below.

-------------------------------------
5a. USING A NACA 4-DIGIT AIRFOIL
-------------------------------------

Set:
    input_type = 1

Then edit the airfoil parameters:
    max_camber_percent      = 1.3    # Max camber as % of chord (e.g., 1.3 = 1.3%)
    camber_position_percent = 18.5   # Position of max camber from LE as % of chord
    alpha_deg               = 3.0    # Angle of attack in degrees

Example: For a NACA 2412 airfoil at 5 degrees:
    max_camber_percent      = 2.0    # '2' in NACA 2412
    camber_position_percent = 40.0   # '4' in NACA 2412 -> 40%
    alpha_deg               = 5.0

NACA 4-Digit Code Reference:
    NACA MPXX:
      M  = max camber (% of chord)              -> max_camber_percent = M
      P  = position of max camber (tenths of chord) -> camber_position_percent = P * 10
      XX = max thickness % of chord (not used here, only camber line is modelled)

-------------------------------------
5b. USING A USER-DEFINED CAMBER FUNCTION
-------------------------------------

Set:
    input_type = 2

Then edit the user_defined_camber function at the bottom of user_input.py:

    def user_defined_camber(x):
        import numpy as np
        y = 0.08 * np.sin(np.pi * x) * (1 - x)   # <-- REPLACE THIS with your function
        return y

  - x is a numpy array of values between 0 and 1 (normalized chord)
  - y must be returned as a numpy array of the same size as x
  - The function must satisfy y(0) = 0 and y(1) = 0 (camber is zero at LE and TE)
  - Also set alpha_deg to your desired angle of attack

  Provided examples (uncomment to use):
      y = 0.08 * np.sin(np.pi * x) * (1 - x)   # Sinusoidal camber (default)
      y = 0.16 * x * (1 - x)                    # Parabolic camber
      y = 0.3  * x * (1 - x)**3                 # Cubic camber

================================================================================
6. MODULE DESCRIPTIONS
================================================================================

  FILE                          ROLE
  -----------------------------------------------------------------------
  user_input.py               | Central configuration file. All airfoil
                              | parameters and flight conditions are set here.
                              | Edit ONLY this file to change inputs.
  -----------------------------------------------------------------------
  camber_line.py              | Computes the camber line y(x) using the
                              | NACA analytical formula or user function.
                              | Plots and saves camber_line.png.
  -----------------------------------------------------------------------
  camber_slope.py             | Numerically differentiates the camber line
                              | to get dy/dx(x). Uses forward, central, and
                              | backward finite differences.
                              | Plots and saves camber_slope.png.
  -----------------------------------------------------------------------
  fourier_cl_cm.py            | Computes Fourier coefficients A0, A1, ..., An
                              | via numerical integration over theta.
                              | Computes Cl and Cm from standard formulae:
                              |   Cl = pi * (2*A0 + A1)
                              |   Cm = -pi/2 * (A0 + A1 - A2/2)
  -----------------------------------------------------------------------
  circulation_distribution.py | Converts x to theta, then evaluates the
                              | vortex sheet strength gamma(theta) using
                              | the Fourier series. Plots gamma vs theta.
                              | Saves Circulation_distribution.png.
  -----------------------------------------------------------------------
  net_circulation.py          | Integrates the circulation distribution
                              | (with the appropriate Jacobian) to get the
                              | total bound circulation (Gamma_total).
  -----------------------------------------------------------------------
  velocity_vector_field.py    | Uses Biot-Savart law to compute velocity
                              | at every point in a grid around the airfoil.
                              | Superimposes freestream + induced velocity.
                              | Plots the velocity vector field with color
                              | showing speed magnitude.
                              | Also computes circulation via closed-contour
                              | line integral for verification.
                              | Saves Velocity_field.png.
  -----------------------------------------------------------------------
  main.py                     | Master driver. Calls all modules in sequence.
                              | Prints Fourier coefficients, Cl, Cm, and both
                              | circulation values to the terminal.
  -----------------------------------------------------------------------

================================================================================
7. OUTPUTS GENERATED
================================================================================

After running main.py, the following outputs are produced:

  PLOTS (saved as .png in the same directory):
  +---------------------------+-----------------------------------------------+
  | File                      | Description                                   |
  +---------------------------+-----------------------------------------------+
  | camber_line.png           | Camber line y vs x. Red dot marks max camber. |
  | camber_slope.png          | Slope dy/dx vs x along the chord.             |
  | Circulation_distribution.png | Vortex sheet strength gamma vs theta.      |
  | Velocity_field.png        | Vector field of velocity around the airfoil.  |
  |                           | Color indicates speed magnitude. Camber line  |
  |                           | shown in red at the angle of attack.          |
  +---------------------------+-----------------------------------------------+

  TERMINAL OUTPUT (printed to screen):
  - A0, A1, A2  : First three Fourier coefficients
  - Cl           : Lift coefficient
  - Cm           : Moment coefficient about the leading edge
  - Net circulation (method 1): Integration of gamma*sin(theta)/2 over theta
  - Net circulation (method 2): Closed-contour line integral of velocity

  Both circulation values should be close to each other, confirming the
  consistency of the two independent methods.

================================================================================
8. THEORETICAL BACKGROUND
================================================================================

This code implements classical Thin Airfoil Theory:

  Coordinate Transformation:
      x = (1 - cos(theta)) / 2   maps   x in [0,1]  ->  theta in [0, pi]

  Vortex Sheet Strength (Fourier Series):
      gamma(theta) = 2*U_inf * [A0 * cot(theta/2) + SUM(An * sin(n*theta))]

  Fourier Coefficients:
      A0 = alpha - (1/pi) * INTEGRAL[dy/dx d(theta)]
      An = (2/pi) * INTEGRAL[dy/dx * cos(n*theta) d(theta)]   for n >= 1

  Aerodynamic Coefficients:
      Cl = pi * (2*A0 + A1)
      Cm_LE = -(pi/2) * (A0 + A1 - A2/2)

  Total Circulation (Method 1 - Integration):
      Gamma = INTEGRAL[gamma(x) dx]  (using Jacobian from theta transformation)

  Total Circulation (Method 2 - Kelvin's Theorem):
      Gamma = CLOSED LINE INTEGRAL of V . dl   around a rectangular contour
              enclosing the airfoil (computed via Biot-Savart induced velocity)

  Velocity Field (Biot-Savart Law):
      Each vortex element dGamma on the airfoil induces velocity:
        dU = +dGamma/(2*pi) * (y - y_i) / r^2
        dV = -dGamma/(2*pi) * (x - x_i) / r^2
      Total velocity = freestream + sum of all induced contributions.

================================================================================
9. EXAMPLE RUN (STEP-BY-STEP)
================================================================================

Goal: Analyze a NACA 4312 airfoil (Max camber=4.3%, Camber position=33.5%)
      at an angle of attack of 3 degrees.

Step 1: Open user_input.py and confirm / set:
          input_type              = 1
          max_camber_percent      = 4.3
          camber_position_percent = 33.5
          alpha_deg               = 3.0

Step 2: Open a terminal / command prompt and navigate to the folder
        containing all the .py files using the 'cd' command.

Step 3: Run:
          python main.py

Step 4: Expected terminal output (approximate values):
          First Fourier Coefficent A0 = 0.035610687985462935
          Second Fourier Coefficent A1 = 0.18123769515910998
          Third Fourier Coefficent A2 = 0.05103837803543531
          Lift Coefficient Cl = 0.7931235631942236
          Coefficient of Moment about leading edge Cm = -0.3005391953430919
          Total Circulation through integration of circulation distributuion= -7.931206691447508 m^2/s
          Total Circulation through line integration of velocity = -7.9870399714276 m^2/s

Step 5: Check the output folder for:
          camber_line.png
          camber_slope.png
          Circulation_distribution.png
          Velocity_field.png

================================================================================
END OF README
================================================================================
