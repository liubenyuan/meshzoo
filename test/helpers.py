import numpy


def _near_equal(a, b, tol=1.0e-12):
    return numpy.allclose(a, b, rtol=0.0, atol=tol)


def _get_signed_areas(coords, cells):
    bc = coords[:, cells]
    return numpy.cross((bc[:, :, 1] - bc[:, :, 0]).T, (bc[:, :, 2] - bc[:, :, 0]).T)
