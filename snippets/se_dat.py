"""
This file saves measurement data based on the AC/DC state estimation
"""

import andes
from andes.utils.math import polar

andes.main.config_logger()

case_file_path = '../../andes_cases/curent/NA_BASE.dm'

na = andes.main.run(case_file_path, routine=['pflow'])

v_mag = na.dae.y[na.Bus.v]
v_ang = na.dae.y[na.Bus.a]
v_polar = polar(v_mag, v_ang)
v_real = v_polar.real()
v_imag = v_polar.imag()

ac_measurement = []
dc_measurement = []

# Bus V_Real section
ac_measurement.append('{:g}'.format(na.Bus.n) + '\n')
for idx, item in zip(na.Bus.idx, v_real):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(idx), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)

# Bus V_Imag section
ac_measurement.append(str(na.Bus.n) + '\n')
for idx, item in zip(na.Bus.idx, v_imag):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(idx), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)

# Line I_Real section
ac_measurement.append(str(na.Line.n * 2) + '\n')
# from bus1 to bus2
for bus1, bus2, item in zip(na.Line.bus1, na.Line.bus2, na.Line.I1_real):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(bus1), '{:g}'.format(bus2), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)
# from bus2 to bus1
for bus1, bus2, item in zip(na.Line.bus1, na.Line.bus2, na.Line.I2_real):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(bus2), '{:g}'.format(bus1), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)

# Line I_Imag section
ac_measurement.append(str(na.Line.n * 2) + '\n')
# from bus1 to bus2
for bus1, bus2, item in zip(na.Line.bus1, na.Line.bus2, na.Line.I1_imag):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(bus1), '{:g}'.format(bus2), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)
# from bus2 to bus1
for bus1, bus2, item in zip(na.Line.bus1, na.Line.bus2, na.Line.I2_imag):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(bus2), '{:g}'.format(bus1), item, 0.001, 0]) + '\n'
    ac_measurement.append(line_data)

ac_measurement.append('0')

with open('AC_Measurement.dat', 'w') as f:
    f.writelines(ac_measurement)

# DC Node Voltage
dc_measurement.append('{:g}'.format(na.Node.n) + '\n')
for idx, item in zip(na.Node.idx, na.dae.y[na.Node.v]):
    line_data = '\t'.join(str(i) for i in ['{:g}'.format(idx), item, 0.001, 0]) + '\n'
    dc_measurement.append(line_data)

# DC Line currents from `R`, `L`, `RLp`, `RCp`, `RLCp`
comp_list = ['R', 'L', 'RLs', 'RCp', 'RLCp']
n_lines = 0
dc_measurement_line_section = []
for comp_name in comp_list:
    comp = na.__dict__[comp_name]
    for node1, node2, item in zip(comp.node1, comp.node2, na.dae.y[comp.Idc]):
        n_lines += 1
        line_data = '\t'.join(str(i) for i in ['{:g}'.format(node1),
                                               '{:g}'.format(node2), item, 0.001, 0]) + '\n'
        dc_measurement_line_section.append(line_data)

dc_measurement.append(str(n_lines) + '\n')
dc_measurement.extend(dc_measurement_line_section)

dc_measurement.append('0')

with open('DC_Measurement.dat', 'w') as f:
    f.writelines(dc_measurement)
