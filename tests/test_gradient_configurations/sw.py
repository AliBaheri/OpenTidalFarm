''' This example optimises the position of three turbines using the hallow water model. '''

import sys
from configuration import * 
import numpy
from dirichlet_bc import DirichletBCSet
import IPOptUtils
import ipopt
from helpers import test_gradient_array
from animated_plot import *
from reduced_functional import ReducedFunctional
from dolfin import *
set_log_level(PROGRESS)
numpy.random.seed(21)

for c in [DefaultConfiguration, PaperConfiguration, ConstantInflowPeriodicSidesPaperConfiguration]:
    info_green("Testing configuration " + c.__name__)
    config = c(nx = 15, ny = 15)
    config.params['finish_time'] = config.params["start_time"] + 2*config.params["dt"]

    # The turbine position is the control variable 
    turbine_pos = [] 
    border_x = config.params["basin_x"]/10
    border_y = config.params["basin_y"]/10

    # For >1 turbine
    for x_r in numpy.linspace(0.+border_x, config.params["basin_x"]-border_x, 2):
        for y_r in numpy.linspace(0.+border_y, config.params["basin_y"]-border_y, 2):
          turbine_pos.append((float(x_r), float(y_r)))

    config.set_turbine_pos(turbine_pos)
    info_blue("Deployed " + str(len(turbine_pos)) + " turbines.")

    model = ReducedFunctional(config, scaling_factor = 10**-6)
    m0 = model.initial_control()

    p = numpy.random.rand(len(m0))
    minconv = test_gradient_array(model.j, model.dj, m0, seed = 0.1, perturbation_direction = p, plot_file = "convergence_" + c.__name__ + ".pdf")
    if minconv < 1.9:
        info_red("The gradient taylor remainder test failed.")
        sys.exit(1)
    else:
        info_green("The gradient taylor remainder test passed.")
