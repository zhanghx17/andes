"""
Filter for IEEE CDF format
"""

from ..consts import rad2deg  # NOQA
import datetime
import logging
logger = logging.getLogger(__name__)

end_of_block = '-999\n'


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
                                                             ' NONE')
    out.append(title + '\n')

    out.extend(get_bus_data(system))
    out.extend(get_line_data(system))
    out.extend(get_zone_data(system))
    out.extend(get_interchange_data(system))
    out.extend(get_tielines_data(system))
    out.extend(get_node_data(system))

    out.append('END OF DATA\n')

    with open(file, 'w') as f:  # NOQA
        f.writelines(out)

    return True


def get_line_data(system):
    """
    Prepare line data and return as a list containing formatted lines

    Parameters
    ----------
    system

    Returns
    -------

    """
    out = []
    line_header = '{0:<44s} {1:<6g} ITEMS'.format('BRANCH DATA FOLLOWS', system.Line.n) + '\n'
    out.append(line_header)

    line_tpl = '{0:<4g} {1:4g} {2:2g} {3:<2g} {4} {5} ' \
               '{6:<10g} {7:10g} {8:10g} {9:5g} {10:5g} ' \
               '{11:5g} {12:4g} {13} {14:6g} {15:6g} ' \
               '{16:6g} {17:6g} {18:6g} {19:6g} {20:6g}'

    for idx, line in enumerate(system.Line.idx):
        bus1 = system.Line.get_field('bus1', line)
        bus2 = system.Line.get_field('bus2', line)
        area = 1
        zone = 1
        circuit = 1
        line_type = 0
        r = system.Line.get_field('r', line)
        x = system.Line.get_field('x', line)
        b = system.Line.get_field('b', line)
        ratea = 0
        rateb = 0
        ratec = 0
        control_bus = 0
        side = 0
        tap = system.Line.get_field('tap', line)
        phi = system.Line.get_field('phi', line)
        maxtap = 0
        mintap = 0
        step_size = 0
        vmin = 0.9
        vmax = 1.1

        line_formatted = line_tpl.format(bus1, bus2, area, zone, circuit,
                                         line_type, r, x, b,
                                         ratea, rateb, ratec, control_bus,
                                         side, tap, phi, maxtap, mintap, step_size,
                                         vmin, vmax
                                         )
        out.append(line_formatted + '\n')

    out.append(end_of_block)

    return out


def get_zone_data(system):
    out = []
    zone_header = '{0:<44s} {1:<6g} ITEMS'.format('LOSS ZONE FOLLOWS', system.Zone.n) + '\n'
    out.append(zone_header)

    zone_tpl = '{0:<4} {1:<20}'

    for item in system.Zone.idx:
        name = system.zone.get_field('name', item)
        zone_formatted = zone_tpl.format(item, name)
        out.append(zone_formatted + '\n')

    out.append(end_of_block)
    return out


def get_interchange_data(system):
    out = []
    ic_header = '{0:<44s} {1:<6g} ITEMS'.format('INTERCHANGE DATA FOLLOWS', 0) + '\n'
    out.append(ic_header)
    out.append('-9\n')

    return out


def get_tielines_data(system):
    out = []
    tieline_header = '{0:<44s} {1:<6g} ITEMS'.format('TIE LINES FOLLOWS', 0) + '\n'
    out.append(tieline_header)
    out.append('-9\n')

    return out


def get_bus_data(system):
    """
    Prepare bus data and return as a list containing formatted lines

    Parameters
    ----------
    system
        Power system instance

    Returns
    -------
    list

    """

    out = []
    bus_header = '{0:<44s} {1:<6g} ITEMS'.format('BUS DATA FOLLOWS', system.Bus.n) + '\n'
    out.append(bus_header)

    bus_line = '{0:<6g} {1:<10} {2:<2} {3:<3} {4:<2} ' \
               '{5:<6} {6:<7} {7:<9g} {8:<10g} {9:<8g} ' \
               '{10:<8g} {11:7g} {12:6g} {13:8g} {14:8g} ' \
               '{15:8g} {16:8g} {17:4}'

    for idx, bus in enumerate(system.Bus.idx):  # NOQA

        mva = system.mva
        name = system.Bus.get_field('name', bus)
        area = system.Bus.get_field('area', bus)
        zone = system.Bus.get_field('zone', bus)
        basekV = system.Bus.get_field('Vn', bus)
        bus_type = -1
        # voltage = system.dae.y[system.Bus.v[idx]]
        # angle = system.dae.y[system.Bus.a[idx]] * rad2deg

        voltage = system.Bus.get_field('voltage', bus)
        angle = system.Bus.get_field('angle', bus) * rad2deg

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
            shuntb = system.Shunt.get_field('b', shunt_idx)
            shuntg = system.Shunt.get_field('g', shunt_idx)
        remote = 0

        bus_line_formatted = bus_line.format(bus, name, area, zone, bus_type,
                                             voltage, angle, loadp, loadq,
                                             genp, genq, basekV, desired_volts,
                                             vmax, vmin, shuntb, shuntg, remote) + '\n'
        out.append(bus_line_formatted)

    out.append(end_of_block)
    return out


def get_node_data(system):
    """
    Return dc node data

    Parameters
    ----------
    system

    Returns
    -------

    """

    out = []

    node_tpl = '{0:<6g} {1:<12} {2:<2} {3:<2} {4:<2} ' \
               '{5:<2} {6:<8g} {7:<8g} {8:<8g}'

    for item in system.Node.idx:
        node_idx = item
        name = system.Node.get_field('name', item)
        vdc = system.Node.get_field('voltage', item)
        vdcn = system.Node.get_field('Vdcn', item)

        node_formatted = node_tpl.format(node_idx, name, 1, 1, 1,
                                         vdc, 0, vdcn)

        out.append(node_formatted + '\n')

    out.append(end_of_block)

    return out


def get_dcline_data(system):
    """
    Return dc line data in a list of strings

    Parameters
    ----------
    system

    Returns
    -------

    """
    comp_list = ['R', 'L', 'RLs', 'RCp', 'RLCp']

    for comp_name in comp_list:
        comp = system.__dict__[comp_name]
        for item in comp.idx:
            # node1 = comp.get_field('node1', item)
            # node2 = comp.get_field('node2', item)
            pass
