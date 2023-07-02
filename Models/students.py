import Models.init as init


class Students:
    def __init__(self, yearN):
        self.db, self.cr = init.connectDatabase(yearN)

    def getAll(self, gradeN, classN, search_input):
        if gradeN == 'All': gradeN = 'grade'
        if classN == 'All': classN = 'class'
        self.cr.execute(
            f"SELECT * FROM students WHERE (first LIKE '%{search_input}%' OR last LIKE '%{search_input}%') AND grade={gradeN} AND class={classN};")
        students = self.cr.fetchall()
        filteredStudents = []
        for s in students:
            newStudent = [s[1], s[2], s[3], s[4], s[5], s[6], f"%{s[9]}", s[0]]
            filteredStudents.append(newStudent)
        self.db.commit()
        self.db.close()
        return filteredStudents

    def add(self, studentOBJ):
        self.cr.execute(
            f'INSERT INTO students (first, last, father, mother, birth, phone, scholarship, grade, class) VALUES ("{studentOBJ[0]}","{studentOBJ[1]}","{studentOBJ[2]}","{studentOBJ[3]}","{studentOBJ[4]}","{studentOBJ[5]}",{int(studentOBJ[6])},{int(studentOBJ[7])},{int(studentOBJ[8])});')
        self.db.commit()
        self.db.close()

    def edit(self, studentOBJ, id):
        self.cr.execute(
            f"UPDATE students SET first='{studentOBJ[0]}', last='{studentOBJ[1]}', father='{studentOBJ[2]}', mother='{studentOBJ[3]}', birth='{studentOBJ[4]}', phone='{studentOBJ[5]}', scholarship={int(studentOBJ[6])}, grade={int(studentOBJ[7])}, class={int(studentOBJ[8])} WHERE id={id};")
        self.db.commit()
        self.db.close()

    def delete(self, id):
        self.cr.execute(f"DELETE FROM students WHERE id={id};")
        self.db.commit()
        self.db.close()

    def getOne(self, id):
        self.cr.execute(f"SELECT * FROM students WHERE id={id}")
        student = self.cr.fetchone()
        return student
