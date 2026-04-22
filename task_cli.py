#!/usr/bin/env python3

import sys 
import json
import os
from datetime import datetime

FILE = "tasks.json"

#------------------------------
# Helper Functions
#----------------------
def load_tasks():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)
    with open(FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def get_new_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def now():
    return 
datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#================================
# Command
#================================
def add_task(desc):
    tasks = load_tasks()
    task = {
         "id" : get_new_id(tasks),
         "description": desc,
         "status": "todo",
         "createdAt": now(),
         "updatedAt": now()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added (ID: {task['id']})")

def update_task(task_id, desc):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = desc
            task["updatedAt"] = now()
            save_tasks(tasks)
            print("Task updated")
            return
    print("Task not found")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print("Task Delete")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = now()
            save_tasks(tasks)
            print(f"Task Marked as {status}")
            return
    print("Task not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if not tasks:
        print("No task found")
        return

    for t in tasks:
        print(f"[{t['id']}] {t['description']} ({t['status']})")

#====================
# CLIbhandlerr
#====================
def menu():
    while True:
        print("\n=== TASK TRACKER ===")
        print("1. Tambah Task")
        print("2. Lihat Semua Task")
        print("3. Update Task")
        print("4. Hapus Task")
        print("5. Tandai In Progress")
        print("6. Tandai Selesai")
        print("7. Lihat Task Selesai")
        print("8. Lihat Task Belum Selesai")
        print("9. Keluar")
        print("10. Todo")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            desc = input("Masukkan deskripsi: ")
            add_task(desc)

        elif pilih == "2":
            list_tasks()

        elif pilih == "3":
            task_id = int(input("ID task: "))
            desc = input("Deskripsi baru: ")
            update_task(task_id, desc)

        elif pilih == "4":
            task_id = int(input("ID task: "))
            delete_task(task_id)

        elif pilih == "5":
            task_id = int(input("ID task: "))
            mark_status(task_id, "in-progress")

        elif pilih == "6":
            task_id = int(input("ID task: "))
            mark_status(task_id, "done")

        elif pilih == "7":
            list_tasks("done")

        elif pilih == "8":
            list_tasks("todo")

        elif pilih == "9":
            print("Keluar...")
            break
        elif pilih == "10":
            task_id = int(input("ID task: "))
            mark_status(task_id, "todo")
        else:
            print("Pilihan tidak valid!")


def main():
    if len(sys.argv) > 1:
        # MODE CLI (tetap bisa pakai command)
        cmd = sys.argv[1]

        if cmd == "add":
            add_task(sys.argv[2])

        elif cmd == "list":
            if len(sys.argv) == 3:
                list_tasks(sys.argv[2])
            else:
                list_tasks()

        elif cmd == "update":
            update_task(int(sys.argv[2]), sys.argv[3])

        elif cmd == "delete":
            delete_task(int(sys.argv[2]))

        elif cmd == "mark-in-progress":
            mark_status(int(sys.argv[2]), "in-progress")

        elif cmd == "mark-done":
            mark_status(int(sys.argv[2]), "done")

        else:
            print("Command tidak dikenal")

    else:
        # MODE MENU
        menu()

if __name__ == "__main__":
    main()


