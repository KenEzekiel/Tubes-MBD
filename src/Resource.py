
class Resource:
  name: str
  value: int
  is_x_lock: bool
  is_s_lock: list

  def __init__(self, name, value):
    self.name = name
    self.value = value
    self.is_x_lock = False
    self.is_s_lock = []


  