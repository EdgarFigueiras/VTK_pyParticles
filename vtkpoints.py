import vtk
import numpy as np
import random
import math
import time
import actor_manage as actor_man
import image_saver as img_save
from step_timer import vtkTimerCallback


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


#Renders the simulation of the file passed and saves it as image
# path -> File path of the numpy array with the 3d data
# n_particles -> number of particles that will be rendered in the simulation each step
# first_step -> starting step of the simulation
# last_step -> ending step of the simulation
# min_Psi -> minimum Psi value to represent the colors of the simulation
# max_Psi -> maximum Psi value to represent the colors of the simulation
# time_step -> time elapsed between steps, measured in miliseconds
# info -> flag, 1==Print info, 0==Dont show info
def render_simulation_images(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, info):
    if (info>0):
        print("path: ", path , "\n", "first step: ", first_step, "  last step: ", last_step)
        print(" min_Psi: ", min_Psi, "  max_Psi: ", max_Psi, "  time_step: ", time_step, "ms")
    
    actor = actor_man.create_actor(path, n_particles, first_step, min_Psi, max_Psi)

    renderer = vtk.vtkOpenGLRenderer()
    renderer.SetBackground(0,0,0)
    renderer.AddViewProp(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    #Disables the 3D render window
    renderWindow.SetOffScreenRendering(1);
    renderWindow.AddRenderer(renderer)

    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)
    renWinInteractor.Render()
    renWinInteractor.Initialize()
    
    print("Steps:")
    print(first_step)
    
    img_save.save_image(renderer, first_step)
    
    # Initialize must be called prior to creating timer events.
    renWinInteractor.Initialize()
    
    # Sign up to receive TimerEvent
    timerCallback = vtkTimerCallback(path, n_particles, first_step + 1, last_step, min_Psi, max_Psi, 2)
    timerCallback.actor = actor
    renWinInteractor.AddObserver('TimerEvent', timerCallback.execute)
    timerId = renWinInteractor.CreateRepeatingTimer(time_step);

    renWinInteractor.Start()
    

#Renders the simulation of the file passed
# path -> File path of the numpy array with the 3d data
# n_particles -> number of particles that will be rendered in the simulation each step
# first_step -> starting step of the simulation
# last_step -> ending step of the simulation
# min_Psi -> minimum Psi value to represent the colors of the simulation
# max_Psi -> maximum Psi value to represent the colors of the simulation
# time_step -> time elapsed between steps, measured in miliseconds
# info -> flag, 1==Print info, 0==Dont show info
def render_simulation(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, info):
    if (info>0):
        print("path: ", path , "\n", "first step: ", first_step, "  last step: ", last_step)
        print(" min_Psi: ", min_Psi, "  max_Psi: ", max_Psi, "  time_step: ", time_step, "ms")
    
    actor = actor_man.create_actor(path, n_particles, first_step, min_Psi, max_Psi)

    renderer = vtk.vtkOpenGLRenderer()
    renderer.SetBackground(0,0,0)
    renderer.AddViewProp(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    renderWindow.AddRenderer(renderer)

    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)
    renWinInteractor.Render()
    
    print("Steps:")
    print(first_step)
    
    # Initialize must be called prior to creating timer events.
    renWinInteractor.Initialize()
        
    # Sign up to receive TimerEvent
    timerCallback = vtkTimerCallback(path, n_particles, first_step + 1, last_step, min_Psi, max_Psi, info)
    timerCallback.actor = actor
    renWinInteractor.AddObserver('TimerEvent', timerCallback.execute)
    timerId = renWinInteractor.CreateRepeatingTimer(time_step);

    renWinInteractor.Start()




