import typing
from ResourceVersion import ResourceVersion

class Resource:
  name: str
  value: int
  is_x_lock: bool
  is_s_lock: list
  versions: typing.List[ResourceVersion]

  def __init__(self, name: str):
    self.name = name
    self.value = 0
    self.is_x_lock = False
    self.is_s_lock = []
    self.versions = []
    self.versions.append(ResourceVersion(0,0,0))
    self.lock_holder = None

  def __str__(self):
    string = f"""Resource {self.name}
  Value: {self.value}
  Is x locked: {self.is_x_lock}
  Is s locked: {self.is_s_lock}
  Versions:"""
    for i in self.versions:
      string += str(i)
    return string
  
  def add_version(self, w_ts: int, r_ts: int):
    max_version = 0
    for version in self.versions:
      if version.version > max_version:
        max_version = version.version
    self.versions.append(ResourceVersion(max_version + 1, w_ts, r_ts))
    
  