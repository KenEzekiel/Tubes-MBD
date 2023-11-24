
from enum import Enum


class Operation_Type(Enum):
  READ = 1
  WRITE = 2
  COMMIT = 3
  XLOCK = 4
  SLOCK = 5
  UNLOCK = 6
  VALIDATE = 7

class Operation:
  op_type: Operation_Type
  transaction_id: int
  resource_name: str

  def __init__(self, string: str):
    if string[0] == 'R':
      self.op_type = Operation_Type.READ
      self.transaction_id = int(string[1])
      self.resource_name = string[3]
    elif string[0] == 'W':
      self.op_type = Operation_Type.WRITE
      self.transaction_id = int(string[1])
      self.resource_name = string[3]
    elif string[0] == 'C':
      self.op_type = Operation_Type.COMMIT
      self.transaction_id = int(string[1])
      self.resource_name = ""
    elif string[0] == 'X':
      self.op_type = Operation_Type.XLOCK
      self.transaction_id = int(string[2])
      self.resource_name = string[4]
    elif string[0] == 'S':
      self.op_type = Operation_Type.SLOCK
      self.transaction_id = int(string[2])
      self.resource_name = string[4]
    elif string[0] == 'U':
      self.op_type = Operation_Type.UNLOCK
      self.transaction_id = "" # type: ignore
      self.resource_name = string[3]
    elif string[0] == 'V':
      self.op_type = Operation_Type.VALIDATE
      self.transaction_id = int(string[1])
      self.resource_name = ""

  def __str__(self):
    return f'{self.op_type.name} {self.transaction_id} {self.resource_name}'
  
  @staticmethod
  def from_array(trans_id: int, array: list):
    string = ""
    if array[0] == Operation_Type.READ.name:
      string = f"R{trans_id}({array[1]})"
    elif array[0] == Operation_Type.WRITE.name:
      string = f"W{trans_id}({array[1]})"
    elif array[0] == Operation_Type.COMMIT.name:
      string = f"C{trans_id}"
    elif array[0] == Operation_Type.XLOCK.name:
      string = f"XL{trans_id}({array[1]})"
    elif array[0] == Operation_Type.SLOCK.name:
      string = f"SL{trans_id}({array[1]})"
    elif array[0] == Operation_Type.UNLOCK.name:
      string = f"UL({array[1]})"
    elif array[0] == Operation_Type.VALIDATE.name:
      string = f"V{trans_id}"
    return string