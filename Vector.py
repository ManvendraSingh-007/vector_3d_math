import math
from typing import Union, Tuple


class Vector:
    """
    A mathematical 3D vector class supporting core linear algebra operations.

    Features:
    - Vector arithmetic (addition, subtraction, scalar multiplication)
    - Vector products (dot, cross, triple scalar & vector)
    - Geometric operations (projection, rejection, reflection, rotation)
    - Relationship checks (parallel, perpendicular, unit vectors)
    - Utility functions (magnitude caching, linear interpolation, serialization)
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """Initialize a 3D vector."""
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
        self._magnitude = None  
        
    @property
    def x(self):
    	return self._x
    
    @x.setter
    def x(self, new_x):
    	self._x = float(new_x)
    	self._magnitude = None
    	
    @property
    def y(self):
    	return self._y
    	
    @y.setter
    def y(self, new_y):
    	self._y = float(new_y)
    	self._magnitude = None
    
    @property
    def z(self):
    	return self._z
    
    @z.setter
    def z(self, new_z):
    	self._z = new_z
    	self._magnitude = None

    def magnitude(self) -> float:
        """Compute and cache the magnitude (length) of the vector."""
        if self._magnitude is None:
            self._magnitude = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        return self._magnitude

    def normalize(self) -> 'Vector':
        """Return a unit vector in the same direction."""
        mag = self.magnitude()
        if math.isclose(mag, 0.0):
            raise ValueError("Cannot normalize a zero vector")
        return self * (1 / mag)

    def dot_product(self, v: 'Vector') -> float:
        """Compute the dot product with another vector."""
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross_product(self, v: 'Vector') -> 'Vector':
        """Compute the cross product with another vector."""
        return Vector(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x
        )

    def triple_scalar_product(self, v: 'Vector', w: 'Vector') -> float:
        """Compute the scalar triple product (self · (v × w))."""
        return self.dot_product(v.cross_product(w))

    def triple_vector_product(self, v: 'Vector', w: 'Vector') -> 'Vector':
        """Compute the vector triple product (self × (v × w))."""
        return v * self.dot_product(w) - w * self.dot_product(v)

    def projection(self, v: 'Vector') -> 'Vector':
        """Project this vector onto another vector."""
        mag_v_sq = v.magnitude() ** 2
        if math.isclose(mag_v_sq, 0.0):
            raise ValueError("Cannot project onto a zero vector")
        return v * (self.dot_product(v) / mag_v_sq)

    def rejection(self, v: 'Vector') -> 'Vector':
        """Compute the rejection of this vector from another vector."""
        return self - self.projection(v)

    def reflect(self, normal: 'Vector') -> 'Vector':
        """Reflect this vector across a given normal vector."""
        return self - 2 * self.projection(normal)

    def angle_between(self, v: 'Vector', degrees: bool = True) -> float:
        """Calculate the smallest angle between two vectors."""
        mag_product = self.magnitude() * v.magnitude()
        if math.isclose(mag_product, 0.0):
            raise ValueError("Cannot compute angle with zero vector")
        cos_theta = max(-1.0, min(1.0, self.dot_product(v) / mag_product))
        theta = math.acos(cos_theta)
        return math.degrees(theta) if degrees else theta

    def rotate_around(self, axis: 'Vector', angle: float, degrees: bool = True) -> 'Vector':
        """Rotate the vector around a given axis by an angle (Rodrigues' formula)."""
        if degrees:
            angle = math.radians(angle)
        k = axis.normalize()
        return (
            self * math.cos(angle) +
            k.cross_product(self) * math.sin(angle) +
            k * k.dot_product(self) * (1 - math.cos(angle))
        )

    def lerp(self, v: 'Vector', t: float) -> 'Vector':
        """Perform linear interpolation between this vector and another."""
        return self * (1 - t) + v * t

    def direction_cosine(self) -> Union[Tuple[float, float, float], str]:
        """Compute the direction cosines of the vector."""
        mag = self.magnitude()
        if math.isclose(mag, 0.0):
            return "Undefined for zero vector"
        return (self.x / mag, self.y / mag, self.z / mag)

    def is_zero(self) -> bool:
        """Check if the vector is a zero vector."""
        return math.isclose(self.magnitude(), 0.0)

    def is_unit(self) -> bool:
        """Check if the vector is a unit vector."""
        return math.isclose(self.magnitude(), 1.0)

    def is_parallel(self, v: 'Vector') -> bool:
        """Check if this vector is parallel to another vector."""
        return self.cross_product(v).is_zero()

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert the vector to a tuple."""
        return (self.x, self.y, self.z)

    def __add__(self, *vectors: 'Vector') -> 'Vector':
        """Vector addition with multiple vectors."""
        return Vector(
            self.x + sum(vec.x for vec in vectors),
            self.y + sum(vec.y for vec in vectors),
            self.z + sum(vec.z for vec in vectors)
        )

    def __sub__(self, *vectors: 'Vector') -> 'Vector':
        """Vector subtraction with multiple vectors."""
        return Vector(
            self.x - sum(vec.x for vec in vectors),
            self.y - sum(vec.y for vec in vectors),
            self.z - sum(vec.z for vec in vectors)
        )

    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        """Scalar multiplication."""
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        """Scalar multiplication (right-hand side)."""
        return self.__mul__(scalar)

    def __eq__(self, v: object) -> bool:
        """Check if two vectors are equal."""
        if not isinstance(v, Vector):
            return False
        return (
            math.isclose(self.x, v.x) and
            math.isclose(self.y, v.y) and
            math.isclose(self.z, v.z)
        )

    def __str__(self) -> str:
        """String representation of the vector."""
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        """Official representation of the vector."""
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"



v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
v3 = Vector(7, 8, 9)