import tkinter as tk
import random
import time
from tkinter import font

# ---- 題庫 ----
normal_words = [
    "apple", "music", "dance", "happy", "photo", "mouse", "green","mango","orange","banana","grape"
]

hard_phrases = [
    "take care", "look out", "give up", "go ahead", "wake up","break down","check in","figure out","run into","set up"
]

nightmare_sentences = [
    "The weather is getting colder today.",
    "She is reading a book in the library.",
    "Please turn off the lights before leaving.",
]

super_hard = [
    "Pneumonoultramicroscopicsilicovolcanoconiosis",
    "Honorificabilitudinitatibus",
    "Supercalifragilisticexpialidocious",
    "Hippopotomonstrosesquipedaliophobia",
    "Antidisestablishmentarianism"
]
class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Game")
        self.root.geometry("520x460")

        self.rounds_total = 0
        self.current_round = 0
        self.score = 0
        self.time_limit = 10
        self.remaining_time = 10
        self.current_answer = ""
        self.difficulty = "NORMAL"

        self.time_start = 0
        self.time_end = 0
        self.total_time_used = 0
        self.total_chars = 0


        tk.Label(root, text="選擇難度：", font=("Arial", 14)).pack()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.normal_btn = tk.Button(self.button_frame, text="NORMAL",
                                    width=10, command=lambda: self.set_difficulty("NORMAL"))
        self.normal_btn.grid(row=0, column=0, padx=5)

        self.hard_btn = tk.Button(self.button_frame, text="HARD",
                                  width=10, command=lambda: self.set_difficulty("HARD"))
        self.hard_btn.grid(row=0, column=1, padx=5)

        self.night_btn = tk.Button(self.button_frame, text="NIGHTMARE",
                                   width=10, command=lambda: self.set_difficulty("NIGHTMARE"))
        self.night_btn.grid(row=0, column=2, padx=5)
        
        self.super_btn = tk.Button(self.button_frame, text="夭壽難",
                                   width=10, command=lambda: self.set_difficulty("super_hard"))
        self.super_btn.grid(row=0, column=3, padx=5)

        self.update_difficulty_button()

        tk.Label(root, text="輸入回合數：").pack()
        self.round_entry = tk.Entry(root)
        self.round_entry.pack()

        tk.Button(root, text="開始遊戲", command=self.start_game).pack(pady=10)

        self.question_label = tk.Label(root, text="", font=("Arial", 18))
        self.question_label.pack(pady=10)

        self.timer_label = tk.Label(root, text="", font=("Arial", 14), fg="purple")
        self.timer_label.pack()

        # 輸入區
        self.input_entry = tk.Entry(root, font=("Arial", 14))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.check_answer)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 14))
        self.feedback_label.pack()


    def set_difficulty(self, level):
        self.difficulty = level
        self.update_difficulty_button()

    def update_difficulty_button(self):
        for btn in [self.normal_btn, self.hard_btn, self.night_btn, self.super_btn]:
            btn.config(bg="SystemButtonFace")

        if self.difficulty == "NORMAL":
            self.normal_btn.config(bg="lightgreen")
        elif self.difficulty == "HARD":
            self.hard_btn.config(bg="orange")
        elif self.difficulty == "NIGHTMARE":
            self.night_btn.config(bg="tomato")
        elif self.difficulty == "super_hard":
            self.super_btn.config(bg="purple")



    def start_game(self):
        try:
            self.rounds_total = int(self.round_entry.get())
        except:
            self.feedback_label.config(text="請輸入有效的回合數！", fg="red")
            return

        # reset
        self.current_round = 0
        self.score = 0
        self.total_time_used = 0
        self.total_chars = 0
        self.feedback_label.config(text="")
        self.input_entry.config(state="normal")

        self.next_round()


    def next_round(self):
        if self.current_round >= self.rounds_total:
            self.show_result()
            return

        self.current_round += 1

        if self.difficulty == "NORMAL":
            self.current_answer = random.choice(normal_words)
            self.time_limit = 10
        elif self.difficulty == "HARD":
            self.current_answer = random.choice(hard_phrases)
            self.time_limit = 10
        elif self.difficulty == "NIGHTMARE":
            self.current_answer = random.choice(nightmare_sentences)
            self.time_limit = 15
        elif self.difficulty == "super_hard":
            self.current_answer = random.choice(super_hard)
            self.time_limit = 20

        self.question_label.config(text=self.current_answer)
        self.input_entry.delete(0, tk.END)

        self.time_start = time.time()

        self.remaining_time = self.time_limit
        self.countdown()


    def countdown(self):
        if self.remaining_time < 0:
            return

        if self.remaining_time == 0:
            self.feedback_label.config(text="時間到！錯誤", fg="red")
            # 計算使用秒數（整回合 = time_limit）
            used_time = self.time_limit
            self.total_time_used += used_time
            self.timer_label.config(text=f"本回合耗時：{used_time} 秒", fg="purple")
            self.root.after(800, self.next_round)
            return

        self.timer_label.config(text=f"倒數：{self.remaining_time} 秒", fg="red")
        self.remaining_time -= 1
        self.root.after(1000, self.countdown)

    

    def check_answer(self, event):
        user_input = self.input_entry.get().strip()

        self.remaining_time = -1

        # 記錄結束時間
        self.time_end = time.time()
        used_time = round(self.time_end - self.time_start, 2)

        # 顯示本回合耗時
        self.timer_label.config(text=f"本回合耗時：{used_time} 秒", fg="purple")

        # 累計時間
        self.total_time_used += used_time

        # 判斷輸入
        if user_input == self.current_answer:
            self.score += 1
            self.feedback_label.config(text=" 正確！", fg="green")

            # 計入字元（不含空白）
            self.total_chars += len(self.current_answer.replace(" ", ""))

        else:
            self.feedback_label.config(text=" 錯誤！", fg="red")

       
        self.root.after(1000, self.next_round)


    def show_result(self):
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(state="disabled")

        self.question_label.config(text="")
        self.timer_label.config(text="")

        # 計算 WPM
        if self.total_time_used > 0:
            wpm = round((self.total_chars / 5) / (self.total_time_used / 60), 2)
        else:
            wpm = 0

       
        self.feedback_label.config(
            text=f"GAME OVER\n得分：{self.score}/{self.rounds_total}\nWPM：{wpm}",
            fg="black",
            font=("Arial", 16)
        )



root = tk.Tk()
game = TypingGame(root)
root.mainloop()
