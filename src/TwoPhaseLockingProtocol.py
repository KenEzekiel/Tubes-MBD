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
        self.retry_queue = deque()
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

        self.process_retry_queue()

    def process_operation(self, operation):
        tx_index = self.transaction_map[operation.transaction_id]
        transaction = self.transactions[tx_index]
        resource = self.resources[(ord(operation.resource_name) - 65)] if operation.resource_name != "" else None

        if operation.op_type in [Operation_Type.READ, Operation_Type.WRITE]:
            lock_success = transaction.x_lock(resource) if resource else False

            if not lock_success and resource:
                conflicting_tx_id = resource.lock_holder
                if conflicting_tx_id is not None:
                    self.handle_lock_conflict(transaction.id, conflicting_tx_id, resource.name)
            else:
                ret = transaction.do_operation(operation, self.resources[
                    self.to_int(operation.resource_name)] if operation.resource_name != "" else "")
                super().write(ret)

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

        # Remove operations from retry_queue that belong to the committed transaction
        self.retry_queue = deque(op for op in self.retry_queue if op.transaction_id != tx_id)

        self.process_retry_queue()

    def process_retry_queue(self):
        while self.retry_queue:
            operation = self.retry_queue.popleft()
            self.process_operation(operation)

    def abort_transaction(self, tx_id):
        tx_index = self.transaction_map[tx_id]
        transaction = self.transactions[tx_index]
        transaction.abort()

        for op in self.schedule.operations:
            if op.transaction_id == tx_id:
                self.retry_queue.append(op)

        # print("RETRY QUEUE: ")
        # for operation in self.retry_queue:
        #     print(operation)
        # print("END")


inputFile = input("Input file: ")
outputfile = input("Output file: ")
schedule = Schedule(inputFile)
twoPL = TwoPhaseLockingProtocol(schedule, outputfile)
twoPL.execute()
twoPL.write(str(twoPL))
