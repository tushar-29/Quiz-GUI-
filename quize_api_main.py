import requests
import random
import tkinter
import html
from tkinter import messagebox


response = requests.get('https://opentdb.com/api.php?amount=10&type=boolean')
response.raise_for_status()
all_data = response.json()['results']
ques_ans = []
answer = ""
question = []
for i in all_data:
    ques = [html.unescape(i['question']), i['correct_answer']]
    ques_ans.append(ques)


window = tkinter.Tk()
window.minsize(width=400, height=500)
window.title(string='QUIZE APP')

point = 00
score = tkinter.Label(text=f'SCORE : {point}', font=("Arial", 16, 'bold'))
score.grid(row=1, column=1)

wrong_pic = tkinter.PhotoImage(file='wrong.png')
right_pic = tkinter.PhotoImage(file='right.png')

body = tkinter.Canvas(height=400, width=400, bg='black')
boad_ques = body.create_text(200, 180, width=360, fill='white', font=("Arial Rounded MT", 25, 'bold'))
body.grid(row=0, column=0, columnspan=3)


def generate():
    global answer, question
    answer = ""
    question = []
    print(len(ques_ans))
    if len(ques_ans) == 0:
        final_result(2)
    else:
        question = random.choice(ques_ans)
        answer = str(question[1])
        body.config(bg='black')
        body.itemconfigure(boad_ques, text=question[0])
        right_btn.configure(state=tkinter.NORMAL)
        wrong_btn.configure(state=tkinter.NORMAL)


def check_answer(color, count=1):
    body.config(bg=color)
    score.config(text=f"SCORE : {point}")
    if count > 0:
        window.after(1000, check_answer, color, count-1)
    else:
        generate()


def wrong_opt():
    right_btn.configure(state=tkinter.DISABLED)
    wrong_btn.configure(state=tkinter.DISABLED)
    global point
    if answer == 'False':
        point += 1

        check_answer('lime')
    else:
        check_answer('red')
    ques_ans.remove(question)


def right_opt():
    global point
    right_btn.configure(state=tkinter.DISABLED)
    wrong_btn.configure(state=tkinter.DISABLED)
    if answer == "True":
        point += 1
        check_answer('lime')
    else:
        check_answer('red')
    ques_ans.remove(question)


def final_result(count):
    body.config(bg='white')
    body.itemconfigure(boad_ques, text=f"GAME OVER \n YOUR SCORE {point} /20", fill='black')
    if count > 0:
        window.after(1000, final_result, count-1)
    else:
        x = messagebox.showinfo(message='GAME OVER')
        if x == "ok":
            exit(1)
        else:
            exit(1)


wrong_btn = tkinter.Button(image=wrong_pic, height=110, width=110, bd=0)
wrong_btn.config(command=wrong_opt)
wrong_btn.grid(row=1, column=0)

right_btn = tkinter.Button(image=right_pic, height=110, width=110, bd=0)
right_btn.config(command=right_opt)
right_btn.grid(row=1, column=2)

generate()
window.mainloop()
