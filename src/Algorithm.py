from abc import abstractmethod
import typing
from Operation import Operation
from Output import Output
from Resource import Resource
from Schedule import Schedule
from Transaction import Transaction


class Algorithm:
  schedule: Schedule
  transactions: list[Transaction]
  resources: list[Resource]
  output_writer: Output

  def __init__(self, schedule: Schedule, outputfilename: str):
    self.name = "Algorithm"
    self.schedule = schedule
    self.transactions = []
    self.resources = []
    self.output_writer = Output(outputfilename)
    list_transactions_id = []
    list_resources_name = []

    # Get the list of transactions and resources
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

  def rollback(self, trans: Transaction, update_ts: typing.Optional[int] = None, execute_first: typing.Optional[bool] = False):
    # rollback, with the transaction being rolled back will be either executed first or later
    if not execute_first:
      for i in trans.operations_done:
        op = Operation(Operation.from_array(trans.id, i))
        self.schedule.operations.append(op)
      trans.operations_done = []
    if execute_first:
      trans.operations_done.reverse()
      for i in trans.operations_done:
        op = Operation(Operation.from_array(trans.id, i))
        self.schedule.operations.insert(0, op)
      trans.operations_done = []
    
    # Update timestamp
    if update_ts is not None:
      trans.ts = update_ts
    
  @abstractmethod  
  def execute(self):
    # Write the output to an output file (from user input)
    string = "------------  SCHEDULE  ------------\n" + str(self.schedule) + "\n"
    self.write(string)
    string = "------------  EXECUTION LOG  ------------"
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
    # Output writer
    self.output_writer.write(string)  
    print(string)

  @staticmethod
  def to_int(res_name: str) -> int:
    # Translate to int
    return (ord(res_name)-65)