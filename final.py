import csv, sqlite3


'Create database and tables'
conn = sqlite3.connect('pumpjack.db')
cur = conn.cursor()

'List of all departments (unique)'
department = []


'------------------------------------------------------------------------------------------------------------------------------------------------'

'Only create employee table if it does NOT exist'
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='employee' ''')
if cur.fetchone()[0]==1:
    cur.execute('''DROP TABLE employee''')
    cur.execute('''CREATE TABLE employee ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [first_name] text, [last_name] text, [salary] int, [department_id] int)''')
else:
    cur.execute('''CREATE TABLE employee ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [first_name] text, [last_name] text, [salary] int, [department_id] int)''')

'------------------------------------------------------------------------------------------------------------------------------------------------'

'Only create department table if it does NOT exist'
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='department' ''')
if cur.fetchone()[0]==1:
    cur.execute('''DROP TABLE department''')
    cur.execute('''CREATE TABLE department ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [name] text, [salary_increment] int)''')
else:
    cur.execute('''CREATE TABLE department ([ID] INTEGER PRIMARY KEY AUTOINCREMENT, [name] text, [salary_increment] int)''')


'------------------------------------------------------------------------------------------------------------------------------------------------'


'Reading a file, appending it to the employee & department table'
with open('flat_data.csv') as fin:
    reader = csv.DictReader(fin)
    for row in reader:
        'Getting the 5 values from csv file'
        firs_name = row.get("first_name")
        last_name = row.get("last_name")
        salary = row.get("salary")
        dept_name = row.get("dept_name")
        increment = row.get("salary_increment")

        if dept_name not in department:
            with open('department_List.txt', 'a') as datafile:
                datafile.write(dept_name + "\n")
            department.append(dept_name)
            'Writing row into the department table'
            sql1 = "INSERT INTO department (name, salary_increment) VALUES ( ?, ?)"
            val1 = (dept_name, increment)
            cur.execute(sql1, val1)

        dept_id = department.index(dept_name)
        'Writing row into the employee table'
        sql2 = "INSERT INTO employee (first_name, last_name, salary, department_id) VALUES (?, ?, ?, ?)"
        val2 = (firs_name,last_name,salary,dept_id)
        cur.execute(sql2,val2)


'------------------------------------------------------------------------------------------------------------------------------------------------'

'Printing the changes on tables'
cur.execute('''SELECT * FROM employee''')
print(cur.fetchall())
print("\n")
cur.execute('''SELECT * FROM department''')
print(cur.fetchall())
'------------------------------------------------------------------------------------------------------------------------------------------------'

conn.commit()
conn.close()
