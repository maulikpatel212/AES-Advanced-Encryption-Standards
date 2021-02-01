import sys
from os import system
import decrypt as dec
import encrypt as enc
import login as lg

if len(sys.argv) == 2:

    while sys.argv[1] == "encrypt":
        system('cls')
        lg.login()
        system('cls')

        print(

            "\n\t\t\t\t1. Encrypt text\n"
            "\n\t\t\t\t2. Encrypt File\n"
            "\n\t\t\t\t3. Exit"
        )

        choice = int(input("\n\n\n\t\t\t\tEnter your choice: "))
        system('cls')
        if choice == 1:
            enc.encryptText()
            break
        elif choice == 2:
            # for any file format (e.g. .jpg,.jpeg, video files, docs file, text file, ppt etc)
            enc.encryptOtherFile()
            break

        elif choice == 3:
            break
        else:
            print("\t\t\t\tInvalid choice")

    while sys.argv[1] == "decrypt":
        system('cls')
        s = lg.login()
        system('cls')

        print(
            "\n\t\t\t\t1. Decrypt text\n"
            "\n\t\t\t\t2. Decrypt File\n"
            "\n\t\t\t\t3. Exit"
        )
        choice = int(input("\n\n\n\t\t\t\tEnter your choice: "))

        if choice == 1:
            dec.decryptText()
            break
        elif choice == 2:
            # for any file format (e.g. .jpg,.jpeg, video files, docs file, text file, ppt etc)
            dec.decryptOtherFile()
            break
        elif choice == 3:
            break
        else:
            print("\t\t\t\tInvalid choice")


else:
    print("",
          "==================================================================",
          ">> Enter command line arguments as encrypt/decrypt",
          "",
          ">> Examples:",
          "",
          ">> To Encrypt ==> python main.py encrypt",
          "",
          ">> To Decrypt ==> python main.py decrypt",
          "",

          "==================================================================",
          "",
          sep="\n")
