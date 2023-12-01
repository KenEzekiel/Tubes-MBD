from Algorithm import Algorithm
from Operation import Operation_Type
from Schedule import Schedule
from datetime import datetime
from collections import defaultdict, deque
from Transaction import Transaction


class TwoPhaseLockingProtocol(Algorithm):
    def __init__(self, schedule: Schedule, outputfilename: str):
        super().__init__(schedule, outputfilename)
        self.name = "Strict Two Phase Locking Protocol"
        self.transaction_timestamps = {t.id: datetime.now() for t in self.transactions}
        self.waiting_queues = defaultdict(deque)
        self.transaction_map = {t.id: i for i, t in enumerate(self.transactions)}

    def execute(self):
        super().execute()
        for operation in self.schedule.operations:
            tx_index = self.transaction_map[operation.transaction_id]
            transaction = self.transactions[tx_index]

            if transaction.status == Transaction.ABORTED:
                continue
            if transaction.status == Transaction.WAITING:
                continue

            self.process_operation(operation)

    def execute_operation(self, transaction, operation):
        ret = transaction.do_operation(operation, self.resources[
            self.to_int(operation.resource_name)] if operation.resource_name != "" else "")
        super().write(ret)

    def find_conflicting_tid(self, resource):
        return resource.lock_holder

    def process_operation(self, operation):
        tx_index = self.transaction_map[operation.transaction_id]
        transaction = self.transactions[tx_index]
        resource = self.resources[(ord(operation.resource_name) - 65)] if operation.resource_name != "" else None

        if operation.op_type in [Operation_Type.READ, Operation_Type.WRITE]:
            lock_success = transaction.x_lock(resource) if resource else False

            if not lock_success and resource:
                conflicting_tx_id = self.find_conflicting_tid(resource)
                if conflicting_tx_id is not None:
                    self.handle_lock_conflict(transaction.id, conflicting_tx_id, resource.name)
                else:
                    self.waiting_queues[resource.name].append(transaction.id)
                    transaction.status = Transaction.WAITING
            else:
                self.execute_operation(transaction, operation)

        elif operation.op_type == Operation_Type.COMMIT:
            self.commit_transaction(transaction.id)

    def handle_lock_conflict(self, tx_id, conflicting_tx_id, res_name):
        if self.transaction_timestamps[tx_id] < self.transaction_timestamps[conflicting_tx_id]:
            self.waiting_queues[res_name].append(tx_id)
            self.transactions[self.transaction_map[tx_id]].status = Transaction.WAITING
            string = f"Transaction {tx_id} will wait for resource {res_name}. (Wait-Die)"
        else:
            self.abort_transaction(tx_id)
            string = f"Transaction {tx_id} is aborted due to conflict with Transaction {conflicting_tx_id}"
        super().write(string)

    def commit_transaction(self, tx_id):
        tx_index = self.transaction_map[tx_id]
        transaction = self.transactions[tx_index]
        ret = transaction.commit()
        super().write(ret)
        self.process_waiting_queue()

    def process_waiting_queue(self):
        # Process the waiting queue for each resource
        for res_name, queue in self.waiting_queues.items():
            while queue:
                waiting_tx_id = queue.popleft()
                waiting_tx_index = self.transaction_map[waiting_tx_id]
                self.transactions[waiting_tx_index].status = Transaction.ACTIVE
                for op in self.schedule.operations:
                    if op.transaction_id == waiting_tx_id:
                        self.process_operation(op)

    def abort_transaction(self, tx_id):
        tx_index = self.transaction_map[tx_id]
        transaction = self.transactions[tx_index]
        transaction.abort()
        self.process_waiting_queue()


inputFile = input("Input file: ")
outputfile = input("Output file: ")
schedule = Schedule(inputFile)
twoPL = TwoPhaseLockingProtocol(schedule, outputfile)
twoPL.execute()
twoPL.write(str(twoPL))
