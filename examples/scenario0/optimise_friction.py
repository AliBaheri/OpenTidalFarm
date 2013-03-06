''' Plots the power ouput of a single turbine for different fricition values. (see also test_optimal_friction_single_turbine) '''
import numpy
from opentidalfarm import *
set_log_level(ERROR)

basin_x = 640.
basin_y = 320.

# We set the perturbation_direction with a constant seed, so that it is consistent in a parallel environment.
config = ScenarioConfiguration("mesh.xml", inflow_direction = [1, 0])
config.params['automatic_scaling'] = False

# Place one turbine 
offset = 0.0
turbine_pos = [[basin_x/3 + offset, basin_y/2 + offset]] 
info_green("Turbine position: " + str(turbine_pos))
config.set_turbine_pos(turbine_pos)
config.params['controls'] = ['turbine_friction']

# Use a negative scaling factor as we want to maximise the power output
rf = ReducedFunctional(config, scaling_factor = -1)
m0 = rf.initial_control()

minimize(rf)
