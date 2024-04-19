## By: Guy Soffer (GSOF) 22/Feb/2024
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = ""
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

import math, copy
pi = math.pi

def radToDeg(rad) -> float:
    """ Convert radians to degrees """
    return 180*rad/pi # or use this math.degrees(rad)

def modulu(val, modulu):
    """ Returns the modulus of val%modulu """
    while val > modulu:
        val -= modulu
    while val < -modulu:
        val += modulu
    return val
    
def clip(val, Min, Max) -> float:
    """ Return the cliped (clamp) result of the input value """
    if val < Min:
        val = Min
    elif val > Max:
        val = Max
    return val

def int_V2(v) -> list:
    return int(v[0]), int(v[1])

def int_V3(v) -> list:
    return int(v[0]), int(v[1]), int(v[2])

def intV(v) -> list:
    out = [0]*len(v)
    for i, elm in enumerate(v):
        out[i] = int(elm)
    return out

def scale_V2(v, s) -> list:
    return v[0] * s, v[1] * s

def scale_V3(v, s) -> list:
    return v[0] * s, v[1] * s, v[2] * s

def negR_V2(R) -> list:
    """ TBR """
    R[0][1] *= -1
    R[1][0] *= -1
    return R

def absV_V2(V) -> float:
    """ Return the magnitude of 2D vector """
    return math.sqrt((V[0]**2) +(V[1]**2))

def angle_V2(V) -> float:
    """ Return the angle of 2D vector """
    return math.atan2(V[1], V[0])

def polar_V2(V) -> float:
    """ Return the polar coordinates of 2D vector """
    return [absV(V), angleV(V)]

def rotation_V2(rad, V) -> list:
    #sinX = math.sin(rad)
    #cosX = math.cos(rad)
    #DCM = ((cosX, -sinX), (sinX, cosX))
    return mul_M2x2(DCM_2D(rad), V)
    
def absV_V3(V) -> float:
    """ Return the magnitude of 2D vector """
    return math.sqrt((V[0]**2) +(V[1]**2) +(V[2]**2))

def angle_V3(v) -> list:
    r = absV3(v)
    _absV2 = absV2( v[0:2] )
    elevation = pi / 2.0                          #< For case 0 and 1
    #elevation = 0.0                                  #< For case2
    if _absV2 > 0.001:
        elevation = math.arctan( v[2] / _absV2 )  #< Case1 - https://keisan.casio.com/exec/system/1359533867 (Passed targeting test)
        #elevation = -math.arctan2( _absV2, v[2]) +pi/2  #< Case2 - https://keisan.casio.com/exec/system/1359533867
        #elevation = math.arcsin( r / v[2])               #< Case3 - https://www.mechamath.com/trigonometry/cartesian-to-spherical-coordinates-formulas-and-examples/
    azimuth = math.arctan2(v[1], v[0])
    return azimuth, elevation, r

def cartesianToPolar_V3(pos):
    return angleV3(pos)

def polarToCartesian_V3(azimuth, elevation, distance):
    abs_xy = distance * math.cos(elevation)
    x = abs_xy * math.cos(azimuth)
    y = abs_xy * math.sin(azimuth)
    z = distance * math.sin(elevation)
    return x, y, z

def DCM_V2(rad) -> list:
    """ Return the 2D rotation matrix """
    cosA = math.cos(rad)
    sinA = math.sin(rad)
    return [[cosA,-sinA],[sinA,cosA]]

### https://en.wikipedia.org/wiki/Rotation_matrix
def DCM_ZYX(a, b, c) -> list:
    """ a is around Z, b is around Y, and c is around X"""
    ca = math.cos(a)
    cb = math.cos(b)
    cc = math.cos(c)
    
    sa = math.sin(a)
    sb = math.sin(b)
    sc = math.sin(c)
    DCM = [ [ca*cb, ca*sb*sc-sa*cc, ca*sb*cc+sa*sc],
            [sa*cb, sa*sb*sc+ca*cc, sa*sb*cc-ca*sc],
            [ -sb,       cb*sc,          cb*cc    ]]
    return DCM

def DCM_XYZ(a, b, c) -> list:
    """ a is around X, b is around Y, and c is around Z"""
    ca = math.cos(a)
    cb = math.cos(b)
    cc = math.cos(c)
    
    sa = math.sin(a)
    sb = math.sin(b)
    sc = math.sin(c)
    DCM = [ [    cb*cc,           -cb*sc,        sb  ],
            [ca*sc+sa*sb*cc,  ca*cc-sa*sb*sc,  -sa*cb],
            [sa*sc-ca*sb*cc,  sa*cc+ca*sb*sc,   ca*cb]]
    return DCM

def MxV_2x2(M,V) -> list:
    """ Return the result of 2x2 matrix and 2D vector multiplication """
    O = [0,0]
    O[0] = M[0][0]*V[0] +(M[0][1]*V[1])
    O[1] = M[1][0]*V[0] +(M[1][1]*V[1])    
    return O

def MxV(M,V) -> list:
    """ Return the result of NxM matrix and V vector multiplication """
    N = len(M)
    O = [0]*N
    for r,row in enumerate(M):
        for m,v in zip(row,V):
            O[r] += m*v
    return O

def getCol(M, col) -> list:
    """ Returns a copy of column 'col' from the matrix 'M' """
    rows = len(M)
    V = [0]*rows
    for i, row in enumerate(M):
        V[i] = row[col]
    return V

def getRow(M, row) -> list:
    """ Returns a copy of row 'row' from the matrix 'M' """
    return copy.copy(M[row])

def MUL_3x3(M, V):
    return [ M[0][0]*V[0] +M[0][1]*V[1] +M[0][2]*V[2],
             M[1][0]*V[0] +M[1][1]*V[1] +M[1][2]*V[2],
             M[2][0]*V[0] +M[2][1]*V[1] +M[2][2]*V[2] ]

def MxM(M1, M2) -> list:
    """ Return the result two matrix multiplication """
    rows = len(M2) #< If vector instead of matrix make a matrix
    try:
        colsM2 = len(M2[0])
    except:
        M2 = [M2]
        rows = 1

    try:           #< If vector instead of matrix make a matrix
        cols = len(M1[0])
    except:
        cols = len(M1)
        M1 = [M1]

    if cols == rows:
        rows = len(M1)
        cols = len(M2[0])
        O = zeros(rows, cols) #< The output
        for r in range(0,rows):
            row = getRow(M1, r)
            for c in range(0, cols):
                col = getCol(M2, c)
                O[r][c] = VxV(row, col)
        return O
    else:
        return [0]

def add_V2(V1, V2) -> list:
    """ Return the result of 2D vector addition """
    return [V1[0]+V2[0], V1[1]+V2[1]]

#def addV(V1, V2) -> list:
#    out = [0]*len(V1)
#    for i, elm1, elm2 in enumerate(zip(V1,V2)):
#        out[i] = elm1+elm2
#    return out

def addV(V1, V2) -> list:
    """ Return the result of vector addition """
    O = [0]*len(V1)
    i = 0
    for v1,v2 in zip(V1, V2):
        O[i] = v1+v2
        i += 1
    return O

def absV(V) -> float:
    """ Return the magnitude of vector """
    s2 = 0
    for v in V:
        s2 += v**2
    return math.sqrt(s2)

def scaleV(V, s) -> list:
    """ Return the scaled vector 'V' by the scaler 's' """
    O = [0]*len(V)
    for i, e in enumerate(V):
        O[i] = e*s
    return O

def VxV(V1, V2) -> float:
    """ Returns the result of two vector multiplacation """
    Sum = 0
    for e1, e2 in zip(V1, V2):
        Sum += e1*e2
    return Sum

def matrix(rows, cols, val=0) -> list:
    """ Returns the rows by cols matrix M filled with value val """
    M = [0]*rows
    for row in range(0,rows):
        M[row] = [val]*cols
    return M

def zeros(rows, cols) -> list:
    """ Returns the rows by cols zero matrix Z """
    return matrix(rows, cols, val=0)

def ones(rows, cols) -> list:
    """ Returns the rows by cols zero matrix Z """
    return matrix(rows, cols, val=1)

def T(M) -> list:
    """ Returns the transposed Matrix of M """
    rows = len(M)
    try:
        cols = len(M[0])
    except:
        cols = rows
        rows = 1
        M = [M]
    O = [0]*cols
    for i in range(0,cols):
        O[i] = getCol(M,i)
    return O
    
def I(size) -> list:
    """ Returns the size by size identity matrix I """
    I = [0]*size
    for row in range(0,size):
        I[row] = [0]*size
        I[row][row] = 1
    return I
    
def invM(M) -> list:
    """ Not ready yet, Returns the inverse of the matrix M (Using Naive Gauss elimination method) """
    rows = len(M)
    cols = rows
    O = [0]*rows
    O[0] = copy.copy(M[0]) #scaleV(M[0], 1)
    for col in range(0, cols-1):
        stRow = col
        refRow = M[stRow]
        for i in range(stRow +1, rows):
            row = M[i]
            tmpRow1 = scaleV(refRow, -row[col])
            tmpRow2 = scaleV(row, refRow[col])
            O[i] = addV(tmpRow2, tmpRow1)
        M = copy.copy(O)
    return O

def LU(M) -> list:
    """ Not ready yet, Returns the lower and upper (LU) matrixes that forms the matrix M """
    rows = len(M)
    cols = rows
    L = I(rows)
    U = [0]*rows
    U[0] = copy.copy(M[0]) #scaleV(M[0], 1)
    for col in range(0, cols-1):
        stRow = col
        refRow = M[stRow]
        for i in range(stRow +1, rows):
            row = M[i]
            tmpRow1 = scaleV(refRow, -row[col])
            tmpRow2 = scaleV(row, refRow[col])
            L[i][col] = refRow[col]/row[col]
            U[i] = addV(tmpRow2, tmpRow1)
        M = copy.copy(U)
    return (L, U)

if __name__ == "__main__":
#    M = [[1,2,3,4],
#         [4,5,60,7],
#         [7,8,9,11],
#         [17,18,19,10],
#         ]
    M = [[1,2,3],
         [4,5,6],
         [7,8,11],
         ]

    #o = invM(M)
    l,u = LU(M)
