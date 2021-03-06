from larf.units import cm, mm, um, deg
from larf.util import unitify
import larf.shapes
from larf.mesh import Object as MeshObject

def cpa(dx=1*mm, dy=20*cm, dz=20*cm, offsetx=0, lcar=None, domain=None, **kwds):
    """Return a list of larf.mesh.Objects consisting of a single box of
    given half-dimensions."""

    if lcar is None:
        lcar = 0.5*max(dx,dy,dz)

    box = larf.shapes.box(dx,dy,dz,lcar, **kwds)
    #print box
    mo = MeshObject(domain=domain)
    mo.gen(box)
    mo.translate([offsetx, 0, 0])
    return [mo]
        
def plane(dy=20*cm, dz=20*cm, offsetx=0, flip=False, lcar=None, domain=None, **kwds):
    """Return a list of larf.mesh.Objects consisting of a single box of
    given half-dimensions."""

    if lcar is None:
        lcar = 0.5*max(dy,dz)

    box = larf.shapes.rectangle(dz,dy,lcar, **kwds)
    mo = MeshObject(domain=domain)
    mo.gen(box)
    rot = 90*deg
    if flip:
        rot = -90*deg
    mo.rotate(rot, (0.0,1.0,0.0))
    mo.translate([offsetx, 0, 0])
    return [mo]
        
def cage(dx=20*cm, dy=20*cm, dz=20*cm, offset=(0.0,0.0,0.0), lcar=None, domain=None, **kwds):
    '''
    Return a box open along the X-axis.
    '''
    if lcar is None:
        lcar = 0.5*max(dx,dy,dz)

    box = larf.shapes.rextru(dz, dy, dx, lcar, **kwds)
    mo = MeshObject(domain=domain)
    mo.gen(box)
    mo.rotate(90*deg, (0.0,1.0,0.0))
    mo.translate(offset)
    return [mo]
    
def box(dx=20*cm, dy=20*cm, dz=20*cm, offset=(0,0,0), lcar=None, domain=None, inverse=False, **kwds):
    '''
    Return a closed box.
    '''
    if lcar is None:
        lcar = 0.5*max(dx,dy,dz)

    if inverse:
        box = larf.shapes.invbox(dx, dy, dz, lcar, **kwds)
    else:
        box = larf.shapes.box(dx, dy, dz, lcar, **kwds)
    mo = MeshObject(domain=domain)
    mo.gen(box)
    mo.translate(offset)
    return [mo]
    
