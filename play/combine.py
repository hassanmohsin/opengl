import numpy
from stl import mesh


# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz


def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies


class Combine:
    def __init__(self, files):
        self.files = files

    def combine(self):
        bodies = [mesh.Mesh.from_file(file) for file in self.files]
        axes = ['x', 'y', 'z']
        for i in range(1, len(bodies)):
            minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(bodies[i-1])
            w1 = maxx - minx
            l1 = maxy - miny
            h1 = maxz - minz
            translate(bodies[i], w1, w1 / 10., 1, axes[i%3])

        return mesh.Mesh(numpy.concatenate([body.data for body in bodies]))

    def combine_two(self):
        # Using an existing stl file:
        main_body = mesh.Mesh.from_file(self.files[0])

        # rotate along Y
        # main_body.rotate([0.0, 0.5, 0.0], math.radians(90))

        minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
        w1 = maxx - minx
        l1 = maxy - miny
        h1 = maxz - minz
        copies = copy_obj(main_body, (w1, l1, h1), 2, 2, 1)

        # I wanted to add another related STL to the final STL
        twist_lock = mesh.Mesh.from_file(self.files[1])
        minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(twist_lock)
        w2 = maxx - minx
        l2 = maxy - miny
        h2 = maxz - minz
        translate(twist_lock, w1, w1 / 100., 3, 'x')
        copies2 = copy_obj(twist_lock, (w2, l2, h2), 2, 2, 1)
        # combined = mesh.Mesh(numpy.concatenate([main_body.data, twist_lock.data] +
        #                                        [copy.data for copy in copies] +
        #                                        [copy.data for copy in copies2]))
        combined = mesh.Mesh(numpy.concatenate([main_body.data, twist_lock.data]))

        return combined
