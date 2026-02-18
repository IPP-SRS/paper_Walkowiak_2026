'''
Master script to generate input, run calculations and collect results of the bt scan
06.2025 Walkowiak
'''
from stellarator_analysis.scripts import generate_input, run_cases, collect_results
import os

case_name = 'results'
prefix = 'squid'

workdir = os.path.dirname(os.path.realpath(__file__))

generate_input.main(case_name,
                    prefix = prefix,
                    var_name='f_st_coil_aspect',
                    var_min=0.8,
                    var_max=1.2,
                    step=0.05,
                    workdir=workdir,
                    clean_start=False,
                    var_short_name='Ac')

run_cases.main(case_name, prefix=prefix, workdir=workdir)

collect_results.main(case_name, 
                     prefix=prefix, 
                     param_x='f_st_coil_aspect', 
                     param_y='rmajor', 
                     workdir=workdir)
