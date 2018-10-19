import vtk

#Image saving function
def save_image(renderer, step):
    #Camera set Up
    renderer.GetActiveCamera().SetPosition(0, -300, 0)
    renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)

    renderLarge = vtk.vtkRenderLargeImage()
    renderLarge.SetInput(renderer)
    #Size of the output image, will change the brightness due to rendering issues
    renderLarge.SetMagnification(1)
    writer = vtk.vtkPNGWriter()
    writer.SetInputConnection(renderLarge.GetOutputPort())
    writer.SetFileName("./rendered_images/" + str(step) + ".png")
    writer.Write()
