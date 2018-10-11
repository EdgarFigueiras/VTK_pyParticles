# VTK_pyParticles
VTK library made for visualize probability clouds with python.

Reads 3d data from a numpy array with the format (x,y,z, Psi) and represents the data using particles. The Psi value is represented using color degradation from blue (low probability) to red (high probability).
Allows the representation of just one time step, multiple simulations simultaeously in one step, one step and modify environment values or display the full simulation between selected time steps.
