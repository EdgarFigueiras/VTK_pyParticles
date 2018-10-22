import vtkpoints as vtkp

#actor = vtkp.create_actor("./Cav3dData.3d", 100000, 25, 0, 0.05)

#vtkp.render_actor_background(actor, 0.0, 0.0, 0.0)

#vtkp.render_simulation("./Cav3dData.3d")

#vtkp.render_simulation("./Cav3dData.3d", 100000, 0, 40, 0.0, 0.05, 100, 1)

#vtkp.render_simulation("./Vort3dData.3d", 100000, 35, 55, 0.0, 1, 1000, 1)

#vtkp.render_simulation("./3dData.3d", 100000, 0, 20, 0.0, 1, 3000, 1)

#vtkp.render_simulation_images("./Cav3dData.3d", 100000, 0, 40, 0.0, 0.05, 100, 1)

#vtkp.render_simulation_images("./Cav3dData.3d", 100000, 0, 50, 0.0, 0.05, 100, 1)

vtkp.render_simulation_images_multiprocess("./Cav3dData.3d", 100000, 0, 50, 0.0, 0.05, 100, 1)