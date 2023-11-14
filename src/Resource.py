
class Resource:
  name: str
  value: int
  is_x_lock: bool
  is_s_lock: list

  def __init__(self, name):
    self.name = name
    self.value = 0
    self.is_x_lock = False
    self.is_s_lock = []

  def __str__(self):
    return f"""Resource {self.name}
  Value: {self.value}
  Is x locked: {self.is_x_lock}
  Is s locked: {self.is_s_lock}"""
  