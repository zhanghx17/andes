"""
Filter for IEEE CDF format
"""

from ..consts import rad2deg  # NOQA
import datetime
import logging
logger = logging.getLogger(__name__)


def testlines(file):
    ret = False

    with open(file, 'r') as fid:
        fid.readline()
        second_line = fid.readline()
        if 'BUS DATA' in second_line:
            ret = True

    return ret


def read(file, system, header=True):
    pass


def write(file, system):
    out = []
    year = datetime.datetime.now().strftime("%Y")
    date = datetime.datetime.now().strftime("%m/%d/%y")
    title = ' {0:<8}{1:<20}{2:<6}{3:<4}{4:<1}{5:<28}'.format(date,
                                                             'ANDES CASE DUMP',
                                                             '100',
                                                             year,
                                                             'S',
                                                             'NONE')
    out += title + '\n'

    bus_line = '{0:<6} {1:<10} {2:<2} {3:<3} {4:<2} ' \
               '{5:<6} {6:<7} {7:<9} {8:<10} {9:<8} ' \
               '{10:<8} {11:7} {12:6} {13:8} {14:8} ' \
               '{15:8} {16:8} {17:4}'

    for idx, bus in enumerate(system.Bus.idx):  # NOQA

        mva = system.mva
        name = system.Bus.get_field('name', bus)
        area = system.Bus.get_field('area', bus)
        zone = system.Bus.get_field('zone', bus)
        basekV = system.Bus.get_field('Vn', bus)
        bus_type = -1
        voltage = system.dae.y[system.Bus.v[idx]]
        angle = system.dae.y[system.Bus.a[idx]] * rad2deg

        # initial values to be overwritten
        loadp = 0
        loadq = 0
        genp = 0
        genq = 0
        shuntg = 0
        shuntb = 0
        desired_volts = 1

        pq_idx = system.PQ.on_bus(idx)
        if pq_idx:
            loadp = system.PQ.get_field('p', pq_idx) * mva
            loadq = system.PQ.get_field('q', pq_idx) * mva
            bus_type = 0
        pv_idx = system.PV.on_bus(idx)
        if pv_idx:
            genp = system.PV.get_field('pg', pv_idx) * mva
            desired_volts = system.PV.get_field('v0', pv_idx)
            bus_type = 2
        sw_idx = system.SW.on_bus(idx)
        if sw_idx:
            desired_volts = system.SW.get_field('v0', sw_idx)
            bus_type = 3

        vmax = 1.1
        vmin = 0.9
        shunt_idx = system.Shunt.on_bus(idx)
        if shunt_idx:
            shuntb = system.Shunt.get_field('b', idx)
            shuntg = system.Shunt.get_field('g', idx)
        remote = 0

        out += bus_line.format(bus, name, area, zone, bus_type,
                               voltage, angle, loadp, loadq,
                               genp, genq, basekV, desired_volts,
                               vmax, vmin, shuntb, shuntg, remote)
        pass

    with open(file, 'w') as f:  # NOQA
        pass
