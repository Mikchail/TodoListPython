import sqlite3
from tkinter import messagebox
with sqlite3.connect("todo.db") as db:
    cursor = db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS tasks(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    description text NOT NULL,
    important INTEGER DEFAULT 0,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    ) """)


def getTask(id):
    res = cursor.execute("""SELECT * FROM tasks WHERE id=? """, [id])
    return res.fetchall()


def getTasks(search=""):
    res = cursor.execute("""SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?""",
                         ("%" + search + "%", "%" + search + "%"))
    return res.fetchall()


def newTask(title_entry, desc_entry, update):
    title = title_entry.get()
    desc = desc_entry.get()
    if title != "" and desc != "":
        cursor.execute(
            """INSERT INTO tasks(title,description) VALUES(?,?) """, [title, desc])
        db.commit()
        update()
        title_entry.delete(0, "end")
        desc_entry.delete(0, "end")
    else:
        messagebox.showwarning("Предупреждение", "Добавьте значение всем полям!")


def deleteTask(id, update):
    cursor.execute("""DELETE FROM tasks WHERE id=? """, [id])
    db.commit()
    update()
    return


def updateTask(id, title_entry, desc_entry, update, closeWindow):
    title = title_entry.get()
    desc = desc_entry.get()
    if title != "" and desc != "":
        cursor.execute(""" UPDATE tasks SET title=?, description=? WHERE id=? """, [
                       title, desc, id])
        db.commit()
        update()
        title_entry.delete(0, "end")
        desc_entry.delete(0, "end")
        closeWindow()
    else:
        messagebox.showwarning("Предупреждение", "Добавьте значение всем полям!")

isImport = 0
def getImpotantTasks(update):
    global isImport
    isImp = 1 if isImport == 0 else 0
    if(isImport==0):
        isImport = 1
    else:
        isImport= 0    
    res = cursor.execute("""SELECT * FROM tasks WHERE important=?""",[isImp])
    update("", res.fetchall())



def updateImportantTask(id, important, update):
    newisImportant = important == 0 if 1 else 0
    cursor.execute(""" UPDATE tasks SET important=? WHERE id=? """, [newisImportant, id])
    db.commit()
    update()
