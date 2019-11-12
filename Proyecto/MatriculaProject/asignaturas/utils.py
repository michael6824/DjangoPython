from enum import IntEnum

class CustomerTypes(IntEnum):
  Profesor = 1
  Alumno = 2
  Secretaria = 3

  @classmethod
  def choices(cls):
    return [(key.value, key.name) for key in cls]
