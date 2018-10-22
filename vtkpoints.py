import vtk
import numpy as np
import random
import math
import time
import multiprocessing
from multiprocessing import Process
import actor_manage as actor_man
import image_saver as img_save
from step_timer import vtkTimerCallback


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



#Renders the simulation of the file passed and saves it as image
# path -> File path of the numpy array with the 3d data
# n_particles -> number of particles that will be rendered in the simulation each step
# first_step -> starting step of the simulation
# last_step -> ending step of the simulation
# min_Psi -> minimum Psi value to represent the colors of the simulation
# max_Psi -> maximum Psi value to represent the colors of the simulation
# time_step -> time elapsed between steps, measured in miliseconds
# info -> flag, 1==Print info, 0==Dont show info
# thread_number -> number of the thread
def render_simulation_for_multiprocess(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, info, thread_number):
    if (info>0):
        print("path: ", path , "\n", "first step: ", first_step, "  last step: ", last_step)
        print(" min_Psi: ", min_Psi, "  max_Psi: ", max_Psi, "  time_step: ", time_step, "ms")
    
    total_steps = last_step - first_step + 1
    
    renderer = vtk.vtkOpenGLRenderer()
    renderer.SetBackground(0,0,0)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    #Disables the 3D render window
    renderWindow.SetOffScreenRendering(1);
    renWinInteractor = vtk.vtkRenderWindowInteractor()

    for actual_step in range(0,total_steps):

        actor = actor_man.create_actor(path, n_particles, actual_step + first_step, min_Psi, max_Psi)
        renderer.AddViewProp(actor)

        renderWindow.AddRenderer(renderer)

        renWinInteractor.SetRenderWindow(renderWindow)
        renWinInteractor.Render()
        renWinInteractor.Initialize()

        print(actual_step + first_step,  "Thread: ", thread_number)
    
        img_save.save_image(renderer, actual_step + first_step)
        renderer.RemoveAllViewProps()
    
    # Initialize must be called prior to creating timer events.
    
    '''
    renWinInteractor.Initialize()
    
    # Sign up to receive TimerEvent
    timerCallback = vtkTimerCallback(path, n_particles, first_step + 1, last_step, min_Psi, max_Psi, 2)
    timerCallback.actor = actor
    renWinInteractor.AddObserver('TimerEvent', timerCallback.execute)
    timerId = renWinInteractor.CreateRepeatingTimer(time_step);

    renWinInteractor.Start()
    '''

#Renders the simulation of the file passed and saves it as image
# path -> File path of the numpy array with the 3d data
# n_particles -> number of particles that will be rendered in the simulation each step
# first_step -> starting step of the simulation
# last_step -> ending step of the simulation
# min_Psi -> minimum Psi value to represent the colors of the simulation
# max_Psi -> maximum Psi value to represent the colors of the simulation
# time_step -> time elapsed between steps, measured in miliseconds
# info -> flag, 1==Print info, 0==Dont show info
def render_simulation_images_multiprocess(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, info):
    #print("Number of cpu : ", multiprocessing.cpu_count())
    number_processors = multiprocessing.cpu_count()
    total_steps = last_step - first_step
    steps_per_process = math.floor (total_steps / number_processors)
    print("Total steps : ", total_steps)
    print("Steps per process : ", steps_per_process)
    procs = []
    start_step = first_step
    finish_step = first_step + steps_per_process
    
    for num_process in range (0,number_processors):
        if (num_process == number_processors - 1):
            finish_step = last_step
        print("Start step : ", start_step, "  finish_step: ", finish_step)
        proc = Process(target=render_simulation_for_multiprocess, args=(path, n_particles, start_step, finish_step, min_Psi, max_Psi, time_step, info, num_process))
        procs.append(proc)
        proc.start()
        start_step =  finish_step + 1
        finish_step = start_step + steps_per_process -1






