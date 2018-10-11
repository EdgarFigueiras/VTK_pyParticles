import vtkpoints as vtkp

#Some examples of use, requires a file with compatible 3d data format

#actor = vtkp.create_actor("./3dData.3d", 100000, 25, 0, 0.05)

#vtkp.render_actor_background(actor, 0.0, 0.0, 0.0)

#vtkp.render_simulation("./3dData.3d")

vtkp.render_simulation("./3dData.3d", 100000, 20, 40, 0.0, 0.05, 3000)