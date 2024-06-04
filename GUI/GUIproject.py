from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as font
import time
import mysql.connector
from random import *
import smtplib as smt
import tkinter.messagebox as tmsg

root = Tk(className=' YG BuyCart   --  INDIA KI APNI DUKAAN')
root.geometry("900x700+0+0")
root.minsize(900, 700)
root.maxsize(900, 700)
userhello=''
c = 0
mydb = mysql.connector.connect(host="localhost", user="root", password="123", database="yatharthproject")
mycursor = mydb.cursor()
status = 'none'
guess = 0
totalNumberOfGuesses = 0
buttons = []
btnStartGameList = []
lblNoGuess = []
secretNumber = 0
timeleft = 30
score = 0
signgmail=''
issign=0
logingmail=''
savecou=0
couvar=''
def YGgames():
    gamewin = Tk(className=' YG BuyCart Games')
    gamewin.geometry("900x400+0+0")
    gamewin.minsize(900, 400)
    gamewin.maxsize(900, 400)
    gamewin.config(bg='sky blue')
    myfont = font.Font(family='times new roman', size=9, weight='bold')
    if savecou==0:
        tmsg.showinfo("Warning","Playing Games without Login or Signup\nwill result in lose of coupon you win.")
    def game1():
        global buttons, guess, totalNumberOfGuesses, status, lblNoGuess
        window = Tk(className=' YG BuyCart Guessing Game')
        # window.title("Guessing Game")  # This is for title
        window.geometry("300x300")
        window.config(bg='aquamarine')

        lblInst = Label(window, text="Guess a number from 0 to 19")
        lblLine0 = Label(window, text="***********************")
        lblNoGu = Label(window, text="Number of Guesses: 0")
        lblNoGuess.append(lblNoGu)
        lblMaxGuess = Label(window, text="Max Guess: 3")
        lblLine1 = Label(window, text="***********************")
        lblLogs = Label(window,
                        text="                                  Game Logs                                      ")
        lblLine2 = Label(window, text="***********************")

        for index in range(0, 20):  # Random number has a range between 0-19
            button = Button(window, text=index, command=lambda index=index: process(index),
                            state=DISABLED, bg='brown')  # lambda index=index: process(index)
            buttons.append(button)  # In buttons lambda is also used for command
        print(buttons)

        def startgame(i):  # This button will start and restart the game
            global status, b, secretNumber
            secretNumber = randrange(20)
            print(secretNumber)

            for b in buttons:
                b["state"] = NORMAL

            if status == "none":
                status = "started"
                btnStartGameList[i]["text"] = "Restart Game"
            else:
                status = "restarted"
                restarting()
            print("Game started")

        btnStartGameList = []
        for index in range(0, 1):
            btnStartGame = Button(window, text="Start Game", command=lambda: startgame(index),
                                  bg='green yellow')  # lambda: startgame
            btnStartGameList.append(btnStartGame)  # This button will start the game

        # append elements to grid
        lblInst.grid(row=0, column=1, columnspan=5, padx=30)
        lblLine0.grid(row=1, column=1, columnspan=5)
        lblNoGuess[0].grid(row=2, column=1, columnspan=3)
        lblMaxGuess.grid(row=2, column=4, columnspan=2)
        lblLine1.grid(row=3, column=1, columnspan=5)
        lblLogs.grid(row=4, column=1, columnspan=5)  # row 4 - 8 is reserved for showing logs
        lblLine2.grid(row=5, column=1, columnspan=5)

        for row in range(0, 4):
            for col in range(0, 5):
                i = row * 5 + col  # convert 2d index to 1d. 5= total number of columns
                buttons[i].grid(row=row + 10, column=col + 1)

        btnStartGameList[0].grid(column=1, columnspan=5)  # row=26

        # Main game logic

        # reset all variables
        def restarting():
            global buttons, guess, totalNumberOfGuesses, secretNumber, lblNoGuess
            guess = 0
            totalNumberOfGuesses = 0
            secretNumber = randrange(20)
            print(secretNumber)
            lblNoGuess[0]["text"] = "Number of Guesses: 0"

            Label(window,text="                                  Game Logs                                      ").grid(row=4, column=1,columnspan=5)
            # remove all logs on init

        def process(i):
            global totalNumberOfGuesses, buttons, lblNoGuess, secretNumber
            guess = i
            totalNumberOfGuesses += 1
            lblNoGuess[0]["text"] = "Number of Guesses: " + str(totalNumberOfGuesses)

            # check if guess match secret number
            if guess == secretNumber:
                lbl = Label(window, text="You won a coupon of Rs.100 ! :) CONGRATULATIONS", fg="green")
                lbl.grid(row=4, column=1, columnspan=5)
                if savecou>=1:
                    mycursor.execute(f'select coupon from users where gmail="{couvar}"')
                    fe = mycursor.fetchall()
                    if fe[0][0]==None:
                        mycursor.execute(f'update users set coupon=100 where gmail="{couvar}"')
                        mydb.commit()
                    else:
                        mycursor.execute(f'update users set coupon=coupon+100 where gmail="{couvar}"')
                        mydb.commit()
                for b in buttons:
                    b["state"] = DISABLED

            # game is over when max no of guesses is reached
            if totalNumberOfGuesses == 3:
                if guess != secretNumber:
                    lbl = Label(window, text="You lost Your coupon,Have a Good luck next time! :)", fg="red")
                    lbl.grid(row=4, column=1, columnspan=5)

                for b in buttons:
                    b["state"] = DISABLED

            buttons[i]["state"] = DISABLED  # Button which is clicked for guessing
        def backing():
            window.destroy()
            YGgames()
        Button(window, text="Back", bg="red", command=backing).place(x=0, y=0)
        window.mainloop()

    def games1():
        gamewin.destroy()
        game1()

    def game2():
        import random
        # list of possible colour.
        colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown']

        # function that will start the game.
        def startGame(event):
            global timeleft, score
            if timeleft == 30:
                # start the countdown timer.
                countdown()
            # choose the next colour.
            nextColour()
            if timeleft == 0:
                if score > 10:
                    Label(root, text='Congratulations! You have won a coupon of 100RS', font=('times new roman',10,'bold'), fg='green').place(x=280, y=200)
                    if savecou >= 1:
                        mycursor.execute(f'select coupon from users where gmail="{couvar}"')
                        fe = mycursor.fetchall()
                        if fe[0][0] == None:
                            mycursor.execute(f'update users set coupon=100 where gmail="{couvar}"')
                            mydb.commit()
                        else:
                            mycursor.execute(f'update users set coupon=coupon+100 where gmail="{couvar}"')
                            mydb.commit()
                else:
                    Label(root, text='Better Luck next time', font=('times new roman',10,'bold'), fg='green').place(x=280, y=200)

        # Function to choose and display the next colour.
        def nextColour():
            global score
            global timeleft

            # if a game is currently in play
            if timeleft > 0:
                # if the colour typed is equal to the colour of the text
                if e.get().lower() == colours[1].lower():
                    score += 1

                # clear the text entry box.
                e.delete(0, END)
                random.shuffle(colours)

                # change the colour to type, by changing the text and the colour to a random colour value
                label.config(fg=str(colours[1]), text=str(colours[0]))

                # update the score.
                scoreLabel.config(text="Score: " + str(score))

        # Countdown timer function
        def countdown():
            global timeleft
            # if a game is in play
            if timeleft > 0:
                # decrement the timer.
                timeleft -= 1

                # update the time left label
                timeLabel.config(text="Time left: " + str(timeleft))

                # run the function again after 1 second.
                timeLabel.after(1000, countdown)

            # Driver Code

        # create a GUI window
        root = Tk()
        # set the title
        root.title("YG BuyCart COLOUR GAME")

        # set the size
        root.geometry("700x300")

        # add an instructions label
        instructions = Label(root, text="Type in the colour of the words, and not the word text!",
                             font=('Helvetica', 12))
        instructions.pack()

        # add a score label
        scoreLabel = Label(root,
                           text="Press enter to start and after 30seconds press enter to see result score more than 10 to win",
                           font=('Helvetica', 12))
        scoreLabel.pack()

        # add a time left label
        timeLabel = Label(root, text="Time left: " + str(timeleft), font=('Helvetica', 12))
        timeLabel.pack()

        # add a label for displaying the colours
        label = Label(root, font=('Helvetica', 60))
        label.pack()

        # add a text entry box for
        # typing in colours
        e = Entry(root, text='enter here to start', fg='green')

        # run the 'startGame' function
        # when the enter key is pressed
        root.bind('<Return>', startGame)
        e.focus_set()  # set focus on the entry box
        e.pack()

        def backing():
            root.destroy()
            YGgames()
        Button(root, text="Back", bg="red", command=backing).place(x=0, y=0)
        # start the GUI
        root.mainloop()

    def games2():
        gamewin.destroy()
        game2()
    def shop():
        gamewin.destroy()
        maiwindow()

    Button(gamewin, text='Colour Name', font=myfont, bg='yellow', command=games2).place(x=500, y=100, width=200, height=200)
    Button(gamewin, text='Perfect Guess', font=myfont, bg='yellow', command=games1).place(x=200, y=100, width=200, height=200)
    Button(gamewin, text="Continue Shopping", bg='red', command=shop).place(x=350, y=350)
    gamewin.mainloop()

def sgames():
    root.destroy()
    YGgames()

def mainro():
    global coupfet,pfont,cpro
    b_root = Tk(className=" BuyCart Payment")
    b_root.geometry("550x300")
    b_root.config(bg='black')
    pfont = font.Font(family="comic sans", size=15, weight="bold")
    cpro=0
    def purcha():
        global coupfet,cpro
        if coupfet[0][0] <= itmpri:
            a = itmpri - coupfet[0][0]
            Label(b_root, text=f'Total updated amount to be paid is {a}', fg="green", font=pfont).place(x=150, y=50)
            cpro = 1
        elif coupfet[0][0] > itmpri:
            a = coupfet[0][0] - itmpri
            Label(b_root, text=f'Total updated amount to be paid is 0  ', fg="green", font=pfont).place(x=150, y=50)
            cpro = 2
        but["state"] = DISABLED
    def finallyover():
        global cpro
        payvag = payvar.get()
        if payvag != "Radio":
            if cpro==1:
                mycursor.execute(f'update users set coupon=Null where gmail="{couvar}"')
                mydb.commit()
            if cpro==2:
                mycursor.execute(f'update users set coupon={a} where gmail="{couvar}"')
                mydb.commit()
            tmsg.showinfo("Payment","Payment Successfull \n Thanks for using our Service")
            mycursor.execute(f"insert into orders(gmail,Product_Name,prise) values('{couvar}','{itmnam}',{itmpri})")
            mydb.commit()
            b_root.destroy()
        else:
            Label(b_root, text="Please Choose a Payment Mode", bg="red").place(x=180, y=200)
    but = Button(b_root, text='Apply Coupon', command=purcha, bg="pink")
    but.place(x=230, y=50)
    mycursor.execute(f'select coupon from users where gmail="{couvar}"')
    coupfet = mycursor.fetchall()
    print(coupfet)
    if coupfet[0][0] != None:
        but["state"] = NORMAL
    if coupfet[0][0] == None:
        but["state"] = DISABLED
    payvar = StringVar()
    payvar.set("Radio")
    BTEXT=f"Total Amount to be paid is {itmpri}"
    Label(b_root, text=BTEXT, fg='green', font=pfont).place(x=100, y=10)
    Label(b_root, text='Please Choose a payment mode:-', fg='green', font=pfont).place(x=100, y=80)
    Radiobutton(b_root, text="Online payment", variable=payvar, value="Online").place(x=230, y=120)
    Radiobutton(b_root, text="COD", variable=payvar, value="CO").place(x=230, y=160)
    Button(b_root, text='Confirm Order', command=finallyover, bg='green').place(x=210, y=250)
    b_root.mainloop()

def maiwindow():
    root = Tk(className=" BuyCart Categories")
    root.geometry("1070x600")
    root.maxsize(1070, 600)
    root.minsize(1070, 600)
    root.config(bg="black")
    # Adding widgets to the root window
    myfont = font.Font(family="Helvetica", size=16, weight="bold")
    Label(root, text=f"Hello {userhello}, Choose a category", \
          relief='groove', font=myfont).place(width=1200)

    def electronics():
        a_root = Tk(className=" BuyCart electronics")
        a_root.geometry("1200x520+0+0")
        a_root.config(bg="black")

        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(a_root, text="Here's Your Electronics Items", \
              relief='groove', font=myfont).place(width=1200)
        def purchase():
            global itmpri,itmnam
            itmpri = 12000
            itmnam = "HEADPHONE(SONY)"
            a_root.destroy()
            mainro()
        o1 = Image.open("1.jpg")
        bo1 = o1.resize((300, 200), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchase1():
            global itmpri,itmnam
            itmnam = "HEADPHONE(TROOPS)"
            itmpri = 8500
            a_root.destroy()
            mainro()
        o = Image.open("2.jpg")
        bo = o.resize((250, 200), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchase2():
            global itmpri,itmnam
            itmnam = "FRIDGE(SONY)"
            itmpri = 85000
            a_root.destroy()
            mainro()
        o2 = Image.open("3.jpg")
        bo2 = o2.resize((250, 200), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchase3():
            global itmpri,itmnam
            itmnam = "K20(OPPO)"
            itmpri = 35000
            a_root.destroy()
            mainro()
        o3 = Image.open("4.jpg")
        bo3 = o3.resize((150, 200), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchase4():
            global itmpri,itmnam
            itmnam = "LAPTOP(SONY)"
            itmpri = 75000
            a_root.destroy()
            mainro()

        o4 = Image.open("5.jpg")
        bo4 = o4.resize((300, 200), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchase5():
            global itmpri,itmnam
            itmnam = "COMPUTER(SONY)"
            itmpri = 85000
            a_root.destroy()
            mainro()

        o5 = Image.open("electronic.jpg")
        bo5 = o5.resize((250, 200), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchase6():
            global itmpri,itmnam
            itmnam = "LAPOTOP(PREDATOR)"
            itmpri = 85000
            a_root.destroy()
            mainro()

        o6 = Image.open("electronic1.jpg")
        bo6 = o6.resize((250, 200), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)

        def purchase7():
            global itmpri,itmnam
            itmnam = "CAMERA(NIKON)"
            itmpri = 250000
            a_root.destroy()
            mainro()

        o7 = Image.open("electronic2.jpg")
        bo7 = o7.resize((250, 200), Image.HUFFMAN_ONLY)
        bl7 = ImageTk.PhotoImage(bo7)

        if savecou>=1:
            Button(a_root, text='HEADPHONE(SONY)       Rs - 12,000', image=bl1, compound=TOP, command=purchase).place(x=20, y=30)
            Button(a_root, text='HEADPHONE(TROOPS)       Rs - 8,500', image=bl, compound=TOP, command=purchase1).place(x=350, y=30)
            Button(a_root, text='FRIDGE(SONY)       Rs - 85,000', image=bl2, compound=TOP, command=purchase2).place(x=630, y=30)
            Button(a_root, text='K20(OPPO)       Rs - 35,000', image=bl3, compound=TOP, command=purchase3).place(x=950, y=30)
            Button(a_root, text='LAPTOP(SONY)       Rs - 75,000', image=bl4, compound=TOP, command=purchase4).place(x=20, y=280)
            Button(a_root, text='COMPUTER(SONY)       Rs - 85,000', image=bl5, compound=TOP, command=purchase5).place(x=350, y=280)
            Button(a_root, text='LAPTOP(PREDATOR)     Rs - 85,000', image=bl6, compound=TOP, command=purchase6).place(x=630, y=280)
            Button(a_root, text='CAMERA(NIKON)        Rs - 250,000', image=bl7, compound=TOP, command=purchase7).place(x=900, y=280)
        if savecou==0:
            Button(a_root, text='HEADPHONE(SONY)       Rs - 12,000', image=bl1, compound=TOP).place(x=20, y=30)
            Button(a_root, text='HEADPHONE(TROOPS)       Rs - 8,500', image=bl, compound=TOP).place(x=350, y=30)
            Button(a_root, text='FRIDGE(SONY)       Rs - 85,000', image=bl2, compound=TOP).place(x=630, y=30)
            Button(a_root, text='K20(OPPO)       Rs - 35,000', image=bl3, compound=TOP).place(x=950, y=30)
            Button(a_root, text='LAPTOP(SONY)       Rs - 75,000', image=bl4, compound=TOP).place(x=20, y=280)
            Button(a_root, text='COMPUTER(SONY)       Rs - 85,000', image=bl5, compound=TOP).place(x=350, y=280)
            Button(a_root, text='LAPTOP(PREDATOR)     Rs - 85,000', image=bl6, compound=TOP).place(x=630, y=280)
            Button(a_root, text='CAMERA(NIKON)        Rs - 250,000', image=bl7, compound=TOP).place(x=900, y=280)

        def backing():
            a_root.destroy()
            maiwindow()
        Button(a_root, text="Back", bg="red", command=backing).place(x=0, y=0)
        a_root.mainloop()

    def ele():
        root.destroy()
        electronics()

    def clothes():
        b = Tk(className=" BuyCart Clothes")
        b.geometry("1200x700+0+0")
        b.config(bg="black")
        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(b, text="Fashion Items", \
              relief='groove', font=myfont).place(width=1200)

        def purchasec1():
            global itmpri,itmnam
            itmnam = "JEANS"
            itmpri = 12000
            b.destroy()
            mainro()
        o1 = Image.open("clothes1.jpg")
        bo1 = o1.resize((300, 300), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchasec2():
            global itmpri,itmnam
            itmnam = "CASUAL T-SHIRT"
            itmpri = 8500
            b.destroy()
            mainro()

        o = Image.open("clothes2.jpg")
        bo = o.resize((250, 300), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchasec3():
            global itmpri,itmnam
            itmnam = "T-SHIRT(ROYAL BLACK)"
            itmpri = 85000
            b.destroy()
            mainro()

        o2 = Image.open("clothes3.jpg")
        bo2 = o2.resize((250, 300), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchasec4():
            global itmpri,itmnam
            itmnam = "SHOES(PUMA)"
            itmpri = 35000
            b.destroy()
            mainro()

        o3 = Image.open("clothes4.jpg")
        bo3 = o3.resize((250, 300), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchasec5():
            global itmpri,itmnam
            itmnam = "CASUAL SHOES(ROBBIN JONES)"
            itmpri = 75000
            b.destroy()
            mainro()

        o4 = Image.open("clothes5.jpg")
        bo4 = o4.resize((300, 300), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchasec6():
            global itmpri,itmnam
            itmnam = "CASUAL JEANS"
            itmpri = 85000
            b.destroy()
            mainro()

        o5 = Image.open("clothes6.jpg")
        bo5 = o5.resize((250, 300), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchasec7():
            global itmpri, itmnam
            itmnam = "WATCH(TITAN)"
            itmpri = 85000
            b.destroy()
            mainro()

        o6 = Image.open("clothes7.jpg")
        bo6 = o6.resize((250, 300), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)

        def purchasec8():
            global itmpri, itmnam
            itmnam = "WATCH(TITAN)"
            itmpri = 245000
            b.destroy()
            mainro()

        o7 = Image.open("clothes8.jpg")
        bo7 = o7.resize((250, 300), Image.HUFFMAN_ONLY)
        bl7 = ImageTk.PhotoImage(bo7)

        if savecou>=1:
            Button(b, text='JEANS       Rs - 12,000', image=bl1, compound=TOP, command=purchasec1).place(x=20, y=30)
            Button(b, text='Casual T-Shirt       Rs - 8,500', image=bl, compound=TOP, command=purchasec2).place(x=350, y=30)
            Button(b, text='T-Shirt(Royal Black)       Rs - 85,000', image=bl2, compound=TOP, command=purchasec3).place(x=630, y=30)
            Button(b, text='Shoes(PUMA)       Rs - 35,000', image=bl3, compound=TOP, command=purchasec4).place(x=900, y=30)
            Button(b, text='Casual Shoes(Robbin jones)       Rs - 75,000', image=bl4, compound=TOP, command=purchasec5).place(x=20, y=360)
            Button(b, text='Casual Jeans       Rs - 85,000', image=bl5, compound=TOP, command=purchasec6).place(x=350, y=360)
            Button(b, text='WATCH(TITAN)     Rs - 85,000', image=bl6, compound=TOP, command=purchasec7).place(x=630, y=360)
            Button(b, text='WATCH(TITAN)       Rs - 2,45,000', image=bl7, compound=TOP, command=purchasec8).place(x=900, y=360)
        if savecou==0:
            Button(b, text='JEANS       Rs - 12,000', image=bl1, compound=TOP).place(x=20, y=30)
            Button(b, text='Casual T-Shirt       Rs - 8,500', image=bl, compound=TOP).place(x=350, y=30)
            Button(b, text='T-Shirt(Royal Black)       Rs - 85,000', image=bl2, compound=TOP).place(x=630, y=30)
            Button(b, text='Shoes(PUMA)       Rs - 35,000', image=bl3, compound=TOP).place(x=900, y=30)
            Button(b, text='Casual Shoes(Robbin jones)       Rs - 75,000', image=bl4, compound=TOP).place(x=20, y=360)
            Button(b, text='Casual Jeans       Rs - 85,000', image=bl5, compound=TOP).place(x=350, y=360)
            Button(b, text='WATCH(TITAN)     Rs - 85,000', image=bl6, compound=TOP).place(x=630, y=360)
            Button(b, text='WATCH(TITAN)       Rs - 2,45,000', image=bl7, compound=TOP).place(x=900, y=360)
        def backing():
            b.destroy()
            maiwindow()
        Button(b, text="Back", bg="red", command=backing).place(x=0, y=0)
        b.mainloop()

    def c():
        root.destroy()
        clothes()

    def sports():
        c = Tk(className=" BuyCart Sports")
        c.geometry("1200x600+0+0")
        c.config(bg="black")

        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(c, text="SPORTS", \
              relief='groove', font=myfont).place(width=1200)

        def purchases1():
            global itmpri, itmnam
            itmnam = "FOOTBALL(NIVIA)"
            itmpri = 12000
            c.destroy()
            mainro()
        o1 = Image.open("sport1.jpg")
        bo1 = o1.resize((300, 200), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchases2():
            global itmpri, itmnam
            itmnam = "BAT(GM)"
            itmpri = 8500
            c.destroy()
            mainro()
        o = Image.open("sport2.jpg")
        bo = o.resize((50, 250), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchases3():
            global itmpri, itmnam
            itmnam = "BAT(CEAT)"
            itmpri = 85000
            c.destroy()
            mainro()
        o2 = Image.open("sport3.jpg")
        bo2 = o2.resize((40, 250), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchases4():
            global itmpri, itmnam
            itmnam = "LEATHER BALL(WHITE)"
            itmpri = 35000
            c.destroy()
            mainro()

        o3 = Image.open("sport4.jpg")
        bo3 = o3.resize((300, 200), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchases5():
            global itmpri, itmnam
            itmnam = "FOOTBALL(MIKASA)"
            itmpri = 75000
            c.destroy()
            mainro()

        o4 = Image.open("sport5.jpg")
        bo4 = o4.resize((300, 200), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchases6():
            global itmpri, itmnam
            itmnam = "RACKET"
            itmpri = 85000
            c.destroy()
            mainro()

        o5 = Image.open("sport6.jpg")
        bo5 = o5.resize((100, 250), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchases7():
            global itmpri, itmnam
            itmnam = "LEATHER BALL(WHITE-JUPITER)"
            itmpri = 85000
            c.destroy()
            mainro()

        o6 = Image.open("sport8.jpg")
        bo6 = o6.resize((300, 200), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)
        if savecou>=1:
            Button(c, text='FOOTBALL(NIVIA)       Rs - 12,000', image=bl1, compound=TOP, command=purchases1).place(x=20, y=30)
            Button(c, text='BAT(GM)       Rs - 8,500', image=bl, compound=TOP, command=purchases2).place(x=400, y=30)
            Button(c, text='BAT(CEAT)       Rs - 85,000', image=bl2, compound=TOP, command=purchases3).place(x=630, y=30)
            Button(c, text='LEATHER BALL(WHITE)       Rs - 35,000', image=bl3, compound=TOP, command=purchases4).place(x=850, y=30)
            Button(c, text='FOOTBALL(MIKASA)       Rs - 75,000', image=bl4, compound=TOP, command=purchases5).place(x=20, y=310)
            Button(c, text='RACKET       Rs - 85,000', image=bl5, compound=TOP, command=purchases6).place(x=400, y=310)
            Button(c, text='LEATHER BALL(WHITE-JUPITER)     Rs - 85,000', image=bl6, compound=TOP, command=purchases7).place(x=850, y=310)
        if savecou==0:
            Button(c, text='FOOTBALL(NIVIA)       Rs - 12,000', image=bl1, compound=TOP).place(x=20, y=30)
            Button(c, text='BAT(GM)       Rs - 8,500', image=bl, compound=TOP).place(x=400, y=30)
            Button(c, text='BAT(CEAT)       Rs - 85,000', image=bl2, compound=TOP).place(x=630, y=30)
            Button(c, text='LEATHER BALL(WHITE)       Rs - 35,000', image=bl3, compound=TOP).place(x=850, y=30)
            Button(c, text='FOOTBALL(MIKASA)       Rs - 75,000', image=bl4, compound=TOP).place(x=20, y=310)
            Button(c, text='RACKET       Rs - 85,000', image=bl5, compound=TOP).place(x=400, y=310)
            Button(c, text='LEATHER BALL(WHITE-JUPITER)     Rs - 85,000', image=bl6, compound=TOP).place(x=850, y=310)
        def backing():
            c.destroy()
            maiwindow()
        Button(c, text="Back", bg="red", command=backing).place(x=0, y=0)
        c.mainloop()

    def s():
        root.destroy()
        sports()

    def home():
        d = Tk(className=" BuyCart Home Appliances")
        d.geometry("1300x600+0+0")
        d.config(bg="black")
        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(d, text="HOME APPLIANCES", \
              relief='groove', font=myfont).place(width=1300)

        def purchaseh1():
            global itmpri, itmnam
            itmnam = "WASHING MACHINE(FRONT LOADED)"
            itmpri = 95000
            d.destroy()
            mainro()
        o1 = Image.open("home1.jpg")
        bo1 = o1.resize((200, 250), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchaseh2():
            global itmpri, itmnam
            itmnam = "WASHING MACHINE"
            itmpri = 45500
            d.destroy()
            mainro()
        o = Image.open("home2.jpg")
        bo = o.resize((200, 250), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchaseh3():
            global itmpri, itmnam
            itmnam = "RO"
            itmpri = 59000
            d.destroy()
            mainro()

        o2 = Image.open("home3.jpg")
        bo2 = o2.resize((200, 250), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchaseh4():
            global itmpri, itmnam
            itmnam = "MICRO OVEN"
            itmpri = 75000
            d.destroy()
            mainro()

        o3 = Image.open("home4.jpg")
        bo3 = o3.resize((250, 250), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchaseh5():
            global itmpri, itmnam
            itmnam = "SOFA(L STYLE)"
            itmpri = 75000
            d.destroy()
            mainro()

        o4 = Image.open("home5.jpg")
        bo4 = o4.resize((300, 250), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchaseh6():
            global itmpri, itmnam
            itmnam = "DINNING TABLE(ROYAL STYLISH)"
            itmpri = 185000
            d.destroy()
            mainro()

        o5 = Image.open("HOME6.jpg")
        bo5 = o5.resize((300, 250), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchaseh7():
            global itmpri, itmnam
            itmnam = "BED(WOOD STYLISH)"
            itmpri = 285000
            d.destroy()
            mainro()

        o6 = Image.open("HOME7.jpg")
        bo6 = o6.resize((300, 250), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)

        def purchaseh8():
            global itmpri, itmnam
            itmnam = "BED(ROYAL STYLISH)"
            itmpri = 485000
            d.destroy()
            mainro()

        o7 = Image.open("HOME8.jpg")
        bo7 = o7.resize((300, 250), Image.HUFFMAN_ONLY)
        bl7 = ImageTk.PhotoImage(bo7)

        if savecou>=1:
            Button(d, text='WASHING MACHINE(FRONT LOADED)       Rs - 95,000', image=bl1, compound=TOP,command=purchaseh1).place(x=20, y=30)
            Button(d, text='WASHING MACHINE       Rs - 45,500', image=bl, compound=TOP, command=purchaseh2).place(x=380, y=30)
            Button(d, text='RO       Rs - 59,000', image=bl2, compound=TOP, command=purchaseh3).place(x=690, y=30)
            Button(d, text='MICRO OVEN       Rs - 75,000', image=bl3, compound=TOP, command=purchaseh4).place(x=1000, y=30)
            Button(d, text='SOFA(L STYLE )      Rs - 75,000', image=bl4, compound=TOP, command=purchaseh5).place(x=20, y=320)
            Button(d, text='DINNING TABLE(ROYAL STYLISH)      Rs - 1,85,000', image=bl5, compound=TOP, command=purchaseh6).place(x=340, y=320)
            Button(d, text='BED(WOOD STYLISH)     Rs - 2,85,000', image=bl6, compound=TOP, command=purchaseh7).place(x=660, y=320)
            Button(d, text='BED(ROYAL STYLISH)     Rs - 4,85,000', image=bl7, compound=TOP, command=purchaseh8).place(x=980, y=320)
        if savecou==0:
            Button(d, text='WASHING MACHINE(FRONT LOADED)       Rs - 95,000', image=bl1, compound=TOP).place(x=20, y=30)
            Button(d, text='WASHING MACHINE       Rs - 45,500', image=bl, compound=TOP).place(x=380, y=30)
            Button(d, text='RO       Rs - 59,000', image=bl2, compound=TOP).place(x=690, y=30)
            Button(d, text='MICRO OVEN       Rs - 75,000', image=bl3, compound=TOP).place(x=1000, y=30)
            Button(d, text='SOFA(L STYLE )      Rs - 75,000', image=bl4, compound=TOP).place(x=20, y=320)
            Button(d, text='DINNING TABLE(ROYAL STYLISH)      Rs - 1,85,000', image=bl5, compound=TOP).place(x=340, y=320)
            Button(d, text='BED(WOOD STYLISH)     Rs - 2,85,000', image=bl6, compound=TOP).place(x=660, y=320)
            Button(d, text='BED(ROYAL STYLISH)     Rs - 4,85,000', image=bl7, compound=TOP).place(x=980, y=320)
        def backing():
            d.destroy()
            maiwindow()
        Button(d, text="Back", bg="red", command=backing).place(x=0, y=0)
        d.mainloop()

    def h():
        root.destroy()
        home()

    def toys():
        e = Tk(className=" BuyCart Toys")
        e.geometry("1180x520+0+0")
        e.config(bg="black")

        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(e, text="TOYS", \
              relief='groove', font=myfont).place(width=1200)

        def purchaset1():
            global itmpri, itmnam
            itmnam = "MINECRAFT SET"
            itmpri = 85000
            e.destroy()
            mainro()
        o1 = Image.open("toy1.jpg")
        bo1 = o1.resize((300, 200), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchaset2():
            global itmpri, itmnam
            itmnam = "ROBOT"
            itmpri = 75500
            e.destroy()
            mainro()
        o = Image.open("toy2.jpg")
        bo = o.resize((250, 200), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchaset3():
            global itmpri, itmnam
            itmnam = "JCB ROBOT"
            itmpri = 55000
            e.destroy()
            mainro()

        o2 = Image.open("toy3.jpg")
        bo2 = o2.resize((250, 200), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchaset4():
            global itmpri, itmnam
            itmnam = "MONOPOLY"
            itmpri = 5700
            e.destroy()
            mainro()

        o3 = Image.open("toy4.jpg")
        bo3 = o3.resize((250, 200), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchaset5():
            global itmpri, itmnam
            itmnam = "CAR ROBOT SET"
            itmpri = 75000
            e.destroy()
            mainro()

        o4 = Image.open("toy5.jpg")
        bo4 = o4.resize((300, 200), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchaset6():
            global itmpri, itmnam
            itmnam = "HARRY POTTER SET"
            itmpri = 85000
            e.destroy()
            mainro()

        o5 = Image.open("toy6.jpg")
        bo5 = o5.resize((250, 200), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchaset7():
            global itmpri, itmnam
            itmnam = "PUPPY ROBOT"
            itmpri = 55000
            e.destroy()
            mainro()

        o6 = Image.open("toy7.jpg")
        bo6 = o6.resize((250, 200), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)

        def purchaset8():
            global itmpri, itmnam
            itmnam = "LEGO STAR WAR"
            itmpri = 245000
            e.destroy()
            mainro()

        o7 = Image.open("toy8.jpg")
        bo7 = o7.resize((250, 200), Image.HUFFMAN_ONLY)
        bl7 = ImageTk.PhotoImage(bo7)

        if savecou>=1:
            Button(e, text='MINECRAFT SET       Rs - 85,000', image=bl1, compound=TOP, command=purchaset1).place(x=20, y=40)
            Button(e, text='ROBOT      Rs - 75,500', image=bl, compound=TOP, command=purchaset2).place(x=350, y=40)
            Button(e, text='JCB ROBOT       Rs - 55,000', image=bl2, compound=TOP, command=purchaset3).place(x=630, y=40)
            Button(e, text='MONOPOLY       Rs - 5,700', image=bl3, compound=TOP, command=purchaset4).place(x=900, y=40)
            Button(e, text='CAR ROBOT SET       Rs - 75,000', image=bl4, compound=TOP, command=purchaset5).place(x=20, y=280)
            Button(e, text='HARRY POTTER SET       Rs - 85,000', image=bl5, compound=TOP, command=purchaset6).place(x=350, y=280)
            Button(e, text='PUPPY ROBOT     Rs - 55,000', image=bl6, compound=TOP, command=purchaset7).place(x=630, y=280)
            Button(e, text='LEGO STAR WAR       Rs - 2,45,000', image=bl7, compound=TOP, command=purchaset8).place(x=900, y=280)
        if savecou==0:
            Button(e, text='MINECRAFT SET       Rs - 85,000', image=bl1, compound=TOP).place(x=20, y=40)
            Button(e, text='ROBOT      Rs - 75,500', image=bl, compound=TOP).place(x=350, y=40)
            Button(e, text='JCB ROBOT       Rs - 55,000', image=bl2, compound=TOP).place(x=630, y=40)
            Button(e, text='MONOPOLY       Rs - 5,700', image=bl3, compound=TOP).place(x=900, y=40)
            Button(e, text='CAR ROBOT SET       Rs - 75,000', image=bl4, compound=TOP).place(x=20, y=280)
            Button(e, text='HARRY POTTER SET       Rs - 85,000', image=bl5, compound=TOP).place(x=350, y=280)
            Button(e, text='PUPPY ROBOT     Rs - 55,000', image=bl6, compound=TOP).place(x=630, y=280)
            Button(e, text='LEGO STAR WAR       Rs - 2,45,000', image=bl7, compound=TOP).place(x=900, y=280)

        def backing():
            e.destroy()
            maiwindow()
        Button(e, text="Back", bg="red", command=backing).place(x=0, y=0)
        e.mainloop()

    def t():
        root.destroy()
        toys()

    def beauty():
        f = Tk(className=" BuyCart Beauty")
        f.geometry("1180x520+0+0")
        f.configure(bg="black")
        myfont = font.Font(family="Helvetica", size=16, weight="bold")
        Label(f, text="BEAUTY", \
              relief='groove', font=myfont).place(width=1200)

        def purchaseb1():
            global itmpri, itmnam
            itmnam = "URBAN NIGHT(PERFUME)"
            itmpri = 5000
            f.destroy()
            mainro()
        o1 = Image.open("beauty1.jpg")
        bo1 = o1.resize((300, 200), Image.HUFFMAN_ONLY)
        bl1 = ImageTk.PhotoImage(bo1)

        def purchaseb2():
            global itmpri, itmnam
            itmnam = "PEARL(PERFUME)"
            itmpri = 5500
            f.destroy()
            mainro()
        o = Image.open("beauty2.jpg")
        bo = o.resize((250, 200), Image.HUFFMAN_ONLY)
        bl = ImageTk.PhotoImage(bo)

        def purchaseb3():
            global itmpri, itmnam
            itmnam = "LOTUS(CREAM)"
            itmpri = 55000
            f.destroy()
            mainro()

        o2 = Image.open("beauty3.jpg")
        bo2 = o2.resize((250, 200), Image.HUFFMAN_ONLY)
        bl2 = ImageTk.PhotoImage(bo2)

        def purchaseb4():
            global itmpri, itmnam
            itmnam = "LAKME ABSOLUTE(CREAM)"
            itmpri = 5700
            f.destroy()
            mainro()

        o3 = Image.open("beauty4.jpg")
        bo3 = o3.resize((250, 200), Image.HUFFMAN_ONLY)
        bl3 = ImageTk.PhotoImage(bo3)

        def purchaseb5():
            global itmpri, itmnam
            itmnam = "TRIMMER"
            itmpri = 15000
            f.destroy()
            mainro()

        o4 = Image.open("beauty5.jpg")
        bo4 = o4.resize((300, 200), Image.HUFFMAN_ONLY)
        bl4 = ImageTk.PhotoImage(bo4)

        def purchaseb6():
            global itmpri, itmnam
            itmnam = "COMB"
            itmpri = 5200
            f.destroy()
            mainro()

        o5 = Image.open("beauty6.jpg")
        bo5 = o5.resize((250, 200), Image.HUFFMAN_ONLY)
        bl5 = ImageTk.PhotoImage(bo5)

        def purchaseb7():
            global itmpri, itmnam
            itmnam = "MAKE-UP KIT"
            itmpri = 55000
            f.destroy()
            mainro()

        o6 = Image.open("beauty8.jpg")
        bo6 = o6.resize((250, 200), Image.HUFFMAN_ONLY)
        bl6 = ImageTk.PhotoImage(bo6)

        def purchaseb8():
            global itmpri, itmnam
            itmnam = "ONION BLACK SEED HAIR OIL"
            itmpri = 5200
            f.destroy()
            mainro()

        o7 = Image.open("beauty7.jpg")
        bo7 = o7.resize((250, 200), Image.HUFFMAN_ONLY)
        bl7 = ImageTk.PhotoImage(bo7)
        if savecou>=1:
            Button(f, text='URBAN NIGHT(PERFUME)       Rs - 5,000', image=bl1, compound=TOP, command=purchaseb1).place(x=20, y=40)
            Button(f, text='PEARL(PERFUME)      Rs - 5,500', image=bl, compound=TOP, command=purchaseb2).place(x=350, y=40)
            Button(f, text='LOTUS(CREAM)      Rs - 55,000', image=bl2, compound=TOP, command=purchaseb3).place(x=630, y=40)
            Button(f, text='LAKME ABSOLUTE (CREAM)      Rs - 5,700', image=bl3, compound=TOP, command=purchaseb4).place(x=900, y=40)
            Button(f, text='TRIMMER       Rs - 15,000', image=bl4, compound=TOP, command=purchaseb5).place(x=20, y=280)
            Button(f, text='COMB       Rs - 5,200', image=bl5, compound=TOP, command=purchaseb6).place(x=350, y=280)
            Button(f, text='MAKE-UP  KIT    Rs - 55,000', image=bl6, compound=TOP, command=purchaseb7).place(x=630, y=280)
            Button(f, text='ONION BLACK SEED HAIR OIL       Rs - 5,200', image=bl7, compound=TOP, command=purchaseb8).place(x=900, y=280)
        if savecou==0:
            Button(f, text='URBAN NIGHT(PERFUME)       Rs - 5,000', image=bl1, compound=TOP).place(x=20, y=40)
            Button(f, text='PEARL(PERFUME)      Rs - 5,500', image=bl, compound=TOP).place(x=350, y=40)
            Button(f, text='LOTUS(CREAM)      Rs - 55,000', image=bl2, compound=TOP).place(x=630, y=40)
            Button(f, text='LAKME ABSOLUTE (CREAM)      Rs - 5,700', image=bl3, compound=TOP).place(x=900, y=40)
            Button(f, text='TRIMMER       Rs - 15,000', image=bl4, compound=TOP).place(x=20, y=280)
            Button(f, text='COMB       Rs - 5,200', image=bl5, compound=TOP).place(x=350, y=280)
            Button(f, text='MAKE-UP  KIT    Rs - 55,000', image=bl6, compound=TOP).place(x=630, y=280)
            Button(f, text='ONION BLACK SEED HAIR OIL       Rs - 5,200', image=bl7, compound=TOP).place(x=900, y=280)

        def backing():
            f.destroy()
            maiwindow()
        Button(f, text="Back", bg="red", command=backing).place(x=0, y=0)
        f.mainloop()

    def bea():
        root.destroy()
        beauty()

    def GOgame():
        root.destroy()
        YGgames()
    def orders():
        mycursor.execute(f'select Product_Name,prise from orders where gmail="{couvar}"')
        extra = mycursor.fetchall()
        order = Tk(className=" My Orders")
        order.geometry("900x500")
        Label(order, text="My Orders", font=('times new roman', 20, 'bold')).place(x=400, y=0)
        Label(order, text="Product", font=('times new roman', 15, 'bold')).place(x=300, y=50)
        Label(order, text="Prize", font=('times new roman', 15, 'bold')).place(x=600, y=50)
        xinc=300
        yinc=100
        for a in range(len(extra)):
            Label(order, text=extra[a][0], bg="SeaGreen1").place(x=xinc, y=yinc)
            Label(order, text=extra[a][1], bg='gold').place(x=xinc+300, y=yinc)
            yinc+=50
        def back():
            order.destroy()
            maiwindow()
        Button(order, text='Back', bg='red', command=back).place(x=0, y=0)

    def showorder():
        root.destroy()
        orders()

    def accountset():
        acc = Tk(className="My account")
        acc.geometry("900x600")
        mycursor.execute(f'select * from users where gmail="{couvar}"')
        ac = mycursor.fetchall()
        Label(acc, text="My Account", font=('times new roman', 20, 'bold')).place(x=300, y=0)
        Label(acc, text="Name:").place(x=300, y=50)
        Label(acc, text="Gender:").place(x=300, y=150)
        Label(acc, text="Address:").place(x=300, y=200)
        Label(acc, text="Gmail:").place(x=300, y=300)
        Label(acc, text="Password:").place(x=300, y=350)
        yinc = 50
        print(ac)
        for a in range(5):
            Label(acc, text=ac[0][a]).place(x=400, y=yinc)
            if a!=1 and a!=3:
                yinc += 100
            else:
                yinc +=50

        def addresschange():
            acc.destroy()
            address = Tk(className="Address")
            address.geometry("500x300")
            Label(address, text="New Address").place(x=100, y=100)
            add = StringVar()
            Entry(address, textvariable=add).place(x=200, y=100)
            def chan():
                ch = add.get()
                mycursor.execute(f"update users set address='{ch}' where gmail='{couvar}'")
                mydb.commit()
                address.destroy()
                login()

            Button(address, text="Change Address", command=chan).place(x=150, y=200)

        def namechange():
            acc.destroy()
            address = Tk(className="Name")
            address.geometry("500x300")
            Label(address, text="New Name").place(x=100, y=100)
            add = StringVar()
            Entry(address, textvariable=add).place(x=200, y=100)
            def chan():
                ch = add.get()
                mycursor.execute(f"update users set userName='{ch}' where gmail='{couvar}'")
                mydb.commit()
                address.destroy()
                login()

            Button(address, text="Change Name", command=chan).place(x=150, y=200)

        def passwrdchange():
            acc.destroy()
            address = Tk(className=" Password")
            address.geometry("500x300")
            Label(address, text="New Password").place(x=100, y=100)
            add = StringVar()
            Entry(address, textvariable=add).place(x=200, y=100)
            def chan():
                ch = add.get()
                mycursor.execute(f"update users set Password='{ch}' where gmail='{couvar}'")
                mydb.commit()
                address.destroy()
                login()

            Button(address, text="Change Password", command=chan).place(x=150, y=200)

        def back():
            acc.destroy()
            maiwindow()
        Button(acc, text='Back', bg='red', command=back).place(x=0, y=0)
        Button(acc, text='Change', bg='light blue', command=namechange).place(x=400, y=100)
        Button(acc, text='Change', bg='light blue', command=addresschange).place(x=400, y=250)
        Button(acc, text='Change', bg='light blue', command=passwrdchange).place(x=400, y=400)

    def account():
        root.destroy()
        accountset()

    def cancelord():
        root.destroy()
        cancel = Tk()
        cancel.geometry("600x300")
        Label(cancel, text="Product Name").place(x=100, y=50)
        can = StringVar()
        Entry(cancel, textvariable=can).place(x=200, y=50)
        def cancell():
            canc = can.get()
            mycursor.execute(f"delete from orders where Product_Name='{canc}' and gmail='{couvar}'")
            mydb.commit()
            tmsg.showinfo("Cancel Order","Order will be cancelled Shortly! if u have ordered it")
            cancel.destroy()

        Label(cancel, text="Warning :- Please Submit the Correct Name of product", fg='red').place(x=100, y=100)
        Button(cancel, text="Cancel Order", bg='red', command=cancell).place(x=150, y=150)

    img1 = Image.open("yathuu.jpg")
    img1 = img1.resize((300, 150), Image.HUFFMAN_ONLY)
    img1 = ImageTk.PhotoImage(img1)
    Button(root, text='ELECTRONICS ', image=img1, compound=TOP, command=ele).place(x=60, y=50)

    img2 = Image.open('yathuu2.jpg')
    img2 = img2.resize((300, 150), Image.HUFFMAN_ONLY)
    img2 = ImageTk.PhotoImage(img2)
    Button(root, text='TOYS ', image=img2, compound=TOP, command=t).place(x=380, y=50)

    img3 = Image.open('yathuu3.jpg')
    img3 = img3.resize((300, 150), Image.HUFFMAN_ONLY)
    img3 = ImageTk.PhotoImage(img3)
    Button(root, text='FASHION', image=img3, compound=TOP, command=c).place(x=700, y=50)

    img4 = Image.open('yathuu4.jpg')
    img4 = img4.resize((300, 150), Image.HUFFMAN_ONLY)
    img4 = ImageTk.PhotoImage(img4)
    Button(root, text='SPORTS ', image=img4,    compound=TOP,command=s).place(x=60, y=350)

    img5 = Image.open('yathuu5.jpg')
    img5 = img5.resize((300, 150), Image.HUFFMAN_ONLY)
    img5 = ImageTk.PhotoImage(img5)
    Button(root, text='HOME APPLIANCES', image=img5, compound=TOP, command=h).place(x=380, y=350)

    img6 = Image.open('yathuu1.jpg')
    img6 = img6.resize((300, 150), Image.HUFFMAN_ONLY)
    img6 = ImageTk.PhotoImage(img6)
    Button(root, text='BEAUTY', image=img6, compound=TOP, command=bea).place(x=700, y=350)

    if savecou==1:
        menubar = Menu(root)
        m1 = Menu(menubar, tearoff=0)
        m1.add_command(label="Games" , command=GOgame)
        m1.add_command(label='My orders', command=showorder)
        m1.add_command(label="My account", command=account)
        m1.add_command(label="Cancel order", command=cancelord)
        root.config(menu=menubar)
        menubar.add_cascade(label='Options', menu=m1)

    root.mainloop()
def OTPGEN():
    import random
    OTP = random.random()
    OTP = OTP * 10000
    OTP = round(OTP)
    print(OTP)
    s = smt.SMTP('smtp.gmail.com', '587')
    s.starttls()
    s.login('Gmail-Address', 'Gmail-password')
    m = f"This is your YG BuyCart {OTP}"
    if issign==1:
        s.sendmail("Gmail-Address", signgmail, m)
    elif issign==2:
        s.sendmail("Gmail-Address", logingmail, m)
    s.quit()
    return OTP

def signfunc():  # This is signup program using database connectivity
    signupfunc = Tk(className=' BuyCart SignUp')
    signupfunc.geometry("850x650")
    signupfunc.minsize(850, 650)
    signupfunc.maxsize(850, 650)
    signupfunc.config(bg='pink')
    o = Image.open('prologo.jpeg')
    bo = o.resize((200, 120), Image.HUFFMAN_ONLY)
    bl = ImageTk.PhotoImage(bo)
    Label(signupfunc, image=bl).place(x=315, y=10, width=200, height=120)
    newfont1 = font.Font(size=9, weight="bold")
    newfont = font.Font(family="Helvetica", size=20, weight="bold")
    Label(signupfunc, text='Signup', font=newfont).place(x=360, y=140)

    def signupdate():
        global userhello,signgmail
        userhello=UserName.get()
        signgmail = Gmail.get()
        value = UserName.get()
        value1 = gender.get()
        value3 = Address.get()
        value4 = Gmail.get()
        value5 = password.get()
        value6 = conpassword.get()
        value7 = TC.get()
        a = 0
        mycursor.execute("select * from users")
        fe = mycursor.fetchall()
        if value == '' or value == ' ':
            a = a + 1
            P = Label(text="Invalid UserName", bg='pink')
            P.place(x=370, y=220)
        if a == 0:
            if value1 == 'Radio':
                a = a + 1
                Label(text='Choose your gender', bg='red').place(x=400, y=255)
            if a == 0:
                if value3 == '' or value3 == ' ':
                    a = a + 1
                    Label(text='Invalid Address', bg='red').place(x=410, y=299)
            if a == 0:
                lowervalue4 = value4.lower()
                if value4 == '' or value4 == ' ' or lowervalue4.endswith('@gmail.com') == False:
                    a = a + 1
                    Label(text='Invalid Gmail', bg='red').place(x=410, y=339)
            if a == 0:
                if value5 == '' or value5 == " ":
                    a = a + 1
                    Label(text='Invalid Password', bg='red').place(x=410, y=379)
                if a == 0:
                    if value5 != value6:
                        a = a + 1
                        Label(text="Password does not match", bg='red').place(x=390, y=419)
        if a == 0:
            if value == value5:
                Label(text='UserName is much similar to password', bg='pink').place(x=450, y=379)
                a = a + 1
        if a == 0:
            for x in fe:
                print(x)
                print(x[3])
                if x[3] == value4:
                    a = a + 1
                    Label(signupfunc, text='Gmail address already exists', bg='pink').place(x=400, y=339)
                    print('Gmail already exists')
                    break
        print('success')
        if a == 0:
            if value7 == 0:
                a = a + 1
                Label(text='Do agree to our T&C', bg='pink').place(x=400, y=470)
        if a == 0:
            signupfunc.destroy()
            runit()

    def runit():
        global issign,couvar,savecou
        issign=issign+1
        couvar=Gmail.get()
        savecou=savecou+1
        window = Tk(className=" BuyCart OTP Verification")
        window.config(bg='black')
        window.geometry("500x400+0+0")
        window.minsize(500, 400)
        window.maxsize(500, 400)
        OPT1 = IntVar()
        Label(window, text='OTP').place(x=200, y=100)
        Entry(window, textvariable=OPT1).place(x=250, y=100)
        value = UserName.get()
        value1 = gender.get()
        value3 = Address.get()
        value4 = Gmail.get()
        value5 = password.get()
        OTP = OTPGEN()

        def insert():
            print(str(OTP))
            OK = OPT1.get()
            print('this' + str(OK))
            print('this is', OK)
            if OTP == OK:
                mycursor.execute(
                    "insert into users(USERNAME,GENDER,ADDRESS,GMAIL,PASSWORD) values('{}','{}','{}','{}','{}')".format(
                        value, value1, value3, value4, value5))
                mydb.commit()
                print("successfully sign up")
                window.destroy()
                maiwindow()
            if OTP != OK:
                Label(window, text="Invalid OTP").place(x=350, y=300)
        Button(window, text='Submit OTP', command=insert).place(x=220, y=150)

    def click(event):
        global c,myLabel
        if c != 0:
            c = c - 1
        if c < 8:
            myLabel = Label(signupfunc, text='Username must carry 8 characters', bg='pink')
            myLabel.place(x=370, y=220)
        if c >= 8:
            Label(signupfunc, text="                                                          ", bg='pink').place(x=370,y=220)

    def clicker(event):
        global c,myLabel
        c = c + 1
        if c < 8:
            myLabel = Label(signupfunc, text='Username must carry 8 characters', bg='pink')
            myLabel.place(x=370, y=220)
        if c >= 8:
            #myLabel.pack_forget()
            Label(signupfunc, text="                                                          ", bg='pink').place(x=370,y=220)
    def markstar1():
        if starvar1.get() == 1:
            EP1.configure(show="")
        elif starvar1.get() == 0:
            EP1.configure(show="*")

    def markstar():
        if starvar.get() == 1:
            EP.configure(show="")
        elif starvar.get() == 0:
            EP.configure(show="*")

    def loginsign():
        signupfunc.destroy()
        login()
    def hover_in(event):
        hoveff["bg"] = "red"
    def hover_out(event):
        hoveff["bg"] = "SystemButtonFace"
    Label(signupfunc, text="Username", bg='pink').place(x=300, y=200)
    Label(signupfunc, text='Gender', bg='pink').place(x=300, y=240)
    Label(signupfunc, text="Address", bg='pink').place(x=300, y=280)
    Label(signupfunc, text="Gmail", bg='pink').place(x=300, y=320)
    Label(signupfunc, text="Password", bg='pink').place(x=300, y=360)
    Label(signupfunc, text="Confirm Password", bg='pink').place(x=300, y=400)
    UserName = StringVar()
    Address = StringVar()
    Gmail = StringVar()
    password = StringVar()
    conpassword = StringVar()
    gender = StringVar()
    gender.set('Radio')
    TC = IntVar()
    starvar = IntVar()
    starvar1 = IntVar()
    E = Entry(signupfunc, textvariable=UserName)
    E.bind("<Key>", clicker)
    E.bind("<BackSpace>", click)
    E.place(x=400, y=200)
    Radiobutton(signupfunc, text='MALE', variable=gender, bg='pink', font=newfont1, value='MALE').place(x=400, y=240, width=50, height=20)
    Radiobutton(signupfunc, text='FEMALE', variable=gender, bg='pink', font=newfont1, value='FEMALE').place(x=460, y=240, width=70, height=20)
    Entry(signupfunc, textvariable=Address).place(x=400, y=280)
    Entry(signupfunc, textvariable=Gmail).place(x=400, y=320)
    EP = Entry(signupfunc, textvariable=password, show='*')
    EP.place(x=400, y=360)
    Checkbutton(signupfunc, command=markstar, offvalue=0, onvalue=1, variable=starvar, bg='deepskyblue2').place(x=530, y=360)
    EP1 = Entry(signupfunc, textvariable=conpassword, show="*")
    EP1.place(x=400, y=400)
    Checkbutton(signupfunc, command=markstar1, offvalue=0, onvalue=1, variable=starvar1, bg='deepskyblue2').place(x=530, y=400)
    Checkbutton(signupfunc, text='I agree to your T&C', bg='grey', variable=TC).place(x=400, y=440)
    Button(signupfunc, text='Submit', command=signupdate, bg="green").place(x=315, y=500, width=200)
    Button(signupfunc, text='Already have a account? Login', command=loginsign).place(x=332, y=550)
    hoveff = Button(signupfunc, text='EXIT')
    hoveff.place(x=380, y=600, width=60)
    hoveff.bind("<Enter>", hover_in)
    hoveff.bind("<Leave>", hover_out)
    signupfunc.mainloop()

def dest1():  # This is destroy func for signup
    root.destroy()
    signfunc()

def login():
    loginfunc = Tk(className=' BuyCart')
    loginfunc.geometry("800x600")
    loginfunc.minsize(800, 600)
    loginfunc.maxsize(800, 600)
    loginfunc.configure(bg='pink')
    o = Image.open('prologo.jpeg')
    bo = o.resize((200, 120), Image.HUFFMAN_ONLY)
    bl = ImageTk.PhotoImage(bo)
    Label(loginfunc, image=bl).place(x=300, y=10, width=200, height=120)
    newfont = font.Font(family="Helvetica", size=20, weight="bold")
    Label(loginfunc, text='Login', font=newfont).place(x=360, y=140)

    def logcheck():
        global couvar,savecou,userhello
        couvar=UserId.get()
        value = UserId.get()
        value1 = password.get()
        mycursor.execute('select * from users')
        fe=mycursor.fetchall()
        L = 0
        for a in fe:
            if a[3]== value and a[4]==value1:
                L=L+1
                userhello=a[0]
                loginfunc.destroy()
                savecou += 1
                maiwindow()
                print('loginsuccessful')
        if L==0:
            Label(loginfunc, text='Invalid Gmail or Password', bg='red').place(x=300, y=200, width=200)
    def markstar():
        if starvar.get() == 1:
            EP1.configure(show="")
        elif starvar.get() == 0:
            EP1.configure(show="*")
    def forpass():
        loginfunc.destroy()
        root=Tk(className=' Reset Password')
        root.config(bg="black")
        root.geometry('600x400')
        root.minsize(600,400)
        root.maxsize(600,400)
        valr = StringVar()
        valr1 = StringVar()
        valr2 = StringVar()
        starvar1 = IntVar()
        starvar2 = IntVar()
        def reset():
            global couvar,savecou
            savecou+=1
            couvar=valr.get()
            K=0
            value=valr.get()
            value1=valr1.get()
            value2=valr2.get()
            lowervalue = value.lower()
            if value == '' or value == ' ' or lowervalue.endswith('@gmail.com') == False:
                K = K + 1
                Label(text='Invalid Gmail address', bg='red').place(x=300, y=125)
            B = 0
            if K == 0:
                mycursor.execute('select gmail from users')
                f = mycursor.fetchall()
                for a in f:
                    print(a[0])
                    if a[0]==value:
                        B+=1
                if B==0:
                    K+=1
                    Label(text='Gmail address does not exists', bg='red').place(x=290, y=125)

            if K==0:
                if value1 == '' or value2 == " ":
                    K = K + 1
                    Label(text='Invalid Password', bg='red').place(x=320, y=175)
            if K == 0:
                if value1 != value2:
                    K = K + 1
                    Label(text="Password does not match", bg='red').place(x=290, y=230)
            if K == 0:
                root.destroy()
                global issign,logingmail
                issign = issign + 2
                logingmail=logingmail+value
                window = Tk()
                window.geometry("500x400+0+0")
                window.config(bg="black")
                window.minsize(500, 400)
                window.maxsize(500, 400)
                OPT1 = IntVar()
                Label(window, text='OTP').place(x=200, y=100)
                Entry(window, textvariable=OPT1).place(x=250, y=100)
                OTP = OTPGEN()

                def insert():
                    global userhello
                    print(str(OTP))
                    OK = OPT1.get()
                    print('this' + str(OK))
                    print('this is', OK)
                    if OTP == OK:
                        mycursor.execute("update users set password='{}' where gmail='{}'".format(value1,value))
                        mydb.commit()
                        print("password reset successful")
                        window.destroy()
                        mycursor.execute(f'select username from users where gmail="{value}"')
                        stor = mycursor.fetchall()
                        userhello = stor[0][0]
                        maiwindow()
                    if OTP != OK:
                        Label(window, text="Invalid OTP", bg="red").place(x=150, y=150)

                Button(window, text='Submit OTP', command=insert).place(x=220, y=200)
                window.mainloop()
        def markstar1():
            if starvar1.get() == 1:
                EP.configure(show="")
            elif starvar1.get() == 0:
                EP.configure(show="*")
        def markstar():
            if starvar2.get() == 1:
                EP2.configure(show="")
            elif starvar2.get() == 0:
                EP2.configure(show="*")
        Entry(root, textvariable=valr).place(x=300,y=100)
        Checkbutton(root, command=markstar1, offvalue=0, onvalue=1, variable=starvar1, bg='deepskyblue2').place(
            x=450, y=150)
        Checkbutton(root, command=markstar, offvalue=0, onvalue=1, variable=starvar2, bg='deepskyblue2').place(x=450, y=200)
        EP = Entry(root, textvariable=valr1, show="*")
        EP.place(x=300, y=150)
        EP2 = Entry(root, textvariable=valr2, show="*")
        EP2.place(x=300, y=200)
        Label(root, text='Gmail').place(x=180, y=100)
        Label(root, text='Password').place(x=180, y=150)
        Label(root, text='Confirm Password').place(x=180, y=200)
        Button(root, text='Reset Password', command=reset, bg='seagreen1').place(x=250, y=280)
        root.mainloop()
    starvar=IntVar()
    user = Label(loginfunc, text="Gmail", bg='pink')
    passwd = Label(loginfunc, text="Password", bg='pink')
    user.place(x=300, y=230)
    passwd.place(x=300, y=280)
    UserId = StringVar()
    password = StringVar()
    Entry(loginfunc, textvariable=UserId).place(x=375, y=230)
    EP1=Entry(loginfunc, textvariable=password, show="*")
    Checkbutton(loginfunc, command=markstar, offvalue=0, onvalue=1, variable=starvar, bg='deepskyblue2').place(x=510,
                                                                                                                y=280)
    EP1.place(x=375, y=280)
    Button(loginfunc, text='Forget password?', bg='pink', fg='blue', command=forpass).place(x=395, y=320)
    Button(loginfunc, text='Submit', bg='green', command=logcheck).place(x=300, y=390, width=200)

    def delee():
        loginfunc.destroy()
        signfunc()

    Button(loginfunc, text="Don't have a account! SignUp", command=delee).place(x=315, y=460)
    Button(loginfunc, text='EXIT').place(x=380, y=510)
    loginfunc.mainloop()

def dest():
    root.destroy()
    login()

def guestwin():
    root.destroy()
    maiwindow()

# set width and height
L = Image.open('BUycart.jpg')
bp = L.resize((900, 700), Image.HUFFMAN_ONLY)
bg = ImageTk.PhotoImage(bp)
by = Label(root, image=bg, ).place(x=200, y=0, relwidth=1, relheight=1)
root.config(bg='white')
o = Image.open('prologo.jpeg')
bo = o.resize((355, 250), Image.HUFFMAN_ONLY)
bl = ImageTk.PhotoImage(bo)
ba = Label(root, image=bl).place(x=80, y=200, width=350, height=250)
myfont = font.Font(family='comicsansms', size=15, weight='bold')
b2 = Button(root, text="Enter as guest", height=5, width=15, bg='white', font='myfont', relief='ridge',
            activebackground='cyan', command=guestwin)
b2.place(relx=0.48, rely=0.29, anchor=NW)

b3 = Button(root, text='Games', height=5, width=15, bg='white', font='myfont', relief='ridge', activebackground='cyan',command=sgames)
b3.place(relx=0.48, rely=0.495)

b4 = Button(root, text='Login', height=5, width=15, bg='white', font='myfont', relief='ridge', \
            activebackground='cyan', command=dest)
b4.place(relx=0.72, rely=0.29)

newfont = font.Font(family="Helvetica", size=16, weight="bold")

b5 = Button(root, text='Signup', height=5, width=15, bg='white', font='myfont', relief='ridge', activebackground='cyan', command=dest1)
b5.place(relx=0.72, rely=0.495)
Label(root, text='In order to be irreplaceable one should always be different.\n   YG BuyCart...India ki apni dukaan',
      bg='pink', relief='ridge', font=newfont).place(x=80, y=450, width=713, height=60)

Button(root, text='EXIT', font=newfont, bg='red', command=lambda: root.destroy()).place(x=450, y=630)

a = ' Welcome to BuyCart                     '  # wlcm animation code begins
statusvar = StringVar()
statusvar.set('')
sbar = Label(root, textvariable=statusvar, bg='pink', font=('times new roman', 20, 'bold'))
sbar.pack()
b = ''
k = 0
while True:
    print(Y)
    for i in a:
        b = b + i
        if k != 0:
            time.sleep(0.1)
            print(b)
        statusvar.set(b)
        sbar.update()
        k += 1
    print(b)
    b.format()
    statusvar.set(b)
    sbar.update()

root.mainloop()
