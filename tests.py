import vtkpoints as vtkp

#actor = vtkp.create_actor("./Cav3dData.3d", 100000, 25, 0, 0.05)

#vtkp.render_actor_background(actor, 0.0, 0.0, 0.0)

#vtkp.render_simulation("./Cav3dData.3d")

vtkp.render_simulation("./Cav3dData.3d", 100000, 0, 40, 0.0, 0.05, 1000, 2)
