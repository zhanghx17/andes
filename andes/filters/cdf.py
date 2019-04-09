"""
Filter for IEEE CDF format
"""

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

    for bus in system.Bus.idx:  # NOQA
        bus_line
        pass

    with open(file, 'w') as f:  # NOQA
        pass
