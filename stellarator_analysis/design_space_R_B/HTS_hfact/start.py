'''
Master script to generate input, run calculations and collect results of the bt scan
06.2025 Walkowiak
'''
from stellarator_analysis.scripts import generate_input, run_cases, collect_results
import os

case_name = 'results'
prefix = 'squid'

# case_name = 'rebuild'
# prefix = 'rebuild'

# case_name = 'updated_beta5'
# prefix = 'updated'

workdir = os.path.dirname(os.path.realpath(__file__))

generate_input.main(case_name,
                    prefix = prefix,
                    var_name='b_plasma_toroidal_on_axis',
                    var_min=5,
                    var_max=9,
                    step=0.25,
                    workdir=workdir,
                    clean_start=False,
                    var_short_name='B')

run_cases.main(case_name, prefix=prefix, workdir=workdir)

collect_results.main(case_name, 
                     prefix=prefix, 
                     param_x='b_plasma_toroidal_on_axis', 
                     param_y='coe', 
                     workdir=workdir)
