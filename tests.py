import vtkpoints as vtkp

#Cav    100
#Vort   57
#Gauss  30
#DarkM  100¿?

#actor = vtkp.create_actor("./Cav3dData.3d", 100000, 25, 0, 0.05)

#vtkp.render_actor_background(actor, 0.0, 0.0, 0.0)

#vtkp.render_simulation("./caviton.3d", 100000, 0, 100, 0, 1, 3000, 1)

#vtkp.render_simulation_images_multiprocess("./caviton.3d", 100000, 0, 100, 0.0, 1, 1)

#vtkp.render_simulation_images_multiprocess("./gauss.3d", 100000, 0, 30, 0.0, 0.3, 1)

#vtkp.render_simulation("./py_3dData.3d", 100000, 0, 100, 0, 1, 3000, 1)

#vtkp.render_simulation_images_multiprocess("./py_3dData.3d", 100000, 0, 100, 0.0, 1, 1)

#vtkp.render_simulation("Vort3dData.3d", 100000, 0, 57, 0, 1, 3000, 1)

#vtkp.render_simulation_images_multiprocess("./Vort3dData.3d", 100000, 0, 57, 0.0, 1, 1)

#vtkp.render_simulation("darkmat.3d", 100000, 0, 100, 0, 1, 3000, 1)

#vtkp.render_simulation_images_multiprocess("./Vort3dData.3d", 100000, 0, 57, 0.0, 1, 1)

#vtkp.render_simulation("vortex_barrier30k.3d", 30000, 0, 200, 0, 0.05, 3000, 1)

vtkp.render_simulation_images_multiprocess("vortex_barrier30k.3d", 30000, 0, 200, 0, 0.05, 1)