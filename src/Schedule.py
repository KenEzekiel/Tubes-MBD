
from InputParser import InputParser


class Schedule:
  operations: list = []

  def __init__(self, filename: str):
    input_parser = InputParser(filename)
    self.operations = input_parser.get_ops()

  def __str__(self):
    string = "----------\nSchedule\n----------"
    for i in self.operations:
      string += "\n" + str(i) 
    return string
  
