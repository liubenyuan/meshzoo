#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Creates meshes on a 3D L-shape.
'''
import meshio
import meshpy.tet
import numpy as np
import time


def _main():

    # get the file name to be written to
    args = _parse_options()

    # circumcirlce radius
    cc_radius = 10.0
    lx = 2.0/np.sqrt(3.0) * cc_radius
    l = [lx, lx, lx]

    # create the mesh data structure
    print 'Create mesh...',
    start = time.time()
    # Corner points of the cube
    points = [
        (-0.5*l[0], -0.5*l[1], -0.5*l[2]),
        ( 0.5*l[0], -0.5*l[1], -0.5*l[2]),
        ( 0.5*l[0],  0.5*l[1], -0.5*l[2]),
        (-0.5*l[0],  0.5*l[1], -0.5*l[2]),
        (-0.5*l[0], -0.5*l[1],  0.5*l[2]),
        ( 0.5*l[0],  0.5*l[1],  0.5*l[2]),
        (-0.5*l[0],  0.5*l[1],  0.5*l[2]),
        ( 0.0,      -0.5*l[1],  0.5*l[2]),
        ( 0.0,      -0.5*l[1],  0.0),
        ( 0.5*l[0], -0.5*l[1],  0.0),
        ( 0.5*l[0],  0.0,       0.0),
        ( 0.5*l[0],  0.0,       0.5*l[2]),
        ( 0.0,       0.0,       0.5*l[2]),
        ( 0.0,       0.0,       0.0)
        ]
    facets = [[0, 1, 2, 3],
              [4, 7, 12, 11, 5, 6],
              [0, 1, 9, 8, 7, 4],
              [1, 2, 5, 11, 10, 9],
              [2, 5, 6, 3],
              [3, 6, 4, 0],
              [8, 13, 12, 7],
              [8, 9, 10, 13],
              [10, 11, 12, 13]
              ]
    # create the mesh
    # Set the geometry and build the mesh.
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=args.maxvol)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    num_nodes = len(meshpy_mesh.points)
    print '\n%d nodes, %d elements\n' % (num_nodes, len(meshpy_mesh.elements))

    # write the mesh with data
    print 'Write to file...',
    start = time.time()
    meshio.write(
        args.filename,
        np.array(meshpy_mesh.points),
        {'tetra': np.array(meshpy_mesh.elements)}
        )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed

    return


def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser(
        description='Construct a trival tetrahedrization of a 3D L-shape.'
        )

    parser.add_argument(
        'filename',
        metavar='FILE',
        type=str,
        help='file to be written to'
        )

    parser.add_argument(
        '--maxvol', '-m',
        metavar='MAXVOL',
        dest='maxvol',
        nargs='?',
        type=float,
        const=1.0,
        default=1.0,
        help=('maximum tetrahedron volume ' +
              'of the tetrahedrization (default: 1.0)')
        )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    _main()