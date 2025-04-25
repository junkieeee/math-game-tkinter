import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random

class User:
    def __init__(self, name):
        self.name = name
        self.correct_number = 0
        self.wrong_number = 0

def clear_all():
    for widget in root.winfo_children():
        widget.destroy()

def clear_question_elements():
    
    for widget in root.winfo_children():
        if widget not in [score_label]:
            widget.destroy()

def age_control(age):
    if age <= 6:
        messagebox.showinfo("Error", "This game is for ages 6 and above.")
        return False
    return True

def ask_question(user, level):
    clear_question_elements()
    question_label = tk.Label(root, text=f"Level {level} Question", font=("Arial", 18), bg="#d1e231")
    question_label.pack(pady=20)
    question_text_label = tk.Label(root, text="", font=("Arial", 16), bg="#d1e231")
    question_text_label.pack(pady=10)
    answer_entry = tk.Entry(root, font=("Arial", 14))
    answer_entry.pack(pady=10)
    feedback_label = tk.Label(root, text="", font=("Arial", 14, "italic"), fg="gray", bg="#d1e231")
    feedback_label.pack(pady=5)
    submit_btn = tk.Button(root, text="Check Answer", command=lambda: check_answer())
    submit_btn.pack(pady=10)
    root.bind("<Return>", lambda event: check_answer())  

    question_data = {}
    current_question_index = 0
    correct_answers = 0
    wrong_answers = 0

    def generate_question(lvl):
        if lvl == 1:
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)
            answer = number1 + number2
            question = f"{number1} + {number2} = ?"
        elif lvl == 2:
            number1 = random.randint(1, 20)
            number2 = random.randint(1, 20)
            answer = number1 - number2
            question = f"{number1} - {number2} = ?"
        else:
            number1 = random.randint(1, 30)
            number2 = random.randint(1, 30)
            answer = number1 * number2
            question = f"{number1} * {number2} = ?"
        return {"question": question, "answer": answer}

    def load_question():
        nonlocal current_question_index
        if current_question_index < 5:
            question_info = question_data[current_question_index]
            question_text_label.config(text=question_info["question"])
            answer_entry.delete(0, tk.END)
            feedback_label.config(text="")
            submit_btn.config(state=tk.NORMAL)
        else:
            user.correct_number = correct_answers
            user.wrong_number = wrong_answers
            save_score(user)
            show_score()

    def check_answer():
        nonlocal current_question_index, correct_answers, wrong_answers
        submit_btn.config(state=tk.DISABLED)
        try:
            user_answer = int(answer_entry.get())
            correct_answer = question_data[current_question_index]["answer"]
            if user_answer == correct_answer:
                feedback_label.config(text="Thats True!", fg="green")
                correct_answers += 1
            else:
                feedback_label.config(text=f"False!: {correct_answer}", fg="red")
                wrong_answers += 1
        except ValueError:
            feedback_label.config(text="TThis is not acceptable!", fg="orange")

        current_question_index += 1
        root.after(500, load_question) 

   
    for _ in range(5):
        question_data[_] = generate_question(level)

    
    load_question()

def ask_level(user):
    clear_all() 
    label = tk.Label(root, text="Choose Level (1-3):", font=("Arial", 18), bg="#d1e231")
    label.pack(pady=30)

    for lvl in range(1, 4):
        btn = tk.Button(
            root,
            text=f"Level {lvl}",
            font=("Arial", 14),
            width=15,
            command=lambda l=lvl: ask_question(user, l)
        )
        btn.pack(pady=10)

def calculate_score(correct):
    if correct == 0:
        return 0
    elif correct <= 10:
        return correct * 10
    elif correct <= 20:
        return correct * 20
    elif correct <= 30:
        return correct * 30
    else:
        return correct * 40

def start_game():
    clear_all() 
    label = tk.Label(root,text="Enter your name:", font=("Helvetica", 20), bg="#d1e231")
    label.pack(pady=20)
    global name_entry, age_entry
    name_entry = tk.Entry(root, font=("Helvetica",16))
    name_entry.pack(pady=10)
    label_age = tk.Label(root, text="Enter your age:", font=("Helvetica", 20), bg="#d1e231")
    label_age.pack(pady=20)
    age_entry = tk.Entry(root, font=("Helvetica",16))
    age_entry.pack(pady=10)
    continue_btn = tk.Button(root, text="Continue", font=("Helvetica", 16), command=proceed)
    continue_btn.pack(pady=10)
    root.bind("<Return>", proceed) 

def proceed(event):
    name = name_entry.get()
    age = age_entry.get()
    if name.strip() == "" or age.strip() == "":
        messagebox.showerror("Error", "Please enter your name and age.")
        return
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid age.")
        return
    if not age_control(age):
        return
    user = User(name)
    ask_level(user)

def save_score(user):
    with open("score.txt", "a") as file:
        file.write(f"{user.name}|{user.correct_number}|{user.wrong_number}|{calculate_score(user.correct_number)}\n")

def show_score():
    clear_all() 
    scores_data = {}
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                try:
                    name, correct_number, wrong_number, score = line.strip().split("|")
                    correct_number = int(correct_number)
                    wrong_number = int(wrong_number)
                    score = int(score)
                    if name in scores_data:
                        scores_data[name]['correct'] += correct_number
                        scores_data[name]['wrong'] += wrong_number
                        scores_data[name]['total_score'] += score
                        scores_data[name]['count'] += 1
                    else:
                        scores_data[name] = {'correct': correct_number, 'wrong': wrong_number, 'total_score': score, 'count': 1}
                except ValueError:
                    continue

    title_label = tk.Label(root, text="🏆 Score 🏆", font=("Helvetica", 16, "bold"), bg="#d1e231")
    title_label.pack(pady=10)

    header_frame = tk.Frame(root, bg="#d1e231")
    header_frame.pack(pady=5)
    tk.Label(header_frame, text="Player", font=("Helvetica", 12, "bold"), width=15, bg="#d1e231").pack(side="left")
    tk.Label(header_frame, text="Correct Count", font=("Helvetica", 12, "bold"), width=15, bg="#d1e231").pack(side="left")
    tk.Label(header_frame, text="Wrong Count", font=("Helvetica", 12, "bold"), width=15, bg="#d1e231").pack(side="left")
    tk.Label(header_frame, text="Average score", font=("Helvetica", 12, "bold"), width=15, bg="#d1e231").pack(side="left")
    tk.Label(header_frame, text="Game count", font=("Helvetica", 12, "bold"), width=15, bg="#d1e231").pack(side="left")

    for name, data in scores_data.items():
        data_frame = tk.Frame(root, bg="#d1e231")
        data_frame.pack(pady=2, fill="x")
        average_score = data['total_score'] / data['count']
        tk.Label(data_frame, text=name, font=("Helvetica", 12), width=17, bg="#d1e231").pack(side="left")
        tk.Label(data_frame, text=str(data['correct']), font=("Helvetica", 12), width=17, bg="#d1e231").pack(side="left")
        tk.Label(data_frame, text=str(data['wrong']), font=("Helvetica", 12), width=17, bg="#d1e231").pack(side="left")
        tk.Label(data_frame, text=f"{average_score:.2f}", font=("Helvetica", 12), width=17, bg="#d1e231").pack(side="left")
        tk.Label(data_frame, text=f"({data['count']})", font=("Helvetica", 12), width=17, bg="#d1e231").pack(side="left")

    if not scores_data:
        no_scores_label = tk.Label(root, text="No scores have been recorded yet.", font=("Helvetica", 12), bg="#d1e231")
        no_scores_label.pack(pady=10)

    back_to_menu_button = tk.Button(root, text="Back to Main Menu", font=("Helvetica", 12), command=show_main_menu)
    back_to_menu_button.pack(pady=10)

def show_main_menu():
    clear_all()
    global score_label, start_button, show_scores_button, exit_button
    root.columnconfigure(0, weight=1)  
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=0)

    score_label = tk.Label(root, text="Welcome to the Math Game!", font=("Helvetica", 24), bg="#d1e231")
    score_label.grid(row=0, column=0, padx=20, pady=20)

    start_button = tk.Button(root, text="Start Game", font=("Helvetica", 25), command=start_game)
    start_button.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
    start_button.config(bg="#4CAF50", fg="white", activebackground="#45a049", width=20, height=2)
    root.bind("<Return>", start_game)

    button_frame = tk.Frame(root, bg="#d1e231")
    button_frame.grid(row=2, column=0, padx=50, pady=20, sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 12), command=root.quit)
    exit_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    exit_button.config(bg="#f44336", fg="white", activebackground="#d32f2f", width=10, height=2)

    show_scores_button = tk.Button(button_frame, text="Show Past Scores", font=("Helvetica", 12), command=show_score)
    show_scores_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    show_scores_button.config(bg="#008CBA", fg="white", activebackground="#007B9E", width=20, height=2)

def adjust_font_size(event):
    global default_font, header_font, large_font
    current_width = root.winfo_width()
    if current_width < 700:
        new_default_size = 10
        new_header_size = 12
        new_large_size = 20
    elif current_width < 900:
        new_default_size = 12
        new_header_size = 14
        new_large_size = 24
    else:
        new_default_size = 14
        new_header_size = 16
        new_large_size = 28

        default_font.config(size=new_default_size)
        header_font.config(size=new_header_size)
        large_font.config(size=new_large_size)
    for widget in root.winfo_children():
        try:
            if "font" in widget.config(): 
                current_font = widget.cget("font")
                if current_font == default_font.actual():
                    widget.config(font=default_font)
                elif current_font == header_font.actual():
                    widget.config(font=header_font)
                elif current_font == large_font.actual():
                    widget.config(font=large_font)
        except tk.TclError:
            pass 

def main():
    global root, score_label, start_button, show_scores_button, exit_button, default_font, header_font, large_font
    root = tk.Tk()
    root.title("MATH GAME")
    root.geometry("800x600")
    root.configure(bg="#d1e231")
    root.bind("<Configure>", adjust_font_size)

    default_font = font.Font(family="Helvetica", size=12)
    header_font = font.Font(family="Helvetica", size=16, weight="bold")
    large_font = font.Font(family="Helvetica", size=20, weight="bold")

    root.columnconfigure(0, weight=1) 
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)

    score_label = tk.Label(root, text="Welcome to the Math Game!", font=("Helvetica", 24), bg="#d1e231")
    score_label.grid(row=0, column=0, padx=20, pady=20)

    start_button = tk.Button(root, text="Start Game", font=large_font, command=start_game)
    start_button.grid(row=1, column=0, padx=50, pady=20, sticky="ew")
    start_button.config(bg="#4CAF50", fg="white", activebackground="#45a049", height=3)  

    button_frame = tk.Frame(root, bg="#d1e231")
    button_frame.grid(row=2, column=0, padx=50, pady=20, sticky="ew")
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    exit_button = tk.Button(button_frame, text="Exit", font=default_font, command=root.quit)
    exit_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    exit_button.config(bg="#f44336", fg="white", activebackground="#d32f2f", height=2)

    show_scores_button = tk.Button(button_frame, text="Show Past Scores", font=default_font, command=show_score)
    show_scores_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    show_scores_button.config(bg="#008CBA", fg="white", activebackground="#007B9E", height=2)

    root.mainloop()
if __name__ == "__main__":
    main()
    