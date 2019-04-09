"""
This file saves measurement data based on the AC/DC state estimation
"""

import andes

andes.main.config_logger()

case_file_path = '/home/hcui7/repos/andes_cases/curent/NA_BASE.dm'

na = andes.main.run(case_file_path)


v_mag = na.dae.y[na.Bus.v]
v_ang = na.dae.y[na.Bus.a]
