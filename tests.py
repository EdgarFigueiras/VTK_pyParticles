import vtkpoints as vtkp

#Cav    100
#Vort   57
#Gauss  30
#DarkM  100¿?


#def render_simulation(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, particles_size, cube_size, info)

#def render_simulation_images_multiprocess(path, n_particles, first_step, last_step, min_Psi, max_Psi, particles_size, cube_size, x_camera, y_camera, z_camera, info)

#vtkp.render_simulation("vortex_barrier30k.3d", 30000, 0, 200, 0, 0.05, 3000, 2, 50, 1)

#vtkp.render_simulation_images_multiprocess("vortex_barrier50k.3d", 50000, 0, 200, 0, 0.05, 2, 50, -105, 95, 110,  1)

#vtkp.render_simulation("soliton_barrera50k.3d", 30000, 190, 200, 0, 0.05, 3000, 2, 100, 1)

#vtkp.render_simulation_images_multiprocess("soliton_barrera50k.3d", 50000, 0, 200, 0, 0.05, 2, 50, -105, 95, 110,  1)

#Camera vortex_barrier [-105, 95, 110], [0, 0, 1]
#Camera soliton_barrier [-227, 130, -180], [0.210064, 0.9538159, 0.214727]


path = "soliton_barrera50k.3d"
n_particles = 50000
first_step = 0
last_step = 200
min_Psi = 0
max_Psi = 0.05
particles_size = 3
cube_size = 95
camera = [-227, 130, -180]
view = [0.210064, 0.9538159, 0.214727]
y_camera = 130
z_camera = -180
info = 1
time_step = 3000

vtkp.render_simulation_images_multiprocess(path, n_particles, first_step, last_step, min_Psi, max_Psi, particles_size, cube_size, camera, view, info)

#vtkp.render_simulation(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, particles_size, cube_size, info)







