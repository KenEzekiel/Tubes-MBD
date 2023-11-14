from Operation import Operation, Operation_Type
from Resource import Resource

class Transaction:
  id: int
  x_locked: list
  s_locked: list
  operations_done: list
  start_ts: int
  validation_ts: int
  finish_ts: int
  write_set: list
  read_set: list

  def __init__(self, id):
    self.id = id
    self.x_locked = []
    self.s_locked = []
    self.operations_done = []
    self.write_set = []
    self.read_set = []
    self.start_ts = None
    self.validation_ts = None
    self.finish_ts = None

  def x_lock(self, res: Resource):
    if (res.is_x_lock):
      print("Resource already exclusively locked, can't lock resource")
    elif (len(res.is_s_lock) != 0):
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
    self.read_set.append(res.name)

  def write(self, res: Resource):
    print(f"{self.id} Writing resource {res.name}")
    self.write_set.append(res.name)

  def unlock_all(self):
    for i in self.x_locked:
      self.x_unlock(i)
    for j in self.s_locked:
      self.s_unlock(j)

  def commit(self):
    print(f"Commit Transaction {self.id}")
    self.unlock_all()

  def validate(self):
    print(f"Validate Transaction {self.id}")

  def do_operation(self, operation: Operation, res: Resource):
    if operation.op_type == Operation_Type.READ:
      self.read(res)
    if operation.op_type == Operation_Type.WRITE:
      self.write(res)
    if operation.op_type == Operation_Type.COMMIT:
      self.commit()
    if operation.op_type == Operation_Type.SLOCK:
      self.s_lock(res)
    if operation.op_type == Operation_Type.XLOCK:
      self.x_lock(res)
    if operation.op_type == Operation_Type.VALIDATE:
      self.validate()
    self.operations_done.append([operation.op_type.name, operation.resource_name])


  def __str__(self):
    return f"""Transaction {self.id}:
  Operations done: {self.operations_done}
  X locked: {self.x_locked}
  S locked: {self.s_locked}
  Start TS: {self.start_ts}
  Validate TS: {self.validation_ts}
  Finish TS: {self.finish_ts}
  Write set: {self.write_set}
  Read set: {self.read_set}"""