class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

    def mark_done(self):
        self.completed = True

    def __str__(self):
        status = "✅ Tamamlandı" if self.completed else "🕓 Devam ediyor"
        return f"{self.title} - {status}\nAçıklama: {self.description}\n"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        print(f"✅ '{title}' görevi eklendi.\n")

    def show_tasks(self):
        if not self.tasks:
            print("Henüz görev eklenmemiş.\n")
        else:
            print("\n📋 GÖREV LİSTESİ:")
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")

    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_done()
            print(f"🎉 '{self.tasks[index].title}' tamamlandı!\n")
        else:
            print("Geçersiz görev numarası!\n")


# --- Test ve Demo ---
print("🌸 Başak’s Planner - Akıllı Görev Takip Uygulaması 🌸\n")

planner = TaskManager()
planner.add_task("Proje Sunumu Hazırlığı", "Sunum slaytlarını tamamla ve prova yap.")
planner.add_task("Python Dersi", "Nesneye dayalı programlama bitirme projesi hazırla.")
planner.show_tasks()
planner.mark_task_done(0)
planner.show_tasks()
