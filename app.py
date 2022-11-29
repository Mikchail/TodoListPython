import tkinter as tk
from tkinter import *
from Database import *
import datetime

main_bg = '#223441'
window = tk.Tk()
window.title('PythonGuides')
window.geometry("530x730")

def searchTasks(search_entry):
    search = search_entry.get()
    updateTaskList(search)
    return

window.config(bg=main_bg)
label = tk.Label(
    text="Todo List",
)
search_frame = Frame(window)
search_frame.pack(pady=20)


search_entry = Entry(
    search_frame,
    font=('arial', 16)
)
search_entry.pack(side=LEFT)
Button(search_frame, text='Поиск', command=lambda : searchTasks(search_entry)).pack(side=LEFT, fill=BOTH, expand=True)
main_frame = Frame(
    window,
)
Button(search_frame, text="Отобразить важные", command=lambda : getImpotantTasks(updateTaskList)).pack(side=LEFT)
Button(search_frame, text="Сбросить", command=lambda : updateTaskList()).pack(side=LEFT)
main_frame.pack(fill=BOTH,expand=1)
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill="y")
my_canvas.config(yscrollcommand=my_scrollbar.set)
my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
second_frame=Frame(my_canvas, padx=10)
my_canvas.create_window((0,0), window=second_frame,anchor="nw")

def openNewWindow(id):
    task = getTask(id)[0]
    title = task[1]
    desc = task[2]
    newWindow = Toplevel(window)
    newWindow.title("New Window")
    newWindow.geometry("200x200")
    new_frame = Frame(newWindow)
    new_frame.pack(pady=20)
    new_title_entry = Entry(
        new_frame,
        font=('arial', 16)
    )
    new_title_label = Label(new_frame, text="Заголовок").pack(anchor="nw", expand=False)
    new_title_label
    new_title_entry.pack(side=TOP)
    new_title_entry.insert(0, title)
    new_desc_entry = Entry(
        new_frame,
        font=('arial', 16)
    )
    new_desc_entry.insert(0, desc)
    new_desc_label = Label(new_frame, text="Описание")
    new_desc_label.pack(anchor="nw", expand=False)
    new_desc_entry.pack(side=BOTTOM)
    def closeWindow():
        newWindow.destroy()
    Button(
        newWindow,
        text='Обновить',
        font=('arial 10'),
        bg='#c5f776',
        padx=5,
        pady=5,
        command=lambda : updateTask(id, new_title_entry, new_desc_entry, updateTaskList, closeWindow)
    ).pack()
    Label(newWindow, text ="Окно для редактировании задачи").pack()

def deleteTaskFromUI(id):
    answer = messagebox.askquestion(title="", message="Удалить задачу ?")
    if answer == "yes":
        deleteTask(id, updateTaskList)
        return
    return    

def createTaskUI(task, index):
    id = task[0]
    title = task[1]
    desc = task[2]
    important = task[3]
    time = task[4]
    label_frame = LabelFrame(second_frame, text='Задача №' + str(index),padx=10, width=100, borderwidth=5, font=("Arial", 12, "bold"),)
    button_frame = Frame(label_frame)
    button_frame.pack(anchor="nw")
    text =  "Важно" if important == 1 else "Не Важно"
    color = '#c56f76' if important == 1 else "#11c41c"
    Label(button_frame, text=str(time), font=("Arial", 10)).pack(side=LEFT,pady=5, anchor="ne",fill=BOTH, expand=True)
    Label(button_frame, text="", font=("Arial", 10)).pack(side=LEFT,padx=100, anchor="nw",fill=BOTH, expand=True)
    Button(button_frame, text='Удалить', command=lambda : deleteTaskFromUI(id)).pack(side=LEFT, padx=5, pady=5, expand=True, anchor="nw")
    Button(button_frame, text=text,bg=color, command=lambda : updateImportantTask(id, important, updateTaskList)).pack(side=RIGHT,padx=5, pady=5, anchor="nw")
    text_frame = Frame(label_frame)
    text_frame.pack(anchor="nw", fill=BOTH, expand=True)
    title=Label(text_frame, text="Название - " + title, font=("Arial", 12, "bold"),width=45, anchor="nw", justify=LEFT)
    description=Label(text_frame, text=desc, font=("Arial", 12),width=45, anchor="nw",justify=LEFT)
    title.pack(side=TOP, fill=BOTH)
    description.pack(side=TOP, fill=BOTH)
    Button(label_frame, text='Редактировать', command=lambda : openNewWindow(id)).pack(padx=5, pady=5, anchor="ne")
    label_frame.pack(side=TOP, fill=BOTH, expand=1)
    
    
def reset_scrollregion():
    my_canvas.update_idletasks()
    my_canvas.configure(scrollregion=my_canvas.bbox("all"))

def updateTaskList(search = "",list = []):
    if(len(list)):
        task_list = list
    else:
        task_list = getTasks(search)     
    index = 0
    for widget in second_frame.winfo_children():
        widget.pack_forget()
        widget.destroy()
    second_frame.pack_forget()
    second_frame.grid_forget()
    for item in task_list:
        index += 1
        createTaskUI(item, index)
    reset_scrollregion()
    
updateTaskList()

Label(window, text="Cоздать задачу",bg=main_bg,foreground="#ffffff", font=('arial', 16)).pack()
title_frame = Frame(window)
title_frame.pack(pady=5)
title_entry = Entry(
    title_frame,
    font=('arial', 16)
)
title_label = Label(title_frame, text="Заголовок")
title_label.pack(side=LEFT,anchor="nw", expand=False)
title_entry.pack(side=LEFT,anchor="nw", expand=False)

desc_frame = Frame(window)
desc_frame.pack(pady=5)
desc_entry = Entry(
    desc_frame,
    textvariable="asd",
    font=('arial', 16)
)
desc_label = Label(desc_frame, text="Описание")
desc_label.pack(side=LEFT, anchor="ne", expand=False)
desc_entry.pack(side=LEFT, anchor="ne", expand=False)

addTask_btn = Button(
    window,
    text='Создать',
    bg='#c5f776',
    command=lambda : newTask(title_entry, desc_entry, updateTaskList)
)

addTask_btn.pack()
lab = Label(window)
lab.pack()
def clock():
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")
    lab.config(text=time)
    #lab['text'] = time
    window.after(1000, clock) # run itself again after 1000 ms
    
# run first time
clock()
window.mainloop()