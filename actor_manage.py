import vtk
import numpy as np
import random
import math
import calculatecolors as colors


#File load, return the array with the 3dData of the selected path
def load_data(path):
    #File with binary data
    file_with_binary_data = open(path, 'rb+')

    #Gets the binary data as an array
    array_with_all_data = np.load(file_with_binary_data)

    #Matrix with the data of the 2D grid
    array_3d = array_with_all_data['arr_0']

    return array_3d


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
