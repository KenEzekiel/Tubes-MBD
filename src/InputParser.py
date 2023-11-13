
from Operation import Operation

class InputParser:
  list_ops: list
  def __init__(self, filename):
    self.file = open(f"./inputs/{filename}.txt", "r").read()
    self.file = self.file.split("\n")
    self.list_ops = []
    for i in self.file:
      op = Operation(i)
      self.list_ops.append(op)
  
  def get_ops(self):
    return self.list_ops
      