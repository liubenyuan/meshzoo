#!/usr/bin/env python
'''
Create irregular mesh on a regular tetrahedron centered at the origin.
'''
import argparse
import meshio
import meshpy.tet
import numpy as np
import time


def _main():
    args = _parse_options()

    # circumcircle radius
    r = 5.0
    # max_volume = 1.0 / args.n**3
    max_volume = 8.0

    # boundary points
    points = []
    points.append((0.0, 0.0, r))
    # theta = arccos(-1/3) (tetrahedral angle)
    costheta = -1.0 / 3.0
    sintheta = 2.0 / 3.0 * np.sqrt(2.0)
    # phi = 0.0
    sinphi = 0.0
    cosphi = 1.0
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = np.pi * 2.0 / 3.0
    sinphi = np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))
    # phi = - np.pi * 2.0 / 3.0
    sinphi = -np.sqrt(3.0) / 2.0
    cosphi = -0.5
    points.append((r * cosphi * sintheta, r * sinphi * sintheta, r * costheta))

    # boundary faces
    facets = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1],
            [1, 2, 3]
            ]

    # create the mesh
    print 'Create mesh...',
    start = time.time()
    # Set the geometry and build the mesh.
    info = meshpy.tet.MeshInfo()
    info.set_points(points)
    info.set_facets(facets)
    meshpy_mesh = meshpy.tet.build(info, max_volume=1.0/args.n**3)
    elapsed = time.time() - start
    print 'done. (%gs)' % elapsed

    print(
        '\n%d nodes, %d elements' % (
            len(meshpy_mesh.points), len(meshpy_mesh.elements))
        )

    meshio.write(
            args.filename,
            meshpy_mesh.points,
            {'tetra': np.array(meshpy_mesh.elements)}
            )

    return


def _parse_options():
    '''Parse input options.'''
    parser = argparse.ArgumentParser(
        description='Construct tetrahedrization of a cube.'
        )

    parser.add_argument(
            'filename',
            metavar='FILE',
            type=str,
            help='file to be written to'
            )

    parser.add_argument(
            '--maxvol', '-m',
            metavar='N',
            dest='n',
            nargs='?',
            type=int,
            const=1,
            default=1,
            help='max volume of a tetrahedron is 1.0/N^3'
            )

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    _main()