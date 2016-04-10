from math import sqrt
from math import acos
from math import pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    """description of class"""
    CANNOT_NORMILIZE_ZERO_VECTOR_MSG = 'Can not normilize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(c) for c in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [sc + c for sc, c in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [sc - c for sc, c in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [sc * Decimal(c) for sc in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        return Decimal(sum([sc**2 for sc in self.coordinates])).sqrt()

    def normalize(self):
        try:
            normalizer = Decimal(1.) / self.magnitude()
            return self.times_scalar(normalizer)
        except ZeroDivisionError:
            raise Exception(CANNOT_NORMILIZE_ZERO_VECTOR_MSG)

    def dot_product(self, v):
        return sum([sc * c for sc, c in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v):
        try:
            radians = acos((self.normalize().dot_product(v.normalize())))
        except Exception as e:
            if str(e) == self.CANNOT_NORMILIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with zero vector')
            else:
               raise e
        return radians

    @staticmethod
    def radian_to_degree(radians):
        return radians * (180. / pi)

    def is_zero(self, tolerance = 1e-10):
        return self.magnitude() < tolerance

    def is_parallel_with(self, v):        
        return self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi

    def is_orthogonal_with(self, v, tolerance = 1e-10):
        return abs(self.dot_product(v)) < tolerance
    
    def component_orthogonal_to(self, basis):
        try:
            return self.minus(self.component_parallel_to(basis))
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            return u.times_scalar(self.dot_product(u))
        except Exception as e:
            if str(e) == self.CANNOT_NORMILIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e