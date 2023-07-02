import Models.init as init

class Fees:
    def __init__(self, yearN):
        self.db, self.cr = init.connectDatabase(yearN)

    def getAll(self):
        self.cr.execute("SELECT * FROM fees")
        fees = self.cr.fetchall()
        filteredFees = []
        for f in fees:
            filteredFees.append(["{:,}".format(f[1]), f[2], f[0]])
        self.db.commit()
        self.db.close()
        return filteredFees
    
    def add(self, feeOBJ):
        self.cr.execute(
            f"INSERT INTO fees (fee, grade) VALUES ({int(feeOBJ[0])}, {int(feeOBJ[1])});")
        self.db.commit()
        self.db.close()
    
    def edit(self, id, feeOBJ):
        self.cr.execute(
            f"UPDATE fees SET fee='{int(feeOBJ[0])}', grade={int(feeOBJ[1])} WHERE id={id};")
        self.db.commit()
        self.db.close()

    def delete(self, id):
        self.cr.execute(f"DELETE FROM fees WHERE id={id};")
        self.db.commit()
        self.db.close()