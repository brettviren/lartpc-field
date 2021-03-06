#!/usr/bin/envy python


import math
from units import mm, cm, um

def rextru(dx=20*cm, dy=20*cm, dz=1*cm, lcar=1.0*mm, **kwds):
    '''
    A rectangular extrusion centered at origin, extruded in Z direction.
    '''
    geostr='''
lcar={lcar};
dx={dx};
dy={dy};
dz={dz};
    '''.format(**locals())
    geostr += '''
Point(1) = { dx,  dy, -dz, lcar};
Point(2) = {-dx,  dy, -dz, lcar};
Point(3) = {-dx, -dy, -dz, lcar};
Point(4) = { dx, -dy, -dz, lcar};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Extrude{{0,0,2*dz}, {0,0,1}, {0,0,0}, 0}{ Line{1,2,3,4}; }
Mesh.Algorithm = 6;
    '''
    print geostr
    return geostr

def rectangle(dx=20*cm, dy=20*cm, lcar=1.0*mm, **kwds):
    '''
    A rectangle centered at the origin normal in Z direction.
    '''
    geostr='''
lcar={lcar};
dx={dx};
dy={dy};
'''.format(**locals())

    geostr += '''
Point(1) = { dx,  dy, 0.0, lcar};
Point(2) = {-dx,  dy, 0.0, lcar};
Point(3) = {-dx, -dy, 0.0, lcar};
Point(4) = { dx, -dy, 0.0, lcar};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line Loop(5) = {-1,-2,-3,-4};

Plane Surface(6) = {5};

Mesh.Algorithm = 6;
'''
    return geostr;


def cylinder(length=10.0*mm, radius=1.0*mm, lcar=1.0*mm, nsegments=6, extrurotang=0.0, **kwds):
    '''
    Return a gmsh geometry string for a capped cylinder along the Z axis from origin up to length.
    '''

    geostr = '''
radius = {radius};
length = {length};
lcar = {lcar};
'''.format(**locals())

    ipoint = 0
    for zed in [0, length]:
        angstep = 2*math.pi/nsegments
        for iseg in range(nsegments):
            ipoint += 1
            ang = angstep * iseg

            geostr += 'Point(%d) = {radius*Cos(%f), radius*Sin(%f), %f, lcar};\n' % (ipoint, ang, ang, zed)
        ipoint += 1
        geostr += 'Point(%d) = {0,0,%f};\n' % (ipoint, zed)

    icirc = 0
    for iplane in [0,1]:
        leap = nsegments*iplane
        icenter = (1+nsegments)*(iplane+1)

        for iseg in range(nsegments):
            icirc += 1

            icirc1 = iseg+1
            icirc2 = (icirc1)%nsegments+1

            icirc1 += leap + iplane
            icirc2 += leap + iplane
            geostr += 'Circle(%d) = {%d, %d, %d};\n' % (icirc, icirc1, icenter, icirc2)
        
    linenums = ','.join(["%d" % (x+1,) for x in range(nsegments)])
    geostr += 'Extrude{{0,0,length}, {0,0,1}, {0,0,0}, %f}{ Line{%s}; }\n' % (extrurotang, linenums)

    loop1 = ','.join([str(-1*(1+n)) for n in range(nsegments)])
    loop2 = ','.join([str(+1*(nsegments+1+n)) for n in range(nsegments)])

    geostr += 'Line Loop(%d) = {%s};\n' % (nsegments+1, loop1)
    geostr += 'Plane Surface(%d) = {%d};\n' % (nsegments+2, nsegments+1)

    geostr += 'Line Loop(%d) = {%s};\n' % (nsegments+3, loop2)
    geostr += 'Plane Surface(%d) = {%d};\n' % (nsegments+4, nsegments+3)

    geostr += 'Mesh.Algorithm = 6;\n'

    print geostr
    return geostr

def straw(length=10.0*mm, radius=1.0*mm, lcar=1.0*mm, nsegments=6, extrurotang=0.0, **kwds):
    '''
    Return a gmsh geometry string for a straw along the Z axis from origin up to length.
    '''

    geostr = '''
radius = {radius};
length = {length};
lcar = {lcar};
'''.format(**locals())

    angstep = 2*math.pi/nsegments
    for iseg in range(nsegments):
        ang = angstep * iseg
        
        geostr += 'Point(%d) = {radius*Cos(%f), radius*Sin(%f), 0, lcar};\n' % (iseg+1, ang, ang)
        geostr += 'Printf("{iseg} {ang} cos=%f sin=%f", Cos({ang}), Sin({ang}));\n'.format(ang=ang, iseg=iseg+1)
    icenter = nsegments+1
    geostr += 'Point(%d) = {0,0,0};\n' % icenter

    for iseg in range(nsegments):
        icirc1 = iseg+1
        icirc2 = (icirc1)%nsegments+1
        geostr += 'Circle(%d) = {%d, %d, %d};\n' % (icirc1, icirc1, icenter, icirc2)
        
    linenums = ','.join(["-%d" % (x+1,) for x in range(nsegments)])
    geostr += 'Extrude{{0,0,length}, {0,0,1}, {0,0,0}, %f}{ Line{%s}; }\n' % (extrurotang, linenums)
    geostr += 'Mesh.Algorithm = 6;\n'

    return geostr



def box(dx=1*mm, dy=20*cm, dz=20*cm, lcar=1.0*mm, **kwds):
    """Return a GMSH geo string for a box of half-lengths dx,dy,dz.  Box is
    centered at 0,0,0
    """
    #print 'box lcar: %d' % lcar

    geostr = '''
dx = {dx};
dy = {dy};
dz = {dz};
lcar = {lcar};
'''.format(**locals())
    geostr += '''
Point(1) = {-dx, -dy, -dz, lcar};
Point(2) = {+dx, -dy, -dz, lcar};
Point(3) = {-dx, +dy, -dz, lcar};
Point(4) = {+dx, +dy, -dz, lcar};
Point(5) = {+dx, +dy, +dz, lcar};
Point(6) = {+dx, -dy, +dz, lcar};
Point(7) = {-dx, +dy, +dz, lcar};
Point(8) = {-dx, -dy, +dz, lcar};
Line(1) = {3, 7};
Line(2) = {7, 5};
Line(3) = {5, 4};
Line(4) = {4, 3};
Line(5) = {3, 1};
Line(6) = {2, 4};
Line(7) = {2, 6};
Line(8) = {6, 8};
Line(9) = {8, 1};
Line(10) = {1, 2};
Line(11) = {8, 7};
Line(12) = {6, 5};
Line Loop(13) = {7, 8, 9, 10};
Plane Surface(14) = {13};
Line Loop(15) = {-6, -4, -5, -10};
Plane Surface(16) = {15};
Line Loop(17) = {3, 4, 1, 2};
Plane Surface(18) = {17};
Line Loop(19) = {12, -2, -11, -8};
Plane Surface(20) = {19};
Line Loop(21) = {-7, -12, -3, +6};
Plane Surface(22) = {21};
Line Loop(23) = {-9, 5, -1, 11};
Plane Surface(24) = {23};
Surface Loop(25) = {14, 22, 20, 18, 16, 24};
Mesh.Algorithm = 6;
'''
    return geostr



def invbox(dx=1*mm, dy=20*cm, dz=20*cm, lcar=1.0*mm, **kwds):
    """Return a GMSH geo string for a box of half-lengths dx,dy,dz.  Box is
    centered at 0,0,0
    """
    #print 'box lcar: %d' % lcar

    geostr = '''
dx = {dx};
dy = {dy};
dz = {dz};
lcar = {lcar};
'''.format(**locals())
    geostr += '''
Point(1) = {-dx, -dy, -dz, lcar};
Point(2) = {+dx, -dy, -dz, lcar};
Point(3) = {-dx, +dy, -dz, lcar};
Point(4) = {+dx, +dy, -dz, lcar};
Point(5) = {+dx, +dy, +dz, lcar};
Point(6) = {+dx, -dy, +dz, lcar};
Point(7) = {-dx, +dy, +dz, lcar};
Point(8) = {-dx, -dy, +dz, lcar};
Line(1) = {3, 7};
Line(2) = {7, 5};
Line(3) = {5, 4};
Line(4) = {4, 3};
Line(5) = {3, 1};
Line(6) = {2, 4};
Line(7) = {2, 6};
Line(8) = {6, 8};
Line(9) = {8, 1};
Line(10) = {1, 2};
Line(11) = {8, 7};
Line(12) = {6, 5};
Line Loop(13) = {-7, -8, -9, -10};
Plane Surface(14) = {13};
Line Loop(15) = {6, 4, 5, 10};
Plane Surface(16) = {15};
Line Loop(17) = {-3, -4, -1, -2};
Plane Surface(18) = {17};
Line Loop(19) = {-12, 2, 11, 8};
Plane Surface(20) = {19};
Line Loop(21) = {7, 12, 3, -6};
Plane Surface(22) = {21};
Line Loop(23) = {9, -5, 1, -11};
Plane Surface(24) = {23};
Surface Loop(25) = {14, 22, 20, 18, 16, 24};
Mesh.Algorithm = 6;
'''
    return geostr






def oldcylinder(length=10*mm, radius=1.0*mm, lcar=1.0, **kwds):
    geostr = '''
radius = {radius};
length = {length};
lcar = {lcar};
'''.format(**locals())
    geostr += '''
Point(1) = { radius, 0, 0, lcar};
Point(2) = {0,  radius, 0, lcar};
Point(3) = {-radius, 0, 0, lcar};
Point(4) = {0, -radius, 0, lcar};
Point(5) = {0,0,0};

Circle(1) = {1,5,2};
Circle(2) = {2,5,3};
Circle(3) = {3,5,4};
Circle(4) = {4,5,1};

Extrude{0,0,length}{ Line{-1,-2,-3,-4}; }

Mesh.Algorithm = 6;
'''
    return geostr
