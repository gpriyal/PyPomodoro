import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_TIME = 25*60
SHORT_BREAK_TIME = 5*60
LONG_BREAK_TIME = 15*60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("250x300")
        self.root.title("Pomodoro Timer")
        self.style = Style(theme="minty")
        self.style.theme_use()

        self.name_label = ttk.Label(self.root, text="Enter your name:")
        self.name_label.pack(pady=5)

        self.name_entry = ttk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.timer_label = tk.Label(self.root, text="00:00", font=("Helvetica", 40))
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.progress_label = ttk.Label(self.root, text="Progress: ")
        self.progress_label.pack(pady=10)

        self.work_time, self.break_time = WORK_TIME, SHORT_BREAK_TIME
        self.is_work_time = True       # Are we in a work session?
        self.pomodoros_completed = 0   # How many sessions completed?
        self.is_running = False        # Is the timer currently running?

        self.root.mainloop()

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()

    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False

    def update_progress(self):
        self.progress_label.config(text=f"Progress: {'✔' * self.pomodoros_completed}")

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -= 1
                if self.work_time == 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.update_progress()
                    self.break_time = LONG_BREAK_TIME if self.pomodoros_completed % 4 == 0 else SHORT_BREAK_TIME
                    name = self.name_entry.get() or "User"
                    message = (
                        f"Take a long break and rest your mind, {name}!"
                        if self.pomodoros_completed % 4 == 0
                        else f"Take a short break and stretch your legs, {name}!"
                    )
                    messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 == 0 else "Good job!", message)
            else:
                self.break_time -= 1
                if self.break_time == 0:
                    self.is_work_time, self.work_time = True, WORK_TIME
                    name = self.name_entry.get() or "User"
                    messagebox.showinfo("Work Time", f"Get back to work, {name}!")
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)

PomodoroTimer()