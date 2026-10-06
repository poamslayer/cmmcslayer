# G-code, 4471C, Op 10

File: `4471C_OP10.NC`, exported from Tom Reyes's post-processor for the Haas VF-2, carried on a USB stick to SHOP-PC-01 and from there to the Haas.

## Comment header

```
(4471-003 REV C OP10 - MERIDIAN - PROGRAM CHOLLA)
(MATERIAL: 6061-T6, STOCK 3.000 DIA)
(TOOL LIST:)
(T1 - 0.750 FACE MILL)
(T2 - 0.500 END MILL, 4 FLUTE)
(T3 - 0.312 DRILL)
(T4 - 0.250 END MILL, 4 FLUTE)
(T5 - EDGE FINDER)
```

## First 40 lines

```
%
O4471
(4471-003 REV C OP10 - MERIDIAN - PROGRAM CHOLLA)
G20
G17 G40 G80 G90
T1 M06
G43 H01 Z1.0
S3500 M03
G54
G00 X0. Y0.
G01 Z0.1 F20.
G01 Z-0.05 F8.
X1.25 Y0. F12.
X1.25 Y0.866
X0.625 Y1.0825
X0. Y0.866
X0. Y0.
G00 Z1.0
T2 M06
G43 H02 Z1.0
S6000 M03
G00 X0.625 Y0.5
G01 Z-0.1 F6.
G02 X0.625 Y0.5 I0.625 J0. F10.
G00 Z1.0
X-0.625 Y0.5
G01 Z-0.1 F6.
G02 X-0.625 Y0.5 I-0.625 J0. F10.
G00 Z1.0
T3 M06
G43 H03 Z1.0
S4200 M03
G81 X0.5 Y0.5 Z-0.4 R0.1 F8.
X-0.5 Y0.5
X0.5 Y-0.5
X-0.5 Y-0.5
G80
M09
G00 Z1.0
```

The toolpaths follow the bore diameter, the mounting hole pattern, and the flange profile taken directly from Drawing 4471-003 Rev C. Op 10 produces the recognizable bracket profile with the mounting hole pattern already present, so this operation is not an unfinished part with no customer geometry.
