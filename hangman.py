#HANGMAN Game
#Made by Tharunkrishna T H
#Credits: (https://github.com/dolph/dictionary/blob/master/popular.txt for the words)
#Discord: wrecker696

import random
import subprocess
import sys

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
try:
    import mysql.connector as mysq
    import pyfiglet
    from colorama import Fore,Back,Style,init
 
except ImportError:
    install_requirements()
    import mysql.connector as mysq
    import pyfiglet
    from colorama import Fore,Back,Style,init

db = mysq.connect(user = "root",host = "localhost",password = "fury")
cur = db.cursor()
def randwgen():
    fin = open("word_data.txt", 'r')
    body = fin.read().split("\n")
    randomw = random.choice(body)
    return randomw

curuser = ""
curlevel = 1
curscore = 0
curreset = 0
curlevellist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def changelevelcol():
    disp = []
    for i, level in enumerate(curlevellist):
        if int(level) > int(curlevel):
            disp.append(f"{Fore.RED}{i + 1}{Style.RESET_ALL}")
        elif int(level) == int(curlevel):
            disp.append(f"{Fore.CYAN}[{Style.RESET_ALL}{i + 1}{Fore.CYAN}]{Style.RESET_ALL}")
        else:
            disp.append(f"{Fore.GREEN}{i + 1}{Style.RESET_ALL}")
    return disp

def createdatab():
    cur.execute("show databases like 'hangman_xen';")
    cur.fetchall()
    if cur.rowcount == 0:
        cur.execute("create database hangman_xen;")
        cur.execute("use hangman_xen;")
    else:
        cur.execute("use hangman_xen;")
def createtabs():
    cur.execute("show tables like 'user_%';")
    cur.fetchall()
    if cur.rowcount == 0:
        cur.execute("create table user_details(username varchar(20), password varchar(20));")
        cur.execute("create table user_progress(username varchar(20), level int, score int, resetted_score int);")

def sintro():
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    title = pyfiglet.figlet_format('BASIC PROJECT 1', font='banner3-D')
    print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(f"\t\t\t\t                      -{Fore.YELLOW}A Basic project{Style.RESET_ALL} by {Fore.RED}Tharunkrishna T H{Style.RESET_ALL}")
    print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def checkinfo(h):
    userf = ""
    passf = ""
    if h == 1:
        while True:
            inp1 = input(f"\t|\t{Fore.BLUE}Enter your username:{Style.RESET_ALL}")
            if inp1.isdigit():
                print(f"\t|\t{Fore.RED}The username cannot contain only numbers...{Style.RESET_ALL}")
            elif " " in inp1:
                print(f"\t|\t{Fore.RED}No spaces are allowed...{Style.RESET_ALL}")
            elif len(inp1) < 4:
                print(f"\t|\t{Fore.RED}Username has to be more than 3 characters...{Style.RESET_ALL}")
            else:
                userf = inp1
                break

        while True:
            inp2 = input(f"\t|\t{Fore.BLUE}Enter your password:{Style.RESET_ALL}")
            if " " in inp2:
                print(f"\t|\t{Fore.RED}No spaces are allowed...{Style.RESET_ALL}")
            elif len(inp2) < 4:
                print(f"\t|\t{Fore.RED}Password has to be more than 3 characters...{Style.RESET_ALL}")
            else:
                passf = inp2
                break

    if h == 2:
        while True:
            inp1 = input(f"\t|\t{Fore.BLUE}Enter your username:{Style.RESET_ALL}")
            if inp1.isdigit():
                print(f"\t|\t{Fore.RED}The username cannot contain only numbers...{Style.RESET_ALL}")
            elif " " in inp1:
                print(f"\t|\t{Fore.RED}No spaces are allowed...{Style.RESET_ALL}")
            elif len(inp1) < 4:
                print(f"\t|\t{Fore.RED}Username has to be more than 3 characters...{Style.RESET_ALL}")
            else:
                userf = inp1
                break

        while True:
            inp2 = input(f"\t|\t{Fore.BLUE}Enter your password:{Style.RESET_ALL}")
            if " " in inp2:
                print(f"\t|\t{Fore.RED}No spaces are allowed...{Style.RESET_ALL}")
            elif len(inp2) < 4:
                print(f"\t|\t{Fore.RED}Password has to be more than 3 characters...{Style.RESET_ALL}")
            else:
                passf = inp2
                break
    return userf, passf

def starti():
    print("\t|\t1) Login.")
    print("\t|\t2) Sign Up.")
    while True:
        emtp()
        inp1 = input(f"\t|\t{Fore.MAGENTA}Enter the number corresponding to your desired action: {Style.RESET_ALL}")
        emtp()
        if not str(inp1).isdigit():
            print(f"\t|\t{Fore.RED}Enter a valid number (1 or 2)...{Style.RESET_ALL}")
        elif " " in str(inp1):
            print(f"\t|\t{Fore.RED}No spaces are allowed...{Style.RESET_ALL}")
        elif len(str(inp1)) != 1:
            print(f"\t|\t{Fore.RED}Enter a valid number (1 or 2)...{Style.RESET_ALL}")
        elif str(inp1) not in ["1", "2"]:
            print(f"\t|\t{Fore.RED}Enter a valid number (1 or 2)...{Style.RESET_ALL}")
        else:
            if inp1 == str(1):
                login()
                break
            else:
                register()
                break

def emtp():
    print("\t|\t")
print("")
def login():
    print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\t|\tLogin!")
    print("\t|\t______")
    emtp()
    global curuser, curlevel, curscore, curreset
    usern, passwd = checkinfo(1)
    cur.execute("select * from user_details;")
    data = cur.fetchall()
    userfound = False
    for i in data:
        if i[0] == usern:
            userfound = True
            if i[1] == passwd:
                emtp()
                print(f"\t|\t{Fore.GREEN}Logged In!{Style.RESET_ALL}")
                emtp()
                curuser = usern
                cur.execute(f"select * from user_progress where username = '{curuser}';")
                datate = cur.fetchone()
                curlevel = int(datate[1])
                curscore = int(datate[2])
                curreset = int(datate[3])
                mainmenu() 
                return
            else:
                emtp()
                print(f"\t|\t{Fore.RED}The password is wrong...{Style.RESET_ALL}")
                emtp()
                login() 
                return

    if not userfound:
        emtp()
        print(f"\t|\t{Fore.RED}User not found...{Style.RESET_ALL}")
        print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    starti()

def updatescore():
    cur.execute(f"select * from user_progress where username = '{curuser}';")
    datate = cur.fetchone()
    curlevel = int(datate[1])
    curscore = int(datate[2])
    curreset = int(datate[3])

def mainmenu():
    global curuser, curlevel, curscore, curreset
    emtp()
    print("_______________________________________________________________________________")
    
    cur.execute(f"select * from user_progress where username = '{curuser}';")
    datate = cur.fetchone()
    curlevel = int(datate[1])
    curscore = int(datate[2])
    curreset = int(datate[3])
    
    title = pyfiglet.figlet_format('HANGMAN', font='poison')
    print(f'{Fore.RED}{title}{Style.RESET_ALL}')
    print("_______________________________________________________________________________")
    print(f"\t|\t                                         User: {Fore.BLUE}{curuser}{Style.RESET_ALL}")
    print(f"\t|\t{Fore.GREEN}1){Style.RESET_ALL} Play.                                  Score: {Fore.BLUE}{curscore}{Style.RESET_ALL}")
    print(f"\t|\t{Fore.GREEN}2){Style.RESET_ALL} Levels.                               Resetted: {Fore.BLUE}{curreset}{Style.RESET_ALL}")
    print(f"\t|\t{Fore.GREEN}3){Style.RESET_ALL} Tutorial.")
    print(f"\t|\t{Fore.GREEN}4){Style.RESET_ALL} Leaderboard.")
    print(f"\t|\t{Fore.MAGENTA}5){Style.RESET_ALL} Reset.")
    print(f"\t|\t{Fore.RED}6){Style.RESET_ALL} Exit.")
    emtp()

    while True:
        ch = input(f"\t|\t{Fore.LIGHTGREEN_EX}Enter the number corresponding to your desired action: {Style.RESET_ALL}")

        if ch == "1":
            ch2 = input(f"\t|\t{Fore.YELLOW}Click Enter to Continue:{Style.RESET_ALL}")
            emtp()
            hangman_game(curlevel)

        elif ch == "2":
            changelevelcol()
            emtp()
            print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("\t|\tLevels")
            print("\t|\t______")
            emtp()
            print("\t|\t", end="")
            teml = changelevelcol()
            for i in teml[:(len(teml)) + 1]:
                print(i, end="  ")
            print("\n\t|\t")
            if teml[-1] == f"{Fore.GREEN}10{Style.RESET_ALL}":
                emtp()
                print(f"\t|\t{Fore.GREEN}You have Completed the Game C:{Style.RESET_ALL}")
            emtp()
            print(f"\t|\t{Fore.CYAN}[]{Style.RESET_ALL} - Current Level\n\t|\t{Fore.RED}Red - Locked{Style.RESET_ALL}\n\t|\t{Fore.GREEN}Green - Completed that level{Style.RESET_ALL}\n\t|\t")
            chl = input(f"\t|\t{Fore.YELLOW}Click Enter to go back:{Style.RESET_ALL}")
            mainmenu()
        elif ch == "3":
            emtp()
            print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("\t|\tTutorial")
            print("\t|\t________")
            emtp()
            print(f"\t|\t\t\t{Fore.RED}Welcome to Hangman!{Style.RESET_ALL}")
            emtp()
            
            with open("tutorial.txt", "r") as tfile:
                tutorial_text = tfile.readlines()
                for i in tutorial_text:
                    print("\t|\t" + i.rstrip("\n"))
            
            emtp()
            cht = input(f"\t|\t{Fore.YELLOW}Click Enter to go back:{Style.RESET_ALL}")
            mainmenu()

        elif ch == "4":
            cur.execute("select * from user_progress order by score DESC")
            results = cur.fetchall()
            emtp()
            print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("\t|\tLeaderboard")
            print("\t|\t___________")
            emtp()
            if results: 
                print("\t|\t____________________________________________________________________")
                print("\t|\t| POSITION |      USERNAME      |   LEVEL   |  SCORE  |  RESETTED  |")
                print("\t|\t|__________|____________________|___________|_________|____________|")
                
                for j, row in enumerate(results[:10], start=1):
                    position = f"|{str(j) + (' ' * (10 - len(str(j))))}"
                    username = f"|{row[0] + (' ' * (20 - len(str(row[0]))))}"
                    level = f"|{str(row[1]) + (' ' * (11 - len(str(row[1]))))}"
                    score = f"|{str(row[2]) + (' ' * (9 - len(str(row[2]))))}"
                    resetted = f"|{str(row[3]) + (' ' * (12 - len(str(row[3]))))}|"
                    print(f"\t|\t{position}{username}{level}{score}{resetted}")
                
                print("\t|\t|__________|____________________|___________|_________|____________|")
            else:
                print(f"\t|\t{Fore.RED}No data found.{Style.RESET_ALL}")  

            emtp()
            chle = input(f"\t|\t{Fore.YELLOW}Click Enter to go back:{Style.RESET_ALL}")
            mainmenu()
        elif ch == "5":
            chsure = input(f"\t|\t{Fore.YELLOW}Type 'reset' if you want to Reset or click enter to go back: {Style.RESET_ALL}")
            if chsure.lower() == "reset":
                cur.execute(f"update user_progress set score = 0, resetted_score = resetted_score + 1, level = 1 where username = '{curuser}';")
                db.commit()
                updatescore()
                emtp()
                print(f"\t|\t{Fore.GREEN}Resetted Your Score and Level...{Style.RESET_ALL}")
                emtp()
                chle = input(f"\t|\t{Fore.YELLOW}Click Enter to go back:{Style.RESET_ALL}")
                mainmenu()
            else:
                mainmenu()

        elif ch == "6":
            emtp()
            print(f"\t|\t{Fore.RED}Terminated the program.{Style.RESET_ALL}")
            print("_______________________________________________________________________________")
            sys.exit()
def register():
    global curuser, curlevel, curscore, curreset
    print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\t|\tSign Up!")
    print("\t|\t________")
    emtp()
    
    usern, passwd = checkinfo(2)
    cur.execute("select * from user_details;")
    data = cur.fetchall()
    
    userexist = False
    
    for i in data:
        if i[0] == usern:
            emtp()
            print(f"\t|\t{Fore.RED}This username already exists...{Style.RESET_ALL}")
            emtp()
            print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            emtp()
            starti() 
            userexist = True
            break
    
    if not userexist:
        cur.execute("insert into user_details values('{}', '{}');".format(usern, passwd))
        db.commit()
        cur.execute("insert into user_progress values('{}', {}, {}, {});".format(usern, 1, 0, 0))
        db.commit()
        emtp() 
        print(f"\t|\t{Fore.GREEN}Signed Up!{Style.RESET_ALL}")
        emtp()
        curuser = usern
        cur.execute(f"select * from user_progress where username = '{curuser}';")
        datate = cur.fetchone()
        curlevel = int(datate[1])
        curscore = int(datate[2])
        curreset = int(datate[3])
        
        mainmenu()

def hangman_game(lvl):
    if lvl > 10:
        print(f"\t|\t{Fore.GREEN}You have completed the Game {Style.RESET_ALL}{Fore.MAGENTA}C:{Style.RESET_ALL}")
        emtp()
        print(f"\t|\tCreate a new account or reset to beat your own highest score!")
        emtp()
        chstop = input(f"\t|\t{Fore.YELLOW}Click Enter to go back to the main menu: {Style.RESET_ALL}")
        mainmenu()

    global curuser, curlevel, curscore, curreset
    
    hangman1 = list(" T----|  ")
    hangman2 = list(" |       ")
    hangman3 = list(" |       ")
    hangman4 = list(" |       ")
    hangman5 = list(" |       ")
    hangman6 = list("_|_      ")
    
    randw = randwgen().upper()
    tleveldict = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5}
    tlvl = tleveldict[lvl]
    while True:
        if len(randw) != tlvl + 3:
            randw = randwgen().upper()
        else:
            break

    print(f"\t|\tLevel: {Fore.MAGENTA}{curlevel}{Style.RESET_ALL}")
    emtp()

    randlist = list(randw)
    randwlen = len(randw)
    randwenum = enumerate(randlist)
    randwenumlist = list(randwenum)
    guess_list = []
    ctext = []
    gameOver = False
    correctGs = 0
    wrongGs = 0
    hstate = 0

    def displayhangman():
        h1 = "".join(hangman1)
        h2 = "".join(hangman2)
        h3 = "".join(hangman3)
        h4 = "".join(hangman4)
        h5 = "".join(hangman5)
        h6 = "".join(hangman6)
        
        print("\t|\t" + h1)
        print("\t|\t" + h2)
        print("\t|\t" + h3)
        print("\t|\t" + h4)
        print("\t|\t" + h5)
        print("\t|\t" + h6)
        emtp()
    displayhangman()
    for ct in range(len(randw)):
        ctext.append("-")

    def printin():
        ctextstr = "".join(ctext)
        print("\t|\tThe word is", ctextstr)
        emtp()

    def changeman(h):
        nonlocal hstate
        
        if h == 0:
            hangman2[-3] = "0"
            hstate += 1
        elif h == 1:
            hangman3[-3] = "|"
            hstate += 1
        elif h == 2:
            hangman3[-4] = "/"
            hstate += 1
        elif h == 3:
            hangman3[-2] = "\\"
            hstate += 1
        elif h == 4:
            hangman4[-3] = "|"
            hstate += 1
        elif h == 5:
            hangman5[-4] = "/"
            hstate += 1
        elif h == 6:
            hangman5[-2] = "\\"
            hstate += 1
    printin()

    while not gameOver:
        print("\t|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        inp = input(f"\t|\t{Fore.YELLOW}Enter a guess or type \"stop\" to abandon the game: {Style.RESET_ALL}").upper()
        emtp()

        if inp.lower() == "stop":
            gameOver = True
            print(f"\t|\t{Fore.RED}Stopped the game...{Style.RESET_ALL}")
            emtp()
            chstop = input(f"\t|\t{Fore.YELLOW}Click Enter to go back to the main menu: {Style.RESET_ALL}")
            mainmenu()
        
        elif not inp.isalpha():
            print(f"\t|\t{Fore.RED}Enter a valid alphabet for guess...{Style.RESET_ALL}")
            emtp()
        
        elif inp in guess_list:
            print(f"\t|\t{Fore.RED}You have already guessed that...{Style.RESET_ALL}")
            emtp()
        elif len(inp) > 1:
            print(f"\t|\t{Fore.RED}Guess one letter of the word...{Style.RESET_ALL}")
            emtp()
            
        elif inp not in randw:
            print(f"\t|\t{Fore.RED}Wrong...Try again{Style.RESET_ALL}")
            emtp()
            wrongGs += 1
            guess_list.append(inp)
            changeman(hstate)
            displayhangman()
            
            if hstate == 7:
                gameOver = True
                print(f"\t|\t{Fore.RED}Game Over...{Style.RESET_ALL}\n\t|\t\n\t|\tCorrect Guesses: {correctGs}\n\t|\tWrong Guesses: {wrongGs}\n\t|\t\n\t|\tThe word was \"{randw}\".")
                chs = input(f"\t|\t{Fore.YELLOW}Click Enter to go to main menu or type 'retry' to retry: {Style.RESET_ALL}").lower()
                if chs.lower() == "retry":  
                    hangman_game(tlvl)
                else:
                    mainmenu()
        else:
            for t in randwenumlist:
                ctextstr = "".join(ctext)
                if t[1] == inp:
                    correctGs += 1
                    ind = t[0]
                    ctext.pop(ind)
                    ctext.insert(ind, inp)
                    guess_list.append(inp)
            print(f"\t|\t{Fore.GREEN}Correct!{Style.RESET_ALL}")
            emtp()
            displayhangman()

        if ctext == list(randw):
            gameOver = True
            print(f"\t|\t{Fore.GREEN}You WIN!{Style.RESET_ALL}\n\t|\tWrong Guesses: {wrongGs} \n\t|\t\n\t|\tThe word was \"{randw}\"")
            scoreadd = 100 - wrongGs * 5
            print(f"\t|\t{Fore.GREEN}Score: +{scoreadd}{Style.RESET_ALL}")
            cur.execute(f"update user_progress set level = level + 1, score = score + {scoreadd} where username = '{curuser}';")
            db.commit()
            updatescore()
            emtp()
            
            chw = input(f"\t|\t{Fore.YELLOW}Click Enter to go back to main menu: {Style.RESET_ALL}")
            mainmenu()
        
        ctextstr = "".join(ctext)
        print("\t|\t" + ctextstr)
        emtp()
        
sintro()
createdatab()
createtabs()
starti()
