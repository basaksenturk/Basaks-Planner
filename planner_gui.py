import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ---------- Veri Tabanı ----------
class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            due_date TEXT,
            completed INTEGER
        )
        """)
        self.conn.commit()

    def add_task(self, title, description, due_date):
        self.cursor.execute("INSERT INTO tasks (title, description, due_date, completed) VALUES (?, ?, ?, ?)",
                            (title, description, due_date, 0))
        self.conn.commit()

    def mark_done(self, task_id):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()

    def search(self, keyword):
        self.cursor.execute("SELECT * FROM tasks WHERE title LIKE ?", (f"%{keyword}%",))
        return self.cursor.fetchall()

# ---------- Arayüz ----------
class PlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Başak’s Planner")
        self.root.geometry("720x620")
        self.root.resizable(False, False)

        self.bg = "#f2ead3"  # açık tema
        self.fg = "#1a1a1a"
        self.dark_mode = False

        self.manager = TaskManager()

        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        self.root.configure(bg=self.bg)

        tk.Label(self.root, text="Başak’s Planner", font=("Poppins", 18, "bold"), bg=self.bg, fg=self.fg).pack(pady=10)

        # Tema Butonu
        tk.Button(self.root, text="🌓 Tema Değiştir", command=self.toggle_theme).pack(pady=5)

        # Arama alanı
        frame_search = tk.Frame(self.root, bg=self.bg)
        frame_search.pack(pady=5)
        self.search_entry = tk.Entry(frame_search, width=30)
        self.search_entry.grid(row=0, column=0, padx=5)
        tk.Button(frame_search, text="🔍 Ara", command=self.search_task).grid(row=0, column=1)

        # Görev Ekleme Alanı
        frame_add = tk.Frame(self.root, bg=self.bg)
        frame_add.pack(pady=5)
        tk.Label(frame_add, text="Görev Başlığı:", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(frame_add, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=(8, 5), sticky="w")
        tk.Label(frame_add, text="Açıklama:", bg=self.bg, fg=self.fg).grid(row=1, column=0, sticky="nw", pady=(5, 0))
        self.desc_entry = tk.Text(frame_add, width=50, height=4)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="w")
        tk.Label(frame_add, text="Tarih (GG/AA/YYYY):", bg=self.bg, fg=self.fg).grid(row=2, column=0, sticky="w")
        self.date_entry = tk.Entry(frame_add, width=20)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.date_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Butonlar
        frame_btn = tk.Frame(self.root, bg=self.bg)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="+ Görev Ekle", command=self.add_task, bg="#b37a4c", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="✔ Tamamla", command=self.mark_done, bg="#805e36", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="🗑 Temizle", command=self.clear_fields, bg="#a07540", fg="white").grid(row=0, column=2, padx=5)

        # Görev Listesi
        self.task_list = tk.Listbox(self.root, width=85, height=12)
        self.task_list.pack(pady=10)
        self.task_list.bind("<Double-1>", self.show_task_details)

        # Alt bilgi
        self.footer = tk.Label(
            self.root,
            text="© 2025 Başak’s Planner | Tkinter + SQLite | by Başak 🌸",
            font=("Arial", 9, "italic"),
            fg=self.fg,
            bg=self.bg
        )
        self.footer.place(relx=0.5, rely=0.97, anchor="center")

    # ---------- Fonksiyonlar ----------
    def add_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get("1.0", tk.END).strip()
        date = self.date_entry.get()
        if title:
            self.manager.add_task(title, desc, date)
            self.update_task_list()
            self.clear_form()
        else:
            messagebox.showwarning("Uyarı", "Lütfen görev başlığı girin!")

    def mark_done(self):
        try:
            index = self.task_list.curselection()[0]
            task = self.tasks[index]
            self.manager.mark_done(task[0])
            self.update_task_list()
            self.show_success("Görev Tamamlandı 🎉")
        except:
            messagebox.showwarning("Uyarı", "Bir görev seçin!")

    def show_success(self, text):
        label = tk.Label(self.root, text=text, bg="lightgreen", fg="black", font=("Arial", 11, "bold"))
        label.place(relx=0.5, rely=0.9, anchor="center")
        self.root.after(1500, label.destroy)

    def clear_fields(self):
        # Tüm görevleri ve formu temizle
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        self.manager.cursor.execute("DELETE FROM tasks")
        self.manager.conn.commit()
        self.update_task_list()

        msg = tk.Label(self.root, text="Tüm görevler silindi 🗑️", bg="#f8d7da", fg="#721c24", font=("Arial", 10, "bold"))
        msg.place(relx=0.5, rely=0.9, anchor="center")
        self.root.after(1500, msg.destroy)

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        self.tasks = self.manager.get_all()
        for task in self.tasks:
            status = "✔" if task[4] else "⏳"
            self.task_list.insert(tk.END, f"{status} {task[1]} - {task[3]}")

    def search_task(self):
        keyword = self.search_entry.get()
        results = self.manager.search(keyword)
        self.task_list.delete(0, tk.END)
        for task in results:
            status = "✔" if task[4] else "⏳"
            self.task_list.insert(tk.END, f"{status} {task[1]} - {task[3]}")

    def show_task_details(self, event):
        try:
            index = self.task_list.curselection()[0]
            task = self.tasks[index]
            detail_win = tk.Toplevel(self.root)
            detail_win.title("Görev Detayı")
            detail_win.geometry("400x300")
            detail_win.configure(bg=self.bg)
            tk.Label(detail_win, text=task[1], font=("Poppins", 14, "bold"), bg=self.bg, fg=self.fg).pack(pady=5)
            tk.Message(detail_win, text=f"Açıklama:\n{task[2]}", width=350, bg=self.bg, fg=self.fg).pack(pady=5)
            tk.Label(detail_win, text=f"Tarih: {task[3]}", bg=self.bg, fg=self.fg).pack(pady=5)
        except IndexError:
            pass

    def toggle_theme(self):
        if self.dark_mode:
            self.bg, self.fg = "#f2ead3", "#1a1a1a"
        else:
            self.bg, self.fg = "#1a1a1a", "#f2ead3"
        self.dark_mode = not self.dark_mode
        self.root.configure(bg=self.bg)
        self.footer.config(bg=self.bg, fg=self.fg)

# ---------- Başlat ----------
root = tk.Tk()
app = PlannerApp(root)
root.mainloop()
