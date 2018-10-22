import vtk
import numpy as np
import random
import math
import time
import actor_manage as actor_man
import image_saver as img_save


# Class that allows the evolutionf of the simulation
# Avances step by step, in loop if is window rendered and until the last step in image saving mode
# path_data -> File path of the numpy array with the 3d data
# num_particles -> number of particles that will be rendered in the simulation each step
# initial_step -> starting step of the simulation
# ultimate_step -> ending step of the simulation
# minim_Psi -> minimum Psi value to represent the colors of the simulation
# maxim_Psi -> maximum Psi value to represent the colors of the simulation
# info_ -> flag, ==2 image save mode, !=2 windowed mode
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
        if((self.timer_count + self.first_step) == self.last_step):
            #If is saving images then stop swhen reaches the end without the loop
            if(self.info == 2):
                iren.TerminateApp()
            else:
                if(self.first_step > 0):
                    self.timer_count = -1
                else:
                    self.timer_count = 0
    
        actor = actor_man.create_actor(self.path, self.n_particles, self.timer_count + self.first_step, self.min_Psi, self.max_Psi)
        renderer.AddViewProp(actor)
    
        if(self.info == 2):
            img_save.save_image(renderer, self.timer_count + self.first_step)
        else:
            iren.GetRenderWindow().Render()
        
        print(self.timer_count + self.first_step)
        
        self.timer_count += 1

