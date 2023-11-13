from abc import abstractmethod
from Resource import Resource
from Schedule import Schedule
from Transaction import Transaction


class Algorithm:
  schedule: Schedule

  def __init__(self, schedule: Schedule):
    self.schedule = schedule

  def rollback(self, trans: Transaction):
    for i in trans.operations_done:
      self.schedule.append(i)
    trans.operations_done = []
    
  @abstractmethod  
  def execute(self):
    # Write the output to an output file (from user input)
    pass