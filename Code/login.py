import os
import stdiomask
from time import sleep
import ctypes


def signIn():
    print("\n\n\n\t\t\t\t=========== Login ===========")
    tempcuser = input("\t\t\t\tEnter Username: ")

    cpass = stdiomask.getpass(prompt="\t\t\t\tenter password: ", mask="*")

    cuser = tempcuser + '\n'

    f = open("login.exe", "r")
    userf = f.readline()
    passf = f.readline()

    f.close()
    if cuser == userf and cpass == passf:
        return "\n\t\t\t\tLogin successfully"
    else:
        ctypes.windll.user32.MessageBoxW(0, "Username or password Incorrect!!!", "Warning!", 16)
        """
        print("\n\t\t\t\tUsername or Password Incorrect!!")
        sleep(1)
        """
        os.system('cls')
        signIn()

def creatAcc():
    print("\n\n\n\t\t\t\t======== Add Account ==========")
    addusername = input("\t\t\t\tEnter your Username: ")
    adduserpass = stdiomask.getpass(prompt="\t\t\t\tenter password: ", mask="*")
    addcuserpass = stdiomask.getpass(prompt="\t\t\t\tconfirm password: ", mask="*")

    if adduserpass == addcuserpass:
        f = open("login.exe", "w")
        f.write(addusername)
        f.write('\n')
        f.write(adduserpass)
        f.close()

        print("\n\t\t\t\tAccount created successfully: ")
    else:
        print("\n\t\t\t\tPassword doesn't match")
        creatAcc()


# =======================  main ======================= #
def login():
    from os import path

    if not path.exists("login.exe"):
        f = open("login.exe", "w")
        f.close()
        creatAcc()


    else:
        signIn()
