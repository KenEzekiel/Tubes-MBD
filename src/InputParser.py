
import typing
from Operation import Operation

class InputParser:
  list_ops: typing.List[Operation]

  def __init__(self, filename: str):
    self.file = open(f"./inputs/{filename}.txt", "r").read()
    self.file = self.file.split("\n")
    self.list_ops = []
    for i in self.file:
      if i != "":
        op = Operation(i)
        self.list_ops.append(op)
  
  def get_ops(self):
    return self.list_ops
      