import sqlite3
import os
import csv

currencies = ['$', '₱', 'LS', '£', '₩', '¥', '﷼', '€']
themeFilePath = './Data/theme.txt'
currencyFilePath = './Data/currency.txt'
themes = {"Default":"DefaultNoMoreNagging", "Blue":"LightGrey6", "Teal":"DarkTeal6", "Dark":"DarkAmber1", "Brown":"LightBrown11", "Red":"LightGrey5"}
themesList = list(themes.keys())

def rangeScore(percent):
    markRange = {'A+': 97, 'A': 93, 'A-': 90,
                 'B+': 87, 'B': 83, 'B-': 80,
                 'C+': 77, 'C': 73, 'C-': 70,
                 'D+': 67, 'D': 65, 'D-': 0}
    for u, v in markRange.items():
        if float(percent) >= v:
            return u

def initiateDatabase(yearN):
    if os.path.exists('./Data/') == False:
        os.mkdir('./Data/')
    db = sqlite3.connect('./Data/' + yearN[0] + '.db')
    cr = db.cursor()
    cr.execute(
        '''
        CREATE TABLE if not exists "students" (
        "id"	INTEGER NOT NULL,
        "first"	TEXT,
        "last"	TEXT,
        "father"	TEXT,
        "mother"	TEXT,
        "birth"	TEXT,
        "phone"	TEXT,
        "grade"	INTEGER,
        "class"	INTEGER,
        "scholarship"	INTEGER,
        PRIMARY KEY("id"));
        ''')
    cr.execute(
        '''
        CREATE TABLE if not exists "fees" (
        "id"	INTEGER NOT NULL,
        "fee"	INTEGER NOT NULL,
        "grade"	INTEGER NOT NULL,
        PRIMARY KEY("id"));
        ''')
    cr.execute(
        '''
        CREATE TABLE if not exists "marks" (
        "id"	INTEGER NOT NULL,
        "student"	INTEGER NOT NULL,
        "subject"	TEXT NOT NULL,
        "mark"	TEXT NOT NULL,
        "full"	TEXT NOT NULL,
        "month"	INTEGER NOT NULL,
        "year"	INTEGER NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("student") REFERENCES "students"("id"));
        ''')
    cr.execute(
        '''
        CREATE TABLE if not exists "tuitions" (
        "id"	INTEGER NOT NULL,
        "date"	TEXT NOT NULL,
        "student"	INTEGER NOT NULL,
        "amount"	INTEGER NOT NULL,
        PRIMARY KEY("id"),
        FOREIGN KEY("student") REFERENCES "students"("id"));
        ''')
    db.commit()
    db.close()

def getConstants(fileName):
    constants = []
    if os.path.exists(f'./Data/{fileName}.csv') == False:
        file = open(f'./Data/{fileName}.csv', 'w')
        if fileName == "grades" or fileName == "classes":
            file.write("All\n")
        file.close()
    with open(f'./Data/{fileName}.csv', 'r') as file:
        for line in file:
            constants.append(line.strip())
    if len(constants) == 0: constants.append("None")
    return constants

def addConstant(fileName, newConstant):
    constants = getConstants(fileName)
    if newConstant not in constants:
        with open(f'./Data/{fileName}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([newConstant])

def setTheme(theme):
    file = open(themeFilePath, 'w')
    file.write(themes[theme])
    file.close()

def setCurrency(curreny):
    file = open(currencyFilePath, 'w')
    file.write(curreny)
    file.close()

def getTheme():
    if os.path.exists(themeFilePath) == False:
        file = open(themeFilePath, 'w')
        file.write(themes['Default'])
        file.close()
    else:
        file = open(themeFilePath, 'r')
        theme = file.read()
        file.close()
        for key, value in themes.items():
            if theme == value:
                return key, theme

def getCurrency():
    if os.path.exists(currencyFilePath) == False:
        file = open(currencyFilePath, 'w')
        file.write('$')
        file.close()
    else:
        file = open(currencyFilePath, 'r')
        currency = file.read()
        file.close()
        return currency

def connectDatabase(yearN):
    db = sqlite3.connect('./Data/' + yearN + '.db')
    cr = db.cursor()
    return db, cr