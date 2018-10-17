import vtk
import numpy as np
import random
import math
import time
import calculatecolors as colors

#Class that allows the evolutionf of the simulation
class vtkTimerCallback():
    def __init__(self, path_data, num_particles, initial_step, ultimate_step, minim_Psi, maxim_Psi, info_):
        self.timer_count = 0
        self.path = path_data
        self.n_particles = num_particles
        self.min_Psi = minim_Psi
        self.max_Psi = maxim_Psi
        self.first_step = initial_step
        self.last_step = ultimate_step
        self.info = info_
        
    def execute(self,obj,event):
        iren = obj
        wren = iren.GetRenderWindow()
        renderer = wren.GetRenderers().GetFirstRenderer()
        
        #self.actor.SetPosition(self.timer_count, self.timer_count,0);
        renderer.RemoveAllViewProps()

        #Enables the loop to never stop the simulation, when reaches last step starts again
        if((self.timer_count + self.first_step) > self.last_step):
            if(self.first_step > 0):
                self.timer_count = -1
            else:
                self.timer_count = 0

        actor = create_actor(self.path, self.n_particles, self.timer_count + self.first_step, self.min_Psi, self.max_Psi)
        renderer.AddViewProp(actor)
        
        #Shows function info
        if(self.info > 1):
            actor_functions = create_actor_fuctions(self.path, self.n_particles, self.timer_count + self.first_step, self.min_Psi, self.max_Psi)
            renderer.AddViewProp(actor_functions)
        
        iren.GetRenderWindow().Render()
        print(self.timer_count + self.first_step)
        
        self.timer_count += 1


# Creates the actor and returns it to be shown:
# path -> The path where is stored the numpy array with the data
# N -> Number of particles that will be used in the simulation
# min -> min Psi value to generate the colour gradation
# max -> max Psi value to generate the colour gradation
def create_actor_fuctions(path, N, time_step, min, max):
    #Use an auxiliar array to work with a variable number of points,
    #allowing the user to make diferent points simulation with good results
    array_data = np.zeros((N, 4))

    array_3d = load_data(path)

    #Fill the auxiliar array with the data of the original one
    for point_number in range (0, N):
        array_data[point_number] = array_3d[time_step][point_number]
    
    
    #Colors
    Colors = vtk.vtkUnsignedCharArray();
    Colors.SetNumberOfComponents(3);
    Colors.SetName("Colors");

    #plot
    x_axis = np.zeros((N))
    y_axis = np.zeros((N))
    z_axis = np.zeros((N))
    psi_axis = np.zeros((N))

    # Generate point positions and insert in vtkPoints
    color = [255,255,255]
    points = vtk.vtkPoints()

    #X axis function
    for x in np.arange(0,N):
        points.InsertNextPoint(array_data[x][0], array_data[x][3]*1000, -100.0)
        #color = colors.calculate_color_by_amplitude(array_data[x][3], min, max)
        Colors.InsertNextTuple3(color[0],color[1],color[2])

    #Z axis function
    for x in np.arange(0,N):
        points.InsertNextPoint(array_data[x][0], -100,  array_data[x][2])
        #color = colors.calculate_color_by_amplitude(array_data[x][3], min, max)
        Colors.InsertNextTuple3(color[0],color[1],color[2])


    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.GetPointData().SetScalars(Colors)

    vertexFilter = vtk.vtkVertexGlyphFilter()
    vertexFilter.SetInputData(polyData)
    vertexFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertexFilter.GetOutputPort())
    mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


#File load, return the array with the 3dData of the selected path
def load_data(path):
    #File with binary data
    file_with_binary_data = open(path, 'rb+')

    #Gets the binary data as an array
    array_with_all_data = np.load(file_with_binary_data)

    #Matrix with the data of the 2D grid
    array_3d = array_with_all_data['arr_0']

    return array_3d


# Creates the actor and returns it to be shown:
# path -> The path where is stored the numpy array with the data
# N -> Number of particles that will be used in the simulation
# min -> min Psi value to generate the colour gradation
# max -> max Psi value to generate the colour gradation
def create_actor(path, N, time_step, min, max):
    #Use an auxiliar array to work with a variable number of points,
    #allowing the user to make diferent points simulation with good results
    array_data = np.zeros((N, 4))

    array_3d = load_data(path)

    #Fill the auxiliar array with the data of the original one
    for point_number in range (0, N):
        array_data[point_number] = array_3d[time_step][point_number]
    
    
    #Colors
    Colors = vtk.vtkUnsignedCharArray();
    Colors.SetNumberOfComponents(3);
    Colors.SetName("Colors");


    # Generate point positions and insert in vtkPoints
    color = [0,0,0]
    points = vtk.vtkPoints()
    for x in np.arange(0,N):
        points.InsertNextPoint(array_data[x][0],array_data[x][1],array_data[x][2])
        color = colors.calculate_color_by_amplitude(array_data[x][3], min, max)
        Colors.InsertNextTuple3(color[0],color[1],color[2])

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.GetPointData().SetScalars(Colors)

    vertexFilter = vtk.vtkVertexGlyphFilter()
    vertexFilter.SetInputData(polyData)
    vertexFilter.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertexFilter.GetOutputPort())
    mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


#Renders multiple actors passed as a list
def render_actors_list(actors_list):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0,0,0)
    
    for actor in actors_list:
        renderer.AddViewProp(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    renderWindow.AddRenderer(renderer)

    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renWinInteractor.Start()


#Renders the actor passed
def render_actor(actor):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0,0,0)

    renderer.AddViewProp(actor)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    renderWindow.AddRenderer(renderer)

    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)
    
    renderWindow.Render()
    renWinInteractor.Start()

#Renders the actor passed and sets the bacground color using r,g,b passed values
def render_actor_background(actor, r, g, b):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(r,g,b)
    renderer.AddViewProp(actor)
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(1600,1200)
    renderWindow.AddRenderer(renderer)
    
    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)
    
    renderWindow.Render()
    renWinInteractor.Start()


#Renders the simulation of the file passed
# path -> File path of the numpy array with the 3d data
# n_particles -> number of particles that will be rendered in the simulation each step
# first_step -> starting step of the simulation
# last_step -> ending step of the simulation
# min_Psi -> minimum Psi value to represent the colors of the simulation
# max_Psi -> maximum Psi value to represent the colors of the simulation
# time_step -> time elapsed between steps, measured in miliseconds
# info -> flag, 2==Print info and show functions in 3D view 1==Print info, 0==Dont show info
def render_simulation(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step, info):
    if (info>0):
        print("path: ", path , "\n", "first step: ", first_step, "  last step: ", last_step)
        print(" min_Psi: ", min_Psi, "  max_Psi: ", max_Psi, "  time_step: ", time_step, "ms")
    
    actor = create_actor(path, n_particles, first_step, min_Psi, max_Psi)
    actor_functions = create_actor_fuctions(path, n_particles, first_step, min_Psi, max_Psi)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0,0,0)

    if (info>1):
        renderer.AddViewProp(actor_functions)
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



