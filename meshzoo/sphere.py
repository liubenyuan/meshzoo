import numpy

from .helpers import _compose_from_faces


def uv_sphere(num_points_per_circle: int, num_circles: int, radius=1.0):
    # Mesh parameters
    n_phi = num_points_per_circle
    n_theta = num_circles

    # Generate suitable ranges for parametrization
    phi_range = numpy.linspace(0.0, 2 * numpy.pi, num=n_phi, endpoint=False)
    theta_range = numpy.linspace(
        -numpy.pi / 2 + numpy.pi / (n_theta - 1),
        numpy.pi / 2 - numpy.pi / (n_theta - 1),
        num=n_theta - 2,
    )

    # nodes in the circles of latitude (except poles)
    nodes = radius * numpy.array(
        [[0.0, 0.0, -1.0]]  # south pole
        + [
            [
                numpy.cos(theta) * numpy.sin(phi),
                numpy.cos(theta) * numpy.cos(phi),
                numpy.sin(theta),
            ]
            for theta in theta_range
            for phi in phi_range
        ]
        + [[0.0, 0.0, 1.0]]  # north pole
    )

    south_pole_index = 0
    north_pole_index = len(nodes) - 1

    # create the elements (cells)
    num_elems = 2 * (n_theta - 2) * n_phi
    elems = []

    # connections to south pole
    for i in range(n_phi - 1):
        elems.append([south_pole_index, i + 1, i + 2])
    # close geometry
    elems.append([south_pole_index, n_phi, 1])

    # non-pole elements
    for i in range(n_theta - 3):
        for j in range(n_phi - 1):
            elems += [
                [i * n_phi + j + 2, i * n_phi + j + 1, (i + 1) * n_phi + j + 2],
                [i * n_phi + j + 1, (i + 1) * n_phi + j + 1, (i + 1) * n_phi + j + 2],
            ]

    # close the geometry
    for i in range(n_theta - 3):
        elems += [
            [i * n_phi + 1, (i + 1) * n_phi, (i + 1) * n_phi + 1],
            [(i + 1) * n_phi + 1, (i + 1) * n_phi, (i + 2) * n_phi],
        ]

    # connections to the north pole
    for i in range(n_phi - 1):
        elems.append(
            [
                i + 1 + n_phi * (n_theta - 3) + 1,
                i + n_phi * (n_theta - 3) + 1,
                north_pole_index,
            ]
        )
    # close geometry
    elems.append(
        [
            0 + n_phi * (n_theta - 3) + 1,
            n_phi - 1 + n_phi * (n_theta - 3) + 1,
            north_pole_index,
        ]
    )
    elems = numpy.array(elems)
    assert len(elems) == num_elems, "Wrong element count."

    return nodes, elems


def tetra_sphere(n):
    corners = numpy.array(
        [
            [2 * numpy.sqrt(2) / 3, 0.0, -1.0 / 3.0],
            [-numpy.sqrt(2) / 3, numpy.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [-numpy.sqrt(2) / 3, -numpy.sqrt(2.0 / 3.0), -1.0 / 3.0],
            [0.0, 0.0, 1.0],
        ]
    )
    # make sure the normals are pointing outwards
    faces = [(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)]

    vertices, cells = _compose_from_faces(corners, faces, n)

    # push all nodes to the sphere
    norms = numpy.sqrt(numpy.einsum("ij,ij->j", vertices, vertices))
    vertices /= norms

    return vertices, cells


def octa_sphere(n):
    corners = numpy.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )
    faces = [
        (0, 2, 4),
        (1, 4, 2),
        (1, 3, 4),
        (0, 4, 3),
        (0, 5, 2),
        (1, 2, 5),
        (1, 5, 3),
        (0, 3, 5),
    ]
    vertices, cells = _compose_from_faces(corners, faces, n)

    # push all nodes to the sphere
    norms = numpy.sqrt(numpy.einsum("ij,ij->j", vertices, vertices))
    vertices /= norms

    return vertices, cells


def icosa_sphere(n):
    assert n >= 1
    # Start off with an isosahedron and refine.

    # Construction from
    # <http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html>.
    # Create 12 vertices of a icosahedron.
    t = (1.0 + numpy.sqrt(5.0)) / 2.0
    corners = numpy.array(
        [
            [-1, +t, +0],
            [+1, +t, +0],
            [-1, -t, +0],
            [+1, -t, +0],
            #
            [+0, -1, +t],
            [+0, +1, +t],
            [+0, -1, -t],
            [+0, +1, -t],
            #
            [+t, +0, -1],
            [+t, +0, +1],
            [-t, +0, -1],
            [-t, +0, +1],
        ]
    )

    faces = [
        (0, 11, 5),
        (0, 5, 1),
        (0, 1, 7),
        (0, 7, 10),
        (0, 10, 11),
        (1, 5, 9),
        (5, 11, 4),
        (11, 10, 2),
        (10, 7, 6),
        (7, 1, 8),
        (3, 9, 4),
        (3, 4, 2),
        (3, 2, 6),
        (3, 6, 8),
        (3, 8, 9),
        (4, 9, 5),
        (2, 4, 11),
        (6, 2, 10),
        (8, 6, 7),
        (9, 8, 1),
    ]

    vertices, cells = _compose_from_faces(corners, faces, n)
    # push all nodes to the sphere
    norms = numpy.sqrt(numpy.einsum("ij,ij->j", vertices, vertices))
    vertices /= norms

    return vertices, cells
