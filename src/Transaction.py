from Resource import Resource

class Transaction:
  id: int
  x_locked: list
  s_locked: list
  operations_done: list

  def __init__(self, id):
    self.id = id
    self.x_locked = []
    self.s_locked = []
    self.operations_done = []

  def x_lock(self, res: Resource):
    if (res.is_x_lock):
      print("Resource already exclusively locked, can't lock resource")
    elif (res.is_s_lock.size != 0):
      print("Resource is share locked, can't lock resource")
    else:
      print(f"Transaction {self.id} Exclusive lock on resource {res.name} successful")
      self.x_locked.append(res)
      res.is_x_lock = True

  def s_lock(self, res: Resource):
    if (res.is_x_lock):
      print("Resource already exclusively locked, can't lock resource")
    else:
      print(f"Transaction {self.id} Shared lock on resource {res.name} successful")
      self.s_locked.append(res)
      res.is_s_lock.append(self.id)

  def x_unlock(self, res: Resource):
    if (res in self.x_locked):
      self.x_locked.remove(res)
      res.is_x_lock = False
      print(f"Transaction {self.id} Unlock Exclusive lock on resource {res.name} successful")
    else:
      print(f"Resource {res.name} is not exclusively locked by transaction {self.id}")

  def s_unlock(self, res: Resource):
    if (res in self.s_locked):
      self.s_locked.remove(res)
      res.is_s_lock.remove(self.id)
      print(f"Transaction {self.id} Unlock Shared lock on resource {res.name} successful")
    else:
      print(f"Resource {res.name} is not shared locked by transaction {self.id}")

  def read(self, res: Resource):
    print(f"{self.id} Reading resource {res.name}")

  def write(self, res: Resource):
    print(f"{self.id} Writing resource {res.name}")

  def unlock_all(self):
    for i in self.x_locked:
      self.x_unlock(i)
    for j in self.s_locked:
      self.s_unlock(j)

  def commit(self):
    print(f"Commit Transaction {self.id}, Unlocking locked resources")
    self.unlock_all()