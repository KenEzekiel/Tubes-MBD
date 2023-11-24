

class ResourceVersion:
  version: int
  w_ts: int
  r_ts: int

  def __init__(self, version: int, w_ts: int, r_ts: int):
    self.version = version
    self.w_ts = w_ts
    self.r_ts = r_ts
  
  def __str__(self):
    return f"""
    Resource Version {self.version}
    Write Timestamp: {self.w_ts}
    Read Timestamp: {self.r_ts}
    """