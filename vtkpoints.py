import vtk
import numpy as np
import random
import math
import time

#Class that allows the evolutionf of the simulation
class vtkTimerCallback():
    def __init__(self, path_data, num_particles, initial_step, ultimate_step, minim_Psi, maxim_Psi):
        self.timer_count = 0
        self.path = path_data
        self.n_particles = num_particles
        self.min_Psi = minim_Psi
        self.max_Psi = maxim_Psi
        self.first_step = initial_step
        self.last_step = ultimate_step
        
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

        new_actor = create_actor(self.path, self.n_particles, self.timer_count + self.first_step, self.min_Psi, self.max_Psi)
        renderer.AddViewProp(new_actor)
        
        iren.GetRenderWindow().Render()
        print(self.timer_count + self.first_step)
        
        self.timer_count += 1


def calculate_color_by_amplitude(amplitude, min, max):
    #Colors array, from dark blue (Lowest probability) to dark red (Highest probability)
    color = [0,0,0]

    colorArray = [
        [0,0,130],
        [0,0,200],
        [0,0,255],
        [0,40,255],
        [0,90,255],
        [0,153,255],
        [1,212,255],
        [38,255,210],
        [96,255,150],
        [134,255,115],
        [177,255,71],
        [228,255,20],
        [255,211,0],
        [255,163,0],
        [255,100,0],
        [255,60,0],
        [245,10,0],
        [200,0,0],
        [155,0,0],
        [131,0,0]
    ];
    
    #Calculate the step to use the full range of colours between min and max psi values
    #Calculate the amplitude to adjust the new steps.
    #Amplitude_in_order_0-1 = (Amplitude - minPsi)/(maxPsi-minPsi)
    x_ampl = (amplitude - min)/(max-min);
    
    #20 steps of colours, amplitude from 0.0 to 1.0
    indexOfColor = math.floor(x_ampl / 0.05);
    
    color[0] = colorArray[indexOfColor][0];
    color[1] = colorArray[indexOfColor][1];
    color[2] = colorArray[indexOfColor][2];

    return color

#File load, return the array with the 3dData of the selected path
def load_data(path):
    #File with binary data
    file_with_binary_data = open(path, 'rb+')

    #Gets the binary data as an array
    array_with_all_data = np.load(file_with_binary_data)

    #Matrix with the data of the 2D grid
    array_3d = array_with_all_data['arr_0']

    return array_3d


# Creates teh actor and returns it to be shown:
# path -> The path where is stored the numoy array with the data
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
        color = calculate_color_by_amplitude(array_data[x][3], min, max)
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
    renderWindow.SetSize(800,600)
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
    renderWindow.SetSize(800,600)
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
    renderWindow.SetSize(800,600)
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
def render_simulation(path, n_particles, first_step, last_step, min_Psi, max_Psi, time_step):
    actor = create_actor(path, n_particles, first_step, min_Psi, max_Psi)
    
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0,0,0)
    renderer.AddViewProp(actor)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(800,600)
    renderWindow.AddRenderer(renderer)
    renWinInteractor = vtk.vtkRenderWindowInteractor()
    renWinInteractor.SetRenderWindow(renderWindow)
    renWinInteractor.Render()
    
    print(first_step)
    
    # Initialize must be called prior to creating timer events.
    renWinInteractor.Initialize()
        
    # Sign up to receive TimerEvent
    timerCallback = vtkTimerCallback(path, n_particles, first_step + 1, last_step, min_Psi, max_Psi)
    timerCallback.actor = actor
    renWinInteractor.AddObserver('TimerEvent', timerCallback.execute)
    timerId = renWinInteractor.CreateRepeatingTimer(time_step);
    
    renWinInteractor.Start()



