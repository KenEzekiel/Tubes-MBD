
from Algorithm import Algorithm
from Operation import Operation_Type
from Schedule import Schedule
from Transaction import Transaction


class ValidationProtocol(Algorithm):

  def __init__(self, schedule: Schedule, outputfilename: str):
    super().__init__(schedule, outputfilename)
    self.name = "Validation Protocol"
    
  
  def execute(self):
    super().execute()
    self.update_ts()

    # Then, run all the operations in the schedule
    # Also get all the write set and read set
    while len(self.schedule.operations) > 0:
      operation = self.schedule.operations.pop(0)
      if (operation.transaction_id != ""):
        transaction: Transaction = self.get_transaction(operation.transaction_id) # type: ignore
        
        ret = transaction.do_operation(operation, self.get_resource(operation.resource_name) if  operation.resource_name != "" else "") # type: ignore
        super().write(ret)

        if operation.op_type == Operation_Type.VALIDATE:
          check = True
          for i in range(operation.transaction_id-1):
            check = self.check(self.transactions[i], transaction) # type: ignore
            if not check:
              string = f"Validation error for transaction {operation.transaction_id} when validating against transaction {i+1}\nAborting transaction {operation.transaction_id}"
              super().write(string)
              # Get all remaining operations for the transaction
              operation_left = []
              for i in self.schedule.operations:
                if i.transaction_id == transaction.id and i != operation:
                  operation_left.append(i)
                  self.schedule.operations.remove(i)
              self.rollback(transaction, execute_first=False) # type: ignore
              # Append the remaining operations
              for i in operation_left:
                self.schedule.operations.append(i)
              self.update_ts()
          if check:
            string = f"Validation for transaction {operation.transaction_id} successful"
            super().write(string)

  def update_ts(self):
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

  def check(self, Ti: Transaction, Tj: Transaction):
    # Check 1 finish_ts Ti < start_ts Tj
    if (Ti.finish_ts < Tj.start_ts):
      return True
    else:
      if (Tj.start_ts < Ti.finish_ts and Ti.finish_ts < Tj.validation_ts):
        condition = True
        for i in Ti.write_set:
          if i in Tj.read_set:
            string = f"Validation failed because transaction i's write set intersects with transaction j's read set"
            super().write(string)
            condition = False
        return condition
      else:
        return False

inputfile = input("Input file: ")
outputfile = input("Output file: ")
schedule = Schedule(inputfile)
validation_protocol = ValidationProtocol(schedule, outputfile)
validation_protocol.execute()
print(str(validation_protocol))
validation_protocol.write(str(validation_protocol))