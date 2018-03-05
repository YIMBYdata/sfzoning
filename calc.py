import math

ZONING = """
RH-1(D)	4000
RH-1	3000
RH-1(S)	1500
RH-2	1500
RH-3	1000
RM-1	800
RM-2	600
RM-3	400
RM-4	200
RC-3	400
RC-4	200
RCD	0
RTO	0
RTO-M	0
RH DTR	0
SB-DTR	0
TB DTR	0
WMUO	1.00E+09
WMUG	0
UMU	0
RED	0
RED-MX	0
MUO	0
MUG	0
MUR	0
SSO	200
NC-1	800
NC-2	800
NC-3	600
NC-S	800
NCD-POLK	400
NCD-UPPER FILLMORE	600
NCD-EXCELSIOR	600
NCD-WEST PORTAL	800
NCD-PACIFIC	1000
NCD-TARAVAL	800
NCD-SACRAMENTO	800
NCD-INNER CLEMENT	600
NCD-BROADWAY	400
NCD-HAIGHT	600
NCD-IRVING	800
NCD-CASTRO	600
NCD-UNION	600
NCD-INNER SUNSET	800
NCD-NORIEGA	800
NCD-NORTH BEACH	400
NCD-OUTER CLEMENT	600
NCD-JUDAH	800
NCD-UPPER MARKET	0
NCD-JAPANTOWN	400
NCD-24TH-NOE-VALLEY	600
NCT-FILLMORE	0
NCT-MISSION	0
NCT-HAYES	0
NCT-SOMA	0
NCT-OCEAN	0
NCT-UPPER MARKET	0
NCT-DIVISADERO	0
NCT-24TH-MISSION	0
NCT-GLEN PARK	0
NCT-FOLSOM	0
NCT-VALENCIA	0
NCT-1	0
NCT-2	0
NCT-3	0
C-2	1.00E+09
C-3-G	1.00E+09
C-3-O	1.00E+09
C-3-O(SD)	1.00E+09
C-3-R	1.00E+09
C-3-S	1.00E+09
M-1	1.00E+09
M-2	1.00E+09
PDR-1-B	1.00E+09
PDR-1-D	1.00E+09
PDR-1-G	1.00E+09
PDR-2	1.00E+09
SALI	1.00E+09
SLI	1.00E+09
CCB	200
CRNC	200
CVR	200
HP-RA	0
MB-O	1.00E+09
MB-OS	1.00E+09
MB-RA	0
PM-OS	1.00E+09
PM-S	1.00E+09
PM-CF	1.00E+09
PM-MU1	1.00E+09
PM-MU2	1.00E+09
PM-R	0
SPD	0
P	1.00E+09
"""


lot_size_per_unit = {}
for l in ZONING.split('\n'):
    if l.strip():
        code, numstring = l.split('\t')
        lot_size_per_unit[code] = float(numstring)


LOT_SIZE_PER = 2500.0
AVG_APT_SIZE = 800.0


def units_per_2500sqft(zone):
    fixed = {
        'P': -1,  # parks are < 0
        'RH-1(D)': 1.0 * (LOT_SIZE_PER / 4000),  # minimum lot size 4000 sq ft
        'RH-1': 1,
        'RH-1(S)': 2,
        'RH-2': 2,
        'RH-3': 3,
    }
    n = fixed.get(zone)
    if n is not None:
        return n

    lot_size = lot_size_per_unit[zone]

    if lot_size > 1e6:
        return 0
    if lot_size == 0:
        return 1e9
    return LOT_SIZE_PER / lot_size


def units_per_height(height_code, height_num):
    if 'OS' in height_code:
        return -1

    sq_ft = LOT_SIZE_PER * .8  # 80% efficiency

    apts_per_floor = sq_ft / AVG_APT_SIZE
    floors = math.floor(height_num / 10.0)

    return apts_per_floor * floors

COLORS = """
-1	gray
0	#3b0000
0.625	#6d0003
1	#950004
2	#c60003
2.5	#ff0000
3	#ff6e00
3.125	#ff8300
4.166666667	#ffbb00
5	#ffff00
6.25	#deec00
7.5	#bed900
10	#9ec500
12.5	#7eb100
15	#609e00
17.5	#428c00
20	#207700
22.5	#006400
"""

colors = {}
for l in COLORS.split('\n'):
    if l.strip():
        units, color = l.split('\t')
        colors[int(1000*float(units))] = color


def color(units):
    if units > 20:
        return colors[int(22.5*1000)]
    return colors[int(units*1000)]
