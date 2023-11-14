from abc import abstractmethod
from Output import Output
from Resource import Resource
from Schedule import Schedule
from Transaction import Transaction


class Algorithm:
  schedule: Schedule
  transactions: list
  resources: list
  output_writer: Output

  def __init__(self, schedule: Schedule, outputfilename: str):
    self.name = "Algorithm"
    self.schedule = schedule
    self.transactions = []
    self.resources = []
    self.output_writer = Output(outputfilename)
    list_transactions_id = []
    list_resources_name = []

    for i in self.schedule.operations:
      if i.transaction_id in list_transactions_id or i.transaction_id == "":
        pass
      else:
        self.transactions.append(Transaction(i.transaction_id))
        list_transactions_id.append(i.transaction_id)
      if i.resource_name in list_resources_name or i.resource_name == "":
        pass
      else:
        self.resources.append(Resource(i.resource_name))
        list_resources_name.append(i.resource_name)

  def rollback(self, trans: Transaction):
    for i in trans.operations_done:
      self.schedule.append(i)
    trans.operations_done = []
    
  @abstractmethod  
  def execute(self):
    # Write the output to an output file (from user input)
    string = "------------  SCHEDULE  ------------\n" + str(self.schedule) + "\n"
    print(string)
    self.write(string)
    string = "------------  EXECUTION LOG  ------------"
    print(string)
    self.write(string)

  def __str__(self):
    string = f"\n------------  ALGORITHM STATE  ------------\n--------------------\n{self.name}\n--------------------\nTransactions:\n"
    for i in self.transactions:
      string += str(i) + "\n"
    string += "Resources:\n"
    for i in self.resources:
      string += str(i) + "\n"
    return string
  
  def write(self, string: str):
    self.output_writer.write(string)