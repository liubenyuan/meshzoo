#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import argparse
from meshpy.tet import MeshInfo, build
from meshpy.geometry import generate_surface_of_revolution, EXT_OPEN, \
    GeometryBuilder
import numpy as np
import time


def create_ball_mesh(num_longi_points):

    radius = 5.0

    radial_subdiv = 2 * num_longi_points

    dphi = np.pi / num_longi_points

    # Make sure the nodes meet at the poles of the ball.
    def truncate(r):
        if abs(r) < 1e-10:
            return 0
        else:
            return r

    # Compute the volume of a canonical tetrahedron
    # with edgelength radius*dphi.
    a = radius * dphi
    canonical_tet_volume = np.sqrt(2.0) / 12 * a**3

    # Build outline for surface of revolution.
    rz = [(truncate(radius * np.sin(i*dphi)), radius * np.cos(i*dphi))
          for i in xrange(num_longi_points+1)
          ]

    geob = GeometryBuilder()
    geob.add_geometry(
            *generate_surface_of_revolution(
                rz,
                closure=EXT_OPEN,
                radial_subdiv=radial_subdiv
                ))
    mesh_info = MeshInfo()
    geob.set(mesh_info)
    meshpy_mesh = build(mesh_info, max_volume=canonical_tet_volume)

    return np.array(meshpy_mesh.points), np.array(meshpy_mesh.elements)


def _parse_options():
    '''Parse input options.'''
    import argparse
    parser = argparse.ArgumentParser(
        description='Construct tetrahedrization of a ball.'
        )

    parser.add_argument('filename',
                        metavar='FILE',
                        type=str,
                        help='file to be written to'
                        )

    parser.add_argument('--numpoints', '-p',
                        metavar='N',
                        dest='num_longi_points',
                        nargs='?',
                        type=int,
                        const=10,
                        default=10,
                        help=('number of discretization points ' +
                              'along a logitudinal line')
                        )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    import meshio
    args = _parse_options()

    print('Build mesh...')
    start = time.time()
    points, cells = create_ball_mesh(args.num_longi_points)
    elapsed = time.time()-start
    print('done. (%gs)' % elapsed)

    print('\n%d nodes, %d elements' % (len(points), len(cells)))

    print('Write mesh...')
    start = time.time()
    meshio.write(
            args.filename,
            points,
            {'tetra': cells}
            )
    elapsed = time.time()-start
    print 'done. (%gs)' % elapsed