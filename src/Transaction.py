from Operation import Operation, Operation_Type
from Resource import Resource


class Transaction:
    ABORTED = 0
    ACTIVE = 1
    WAITING = 2
    id: int
    ts: int
    x_locked: list
    s_locked: list
    status: int
    operations_done: list
    start_ts: int
    validation_ts: int
    finish_ts: int
    write_set: list
    read_set: list

    def __init__(self, id: int):
        self.id = id
        self.ts = id
        self.x_locked = []
        self.s_locked = []
        self.operations_done = []
        self.write_set = []
        self.read_set = []
        self.status = 1
        self.start_ts = None  # type: ignore
        self.validation_ts = None  # type: ignore
        self.finish_ts = None  # type: ignore

    # def x_lock(self, res: Resource):
    #     if res.is_x_lock:
    #         string = f"Resource {res.name} already exclusively locked, can't lock resource"
    #     elif len(res.is_s_lock) != 0:
    #         string = f"Resource {res.name} is share locked, can't lock resource"
    #     else:
    #         string = f"Transaction {self.id} Exclusive lock on resource {res.name} successful"
    #         self.x_locked.append(res)
    #         res.is_x_lock = True
    #     return string

    def x_lock(self, res: Resource):
        if res.is_x_lock and res.lock_holder != self.id:
            return False
        else:
            if not res.is_x_lock:
                self.x_locked.append(res)
                res.is_x_lock = True
                res.lock_holder = self.id
            return True

    def s_lock(self, res: Resource):
        if res.is_x_lock:
            string = f"Resource {res.name} already exclusively locked, can't lock resource"
        else:
            string = f"Transaction {self.id} Shared lock on resource {res.name} successful"
            self.s_locked.append(res)
            res.is_s_lock.append(self.id)
        return string

    def abort(self):
        if self.status != Transaction.ABORTED:
            self.status = Transaction.ABORTED
            self.unlock_all()
            return f"Transaction {self.id} is aborted"
        return f"Transaction {self.id} is already aborted"

    def wait(self):
        if self.status != Transaction.ABORTED:
            self.status = Transaction.WAITING
            return f"Transaction {self.id} is waiting"
        return f"Transaction {self.id} cannot wait, it's already aborted"

    def x_unlock(self, res: Resource):
        if res in self.x_locked:
            self.x_locked.remove(res)
            res.is_x_lock = False
            string = f"Transaction {self.id} Unlock Exclusive lock on resource {res.name} successful"
        else:
            string = f"Resource {res.name} is not exclusively locked by transaction {self.id}"
        return string

    def s_unlock(self, res: Resource):
        if res in self.s_locked:
            self.s_locked.remove(res)
            res.is_s_lock.remove(self.id)
            string = f"Transaction {self.id} Unlock Shared lock on resource {res.name} successful"
        else:
            string = f"Resource {res.name} is not shared locked by transaction {self.id}"
        return string

    def read(self, res: Resource):
        string = f"{self.id} Reading resource {res.name}"
        self.read_set.append(res.name)
        return string

    def write(self, res: Resource):
        string = f"{self.id} Writing resource {res.name}"
        self.write_set.append(res.name)
        return string

    def unlock_all(self):
        for i in self.x_locked:
            self.x_unlock(i)
        for j in self.s_locked:
            self.s_unlock(j)

    def commit(self):
        string = f"Commit Transaction {self.id}"
        self.unlock_all()
        return string

    def validate(self):
        string = f"Validate Transaction {self.id}"
        return string

    def do_operation(self, operation: Operation, res: Resource):
        result = ""
        if operation.op_type == Operation_Type.READ:
            result = self.read(res)
        if operation.op_type == Operation_Type.WRITE:
            result = self.write(res)
        if operation.op_type == Operation_Type.COMMIT:
            result = self.commit()
        if operation.op_type == Operation_Type.SLOCK:
            result = self.s_lock(res)
        if operation.op_type == Operation_Type.XLOCK:
            result = self.x_lock(res)
        if operation.op_type == Operation_Type.VALIDATE:
            result = self.validate()
        self.operations_done.append([operation.op_type.name, operation.resource_name])
        return result

    def __str__(self):
        return f"""Transaction {self.id}:
  Operations done: {self.operations_done}
  X locked: {self.x_locked}
  S locked: {self.s_locked}
  Start TS: {self.start_ts}
  Validate TS: {self.validation_ts}
  Finish TS: {self.finish_ts}
  Write set: {self.write_set}
  Read set: {self.read_set}"""
