# for voxelisation
# INSTALLATION OF THE VOXSURF PACKAGE:
# 1. Make sure Visual Studio (or at least MSVC) is installed for Windows users.
# 2. In the folder where you will work on the stl-to-voxel related tasks ($PATH$) run the following commands:
# 	--- IN GIT BASH ---
# 	git clone https://github.com/cakepirate/VoxSurf.git
# 	--- IN ANACONDA PROMPT ---
# 	$Activate the python environment (optional)
# 	cd $PATH 
# 	pip install .   OR   python setup.py clean --all install
import pyvoxsurf
import numpy as np

# for visualisation
import pyvista as pv
import matplotlib.pyplot as plt
######### for debugging and testing
import time
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""
class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
#####################


def plotVox(vol, tool='pyvista', type=0):
    if tool == 'pyvista':
        p = pv.Plotter()
        mvolume1 = pv.wrap(vol)
        p.add_mesh_threshold(mvolume1, color=True, show_edges=True)
        p.show()
    elif tool == 'matplotlib':
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        cmap = plt.get_cmap("Greys")
        norm= plt.Normalize(vol.min(), vol.max())
        if type == 0:
            ax.voxels(volume1, facecolors=cmap(norm(volume1)), edgecolor='grey')                              # not plotting the element if the value is 0
        elif type == 1:
            ax.voxels(np.ones_like(volume1), facecolors=cmap(norm(volume1)), edgecolor="grey")   # plotting all elements including the 0 ones [Not desirable for us]
        ax.set_box_aspect(volume1.shape)                                              # Plot in uniform aspect ratio (shape convention x,y,z)
        plt.show()
    else:
        print("Unrecognised command, select 'pyvista' or 'matplotlib' as visualisation tool")



t = Timer()
filePath = 'test/ai5206_thermocouple_test_block.stl'

t.start()
# USING CPP
volume1 = pyvoxsurf.voxelize_stl(filePath,120,[],'Inside')
print('Cpp Voxelised.')
t.stop()
## Visualise the voxelised stl
plotVox(volume1, 'pyvista')

# USING PYVISTA
# Load mesh and texture into PyVista
mesh = pv.read(filePath)
density = mesh.length / 200
t.start()
voxels = pv.voxelize(mesh, density, check_surface=False)
print('PyVista Voxelised.')
t.stop()

# Direct comparison between cpp and pyvista
pl = pv.Plotter(shape=(1, 2))

# PyVista
pl.subplot(0, 0)
pl.add_mesh(voxels, color=True, show_edges=True)
# Cpp
pl.subplot(0,1)
mvolume1 = pv.wrap(volume1)
pl.add_mesh_threshold(mvolume1, color=True, show_edges=True)

# Link all four views so all cameras are moved at the same time
pl.link_views()
# Set camera start position
pl.camera_position = 'xy'
# Show everything
pl.show()

print(volume1.shape)