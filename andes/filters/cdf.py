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
    out += title

    bus_line = '{0:<6} {1:<10} {2:<2} {3:<3} {4:<2} ' \
               '{5:<6} {6:<7} {7:<9} {8:<10} {9:<8} ' \
               '{10:<8} {11:7} {12:6} {13:8} {14:8} ' \
               '{15:8} {16:8} {17:4}'

    for idx, bus in enumerate(system.Bus.idx):  # NOQA

        # mva = system.mva
        # name = system.Bus.get_field('name', bus)
        # area = system.Bus.get_field('area', bus)
        # zone = system.Bus.get_field('zone', bus)
        # bus_type = -1
        # voltage = system.dae.y[system.Bus.v[idx]]
        # angle = system.dae.y[system.Bus.a[idx]] * rad2deg
        # loadp = 0
        # loadq = 0
        # genp = 0
        # genq = 0
        # basekV = 0

        bus_line
        pass

    with open(file, 'w') as f:  # NOQA
        pass
