
from Algorithm import Algorithm
from Operation import Operation_Type
from Resource import Resource
from Schedule import Schedule
from Transaction import Transaction


class ValidationProtocol(Algorithm):


  def __init__(self, schedule: Schedule):
    super().__init__(schedule)
    
  
  def execute(self):
    super().execute()
    # Get all startTS, validationTS, and finishTS for every transaction, based on the schedule
    for transaction in self.transactions:
      for i in range(len(self.schedule.operations)):
        if (self.schedule.operations[i].transaction_id == transaction.id):
          transaction.start_ts = i
          break
      for i in range(len(self.schedule.operations)):
        if (self.schedule.operations[i].op_type == Operation_Type.VALIDATE and self.schedule.operations[i].transaction_id == transaction.id):
          transaction.validation_ts = i
          break
      for i in range(len(self.schedule.operations)-1, -1, -1):
        if (self.schedule.operations[i].transaction_id == transaction.id):
          transaction.finish_ts = i
          break

    # Then, run all the operations in the schedule
    # Also get all the write set and read set
    for operation in self.schedule.operations:
      if (operation.transaction_id != ""):
        transaction = self.transactions[operation.transaction_id-1]
        
        transaction.do_operation(operation, self.resources[(ord(operation.resource_name)-65)] if  operation.resource_name != "" else "")

        if operation.op_type == Operation_Type.VALIDATE:
          check = True
          for i in range(operation.transaction_id-1):
            check = self.check(self.transactions[i], self.transactions[operation.transaction_id-1])
            if not check:
              print(f"Validation error for transaction {operation.transaction_id} when validating against transaction {i+1}")
          if check:
            print(f"Validation for transaction {operation.transaction_id} successful")


  def check(self, Ti: Transaction, Tj: Transaction):
    # Check 1 finish_ts Ti < start_ts Tj
    if (Ti.finish_ts < Tj.start_ts):
      return True
    else:
      if (Tj.start_ts < Ti.finish_ts and Ti.finish_ts < Tj.validation_ts):
        condition = True
        for i in Ti.write_set:
          if i in Tj.read_set:
            print(f"Validation failed because transaction i's write set intersects with transaction j's read set")
            condition = False
        return condition
      else:
        return False

schedule = Schedule("input1")
print(str(schedule))
validation_protocol = ValidationProtocol(schedule)
validation_protocol.execute()
print(str(validation_protocol))