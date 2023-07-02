import Models.init as init, Models.students as students
from jinja2 import Environment, FileSystemLoader

class Print:
    def __init__(self, yearN):
        self.db, self.cr = init.connectDatabase(yearN)
        self.yearN = yearN

    def printAll(self, gradeNum, classNum, monthNum, yearNum, folderPath):
        
        templateLoader = FileSystemLoader(searchpath="./")
        env = Environment(loader=templateLoader)
        template = env.get_template("template.html")

        allStudents = students.Students(self.yearN).getAll(gradeNum, classNum, '')
        allStudentsIDs = []
        for s in allStudents:
            allStudentsIDs.append(int(s[-1]))
        
        for sid in allStudentsIDs:
            self.cr.execute(f"SELECT subject,mark,full FROM marks WHERE student={sid} AND month={monthNum} AND year={yearNum};")
            marks = self.cr.fetchall()

            self.cr.execute(f"SELECT first,last,father FROM students WHERE id={sid}")
            first, last, father = self.cr.fetchone()
            result = 0
            total = 0

            for m in marks:
                result = result + int(m[1])
                total = total + int(m[2])

            percentInt = result * 100 / total
            percent = str(float("{:.1f}".format(result * 100 / total))) + '%'

            readyFile = template.render(
            {'title':f'{first} {last}',
             'father':f'{father}',
             'ccgg':f'{classNum}-{gradeNum}',
             'mmyy':f'{monthNum}-{yearNum}',
             'rows':marks,
             'result':f'{result} - {percent} - {init.rangeScore(percentInt)}',
             'total':f'{total}'}
            )

            with open(f"{folderPath}/{first}-{last}-{monthNum}-{yearNum}.html", 'w') as index:
                index.write(readyFile)

            # self.cr.execute(f"SELECT * FROM marks WHERE student IN {tuple(allStudentsIDs)} AND month={monthNum} AND year={yearNum}")
            # filePath = folderPath + f'/{first}-{last}-{monthNum}-{yearNum}.csv'
            # if init.os.path.exists(filePath) == False:
            #     createFile = open(filePath, 'x')
            #     createFile.close()
            # else:
            #     with open(filePath, 'a') as file:
            #         writer = init.csv.writer(file)
            #         writer.writerow([e[2], e[3], e[4]])
