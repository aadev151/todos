import tkinter
import os


class Name:
    def __init__(self, root, text):
        self.name = tkinter.Entry(root, width=50)
        self.name.insert(0, text)
        self.name.bind("<Button-1>", self.enter)
        self.name.pack()

    def enter(self, event):
        self.name.delete(0, tkinter.END)

    def get_name(self):
        return self.name.get()


class Task:
    def __init__(self, name, is_done, root, todo_name):
        self.name = name
        self.todo_name = todo_name
        self.is_done = False
        if is_done:
            self.is_done = True

        self.cvar = tkinter.BooleanVar().set(False)

        self.check = tkinter.Checkbutton(root, text=self.name, variable=self.cvar, onvalue=True, offvalue=False, command=self.change_value)
        if self.is_done:
            self.check.select()

        self.check.pack(anchor=tkinter.W)

    def change_value(self):
        self.is_done = not self.is_done
        file = open("my todos/" + self.todo_name + "/" + self.name + ".txt", "w")
        file.write(str(self.is_done))
        file.close()


def submit(name):
    if os.path.isdir("my todos/" + name):
        new_todo(text="This TODO already exists. Please enter another name")
    else:
        os.mkdir("my todos/" + name)
        new_todo_file = open("my todos/" + name + "/tasks.txt", "w")
        new_todo_file.close()
        names = open("names.txt", "a+")
        names.write(name + "\n")
        names.close()


def new_todo(text="HQ Browser v2.0"):
    root = tkinter.Tk()
    root.title("Enter the name of the TODO")
    name = Name(root, text)

    submit_btn = tkinter.Button(root, text="Submit", command=lambda: [submit(name.get_name()), root.destroy()])
    submit_btn.pack()

    root.mainloop()


def submit_task(todo_name, task_name):
    if os.path.isfile("my todos/" + todo_name + "/" + task_name + ".txt"):
        new_task(todo_name, text="This Task already exists. Please enter another name")
    else:
        new_file = open("my todos/" + todo_name + "/" + task_name + ".txt", "w")
        new_file.close()
        tasks = open("my todos/" + todo_name + "/tasks.txt", "a+")
        tasks.write(task_name + "\n")
        tasks.close()


def new_task(todo_name, text="Create a favicon"):
    root = tkinter.Tk()
    root.title("Create a new Task for \"" + todo_name + "\" TODO")

    new_task_name = Name(root, text)
    submit_btn = tkinter.Button(root, text="Submit", command=lambda: [submit_task(todo_name, new_task_name.get_name()), root.destroy()])
    submit_btn.pack()

    root.mainloop()


def todo(name):
    root = tkinter.Tk()
    root.title(name)

    todo_name = tkinter.Label(root, text=name, font=("Comic Sans MS", 24))
    todo_name.pack(anchor=tkinter.CENTER)

    file = open("my todos/" + name + "/tasks.txt", "r+")
    all_tasks = []

    for line in file:
        line = line[:-1]
        task_file = open('my todos/' + name + '/' + line + ".txt", "r")

        is_done = None
        if task_file.read() == "True":
            is_done = True
        else:
            is_done = False

        task_file.close()
        all_tasks.append({"name": line, "is_done": is_done})

    for task in all_tasks:
        this_task = Task(task["name"], task["is_done"], root, name)

    file.close()

    new_task_btn = tkinter.Button(root, text="New Task", command=lambda todo_name=name: new_task(todo_name))
    new_task_btn.pack()

    root.mainloop()


def open_todo():
    root = tkinter.Tk()
    root.title("Open a TODO")

    names_file = open("names.txt")
    all_names = []

    for line in names_file:
        all_names.append(line[:-1])

    names_file.close()

    for name in all_names:
        text = tkinter.Label(root, text=name)
        open_btn = tkinter.Button(root, text="Open", command=lambda name=name: todo(name))
        line = tkinter.Label(root, text="__________________________________")

        text.pack(anchor=tkinter.CENTER)
        open_btn.pack(anchor=tkinter.CENTER)
        line.pack(anchor=tkinter.CENTER)

    root.mainloop()


def main():
    root = tkinter.Tk()
    root.geometry("400x400")
    root.title("Create TODOs")

    create_new = tkinter.Button(root, text="New TODO", command=new_todo)
    create_new.place(x=200, y=250, anchor=tkinter.CENTER)

    open_one = tkinter.Button(root, text="Open an existing TODO", command=open_todo)
    open_one.place(x=200, y=150, anchor=tkinter.CENTER)

    root.mainloop()


if __name__ == "__main__":
    main()
