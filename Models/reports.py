import Models.init as init

class Reports:
    def __init__(self, yearN):
        self.db, self.cr = init.connectDatabase(yearN)

    def getAll(self, studentId):
        self.cr.execute(f"SELECT * from marks WHERE student={studentId}")
        marks = self.cr.fetchall()
        filteredMarks = []
        for m in marks:
            newM = [m[2], m[3], m[4], m[5], m[6], m[0]]
            filteredMarks.append(newM)
        self.db.commit()
        self.db.close()
        return filteredMarks

    def add(self, id, markOBJ):
        self.cr.execute(
            f"INSERT INTO marks (subject, mark, full, month, year, student) VALUES ('{markOBJ[0]}', {int(markOBJ[1])}, {int(markOBJ[2])}, {int(markOBJ[3])}, {int(markOBJ[4])},{id});")
        self.db.commit()
        self.db.close()
    
    def edit(self, id, markOBJ):
        self.cr.execute(
            f"UPDATE marks SET subject='{markOBJ[0]}', mark={int(markOBJ[1])}, full={int(markOBJ[2])}, month={int(markOBJ[3])}, year={int(markOBJ[4])} WHERE id={id};")
        self.db.commit()
        self.db.close()

    def delete(self, id):
        self.cr.execute(f"DELETE FROM marks WHERE id={id};")
        self.db.commit()
        self.db.close()
