import Models.init as init

class Transactions:
    def __init__(self, yearN):
        self.db, self.cr = init.connectDatabase(yearN)

    def getAll(self, studentId):
        self.cr.execute(f"SELECT * FROM tuitions WHERE student={studentId};")
        transactions = self.cr.fetchall()

        self.cr.execute(f"SELECT fees.fee, students.id, students.scholarship FROM fees INNER JOIN students ON fees.grade = students.grade WHERE students.id={studentId};")
        fee = self.cr.fetchone()
        if str(fee) == 'None': fee = 0
        else:
            scholarship = int(fee[2])
            fee = int(fee[0])
            if scholarship > 0: fee = fee - (fee * scholarship / 100)
        
        filteredTransactions = []
        paid = 0
        for t in transactions:
            newT = [t[1], "{:,}".format(int(t[3])), t[0]]
            filteredTransactions.append(newT)
            paid += int(t[3])

        remaining = fee - paid

        self.db.commit()
        self.db.close()
        return (filteredTransactions, paid, remaining, fee)

    def edit(self, id, transactionOBJ):
        self.cr.execute(
            f"UPDATE tuitions SET date='{transactionOBJ[0]}', amount={int(transactionOBJ[1])} WHERE id={id};")
        self.db.commit()
        self.db.close()

    def add(self, id, transactionOBJ):
        self.cr.execute(
            f"INSERT INTO tuitions (date, amount, student) VALUES ('{transactionOBJ[0]}', {int(transactionOBJ[1])}, {id});")
        self.db.commit()
        self.db.close()

    def delete(self, id):
        self.cr.execute(f"DELETE FROM tuitions WHERE id={id};")
        self.db.commit()
        self.db.close()