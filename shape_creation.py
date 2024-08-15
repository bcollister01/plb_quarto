"""Script to create all the 3D shapes. Takes around 10-15s to run."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for cuboids
height_fac_tall = 3
stretch_out_factor = 1.5

color_ops = ['orange','cyan']
shape_ops = ['cuboid','cylinder']
height_ops = ['tall','small']
stripe_ops = ['striped','plain']

def get_cube(stretch_out_factor):   
    phi = np.arange(1,50,2)*np.pi/4
    Phi, Theta = np.meshgrid(phi, phi)
    x = stretch_out_factor*np.cos(Phi)*np.sin(Theta)
    y = stretch_out_factor*np.sin(Phi)*np.sin(Theta)
    z = stretch_out_factor*np.cos(Theta)/np.sqrt(2)
    return x,y,z

def get_cylinder(height):
    #height = [-2,1.95]
    if height=="tall":
        zs = np.linspace(-2, 1.95, 2)
    else:
        zs = np.linspace(0, 1.5, 2)
        
    us = np.linspace(0, 2 * np.pi, 128)
   
    
    us, zs = np.meshgrid(us, zs)
    xs = 1 * np.cos(us)
    ys = 1 * np.sin(us)
    #plot a circle on top of this to get rid of the white space
    
    return xs, ys, zs
        
for color_var in color_ops:
    for stripe_var in stripe_ops:
        for height_var in height_ops:
            for shape_var in shape_ops:

                if stripe_var == 'striped':
                    hatch_type = r"/"
                else:
                    hatch_type = ""
                if height_var == "tall": #height_fac only works for cuboid
                    height_fac = height_fac_tall
                else:
                    height_fac = 1
                    
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                if shape_var=='cuboid':
                    x,y,z = get_cube(stretch_out_factor)
                    ax.plot_surface(x, y, z*height_fac, alpha=1, color=color_var, hatch=hatch_type)
                else:
                    x,y,z = get_cylinder(height_var)
                    ax.plot_surface(x, y, z, alpha=1, color=color_var, hatch=hatch_type)

                
                 
                # ax.view_init(0, 60)
                ax.axis('off')
                
                ax.set_xlim(-2,2)
                ax.set_ylim(-2,2)
                ax.set_zlim(-2,2)
                
                # plt.show()

                plt.savefig(f'pieces/{color_var}_{shape_var}_{height_var}_{stripe_var}.png', dpi = 400, transparent = True)