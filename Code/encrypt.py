import base64
import os

a = [[0 for i in range(4)] for j in range(4)]
arr = [[0 for i in range(4)] for j in range(4)]
temp = [[0 for i in range(4)] for j in range(4)]
temp1 = [[0 for i in range(4)] for j in range(4)]
state2 = [[0 for i in range(4)] for j in range(4)]
rKeys = [[0 for i in range(44)] for j in range(4)]

roundKeys = [[0 for i in range(4)] for j in range(4)]



def encryptOtherFile():
    from os import path
    f = open("login.exe", "r")
    userf = f.readline()
    key = padding(f.readline())
    f.close()
    IFile = input("\n\n\t\t\t\t>> Enter your File name with extension: ")

    if not path.exists(IFile):
        print("\n\t\t\t\t_._._.File not found!!!!._._._")
        return

    print("\n\n\n\t\t\t\tencryption is under process, Please Wait.........")
    name = IFile.split(".")[0]
    extension = IFile.split(".")[1]
    encryptstring = ""

    with open(IFile, "rb") as img_file:
        temptext = base64.b64encode(img_file.read())
    temptext = temptext.decode('utf-8')




    for i in range(len(temptext) // 16 if len(temptext) % 16 == 0 else len(temptext) // 16 + 1):
        text = temptext[i * 16:(i + 1) * 16]
        text = padding(text)
        plainText = strToArr(text)

        roundKeys = strToArr(key)
        setMatrices(roundKeys, 0)

        temp1 = strToArr(key)

        state2 = AddRoundConstant(plainText, roundKeys)



        for i in range(0, 10):

            state2 = intToHexArr(state2)

            state2 = sboxSub(state2)

            state2 = rowShift(state2)

            if i != 9:
                state2 = mixCol(state2)

            state2 = hexToInt(state2)

            arr = generateRoundKey(temp1, i, roundKeys)
            current = 4 * i + 4
            setMatrices(arr, current)
            state2 = AddRoundConstant(state2, arr)
            arrcpy(arr, temp1)
            arrcpy(arr, roundKeys)

        encryptstring += arrToStr(state2)

    b = encryptstring.encode("UTF-8")

    encryptimgstring = base64.b64encode(b)

    imgdata = base64.b64decode(encryptimgstring)
    with open(name + "_enc." + extension, 'wb') as f:
        f.write(imgdata)

    print("\n\n\t\t\t\tFile Encryption successful")



def encryptText():
    f = open("login.exe", "r")
    userf = f.readline()
    tempKey = f.readline()
    f.close()
    key = padding(tempKey)



    temptext = input("\n\n\t\t\t\t>> Enter Message: ")
    encyptMessage = ""
    for i in range(len(temptext) // 16 if len(temptext) % 16 == 0 else len(temptext) // 16 + 1):
        text = temptext[i * 16:(i + 1) * 16]
        text = padding(text)


        plainText = strToArr(text)

        roundKeys = strToArr(key)
        setMatrices(roundKeys, 0)
        temp1 = strToArr(key)

        state2 = AddRoundConstant(plainText, roundKeys)


        for i in range(0, 10):

            state2 = intToHexArr(state2)

            state2 = sboxSub(state2)

            state2 = rowShift(state2)

            if i != 9:
                state2 = mixCol(state2)

            state2 = hexToInt(state2)

            arr = generateRoundKey(temp1, i, roundKeys)
            current = 4 * i + 4
            setMatrices(arr, current)
            state2 = AddRoundConstant(state2, arr)

            arrcpy(arr, temp1)
            arrcpy(arr, roundKeys)
        encyptMessage += arrToStr(state2)

    print("\n\n\t\t\t\tencrypted Message",encyptMessage)
    filename = input("\n\n\t\t\t\t>> Please Enter file name where you want to print encrypted string: ")
    writeInfile(encyptMessage, filename)
    print("\n\n\t\t\t\tText Encryption successful")



s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)



def padding(string):
    if len(string) < 16:
        string = string.ljust(16)
    return string

def writeInfile(st,filepath):

    name = filepath.split('.')[0]
    b22 = st.encode("UTF-8")
    e = base64.b64encode(b22)
    s1 = e.decode("UTF-8")
    f = open(name + '.exe', "w")
    f.write(s1)
    f.close()



def readFromFile(Fname):
    f = open(Fname, "r")
    b1 = f.readlines()
    f.close()
    j1 = ""
    j1 = j1.join(b1)
    b1 = j1.encode("UTF-8")
    d = base64.b64decode(b1)
    s2 = d.decode("UTF-8")

    return s2

def strToArr(s):
    array = [[0 for i in range(4)] for j in range(4)]
    i = 0
    ch = 0
    for i in range(4):
        for j in range(4):
            current = int(ord(s[ch]))

            array[j][i] = current
            ch = ch + 1
    return array

def setMatrices(arrr, start):
    for i in range(4):
        for j in range(4):
            rKeys[i][start + j] = arrr[i][j]
    return rKeys

def AddRoundConstant(arr1, arr2):
    for i in range(4):
        for j in range(4):
            arr1[i][j] ^= arr2[i][j]
    return arr1

def intToHexArr(arrr):
    hexarrr = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            hexarrr[j][i] = hex((arrr[j][i]))[2:]
    return hexarrr


def sboxSub(a):
    for i in range(4):
        for j in range(4):
            a[i][j] = hex(s_box[int(a[i][j], 16)])[2:]
    return a

def rowShift(a):
    m = 1
    for i in range(1, 4):
        for l in range(m):
            if m > 0:
                temp = a[i][0]
                for k in range(3):
                    a[i][k] = a[i][k + 1]
                a[i][3] = temp
        m = m + 1
    return a



cArry = ['0x02', '0x03', '0x01', '0x01',
         '0x01', '0x02', '0x03', '0x01',
         '0x01', '0x01', '0x02', '0x03',
         '0x03', '0x01', '0x01', '0x02']
constantCol = [[0 for i in range(4)] for j in range(4)]



for i in range(4):
    for j in range(4):
        constantCol[i][j] = hex(int(cArry[i + j + 3 * i], 16))[2:]

mixCol = [[0 for i in range(4)] for j in range(4)]
modEight = 27
xorcomp = [0, 0, 0, 0]

def mixCol(arr):
    mixcolumn = [[0 for i in range(4)] for j in range(4)]
    xorlist = [0, 0, 0, 0]
    finalxorlist = [0, 0, 0, 0]
    for k in range(4):
        for i in range(4):
            for j in range(4):
                if constantCol[k][j] == '1':
                    xorlist[j] = int(arr[j][i], 16)
                elif constantCol[k][j] == '2':
                    Ba = bitVector(arr, j, i)
                    if Ba[0] != 1:
                        xorlist[j] = leftShift(arr, j, i)
                    if Ba[0] == 1:
                        ls2 = leftShift(arr, j, i)
                        xorlist[j] = (ls2 ^ modEight) - 256

                elif constantCol[k][j] == '3':
                    Ba = bitVector(arr, j, i)
                    if Ba[0] != 1:
                        xorVar = leftShift(arr, j, i)
                    if Ba[0] == 1:
                        ls3 = leftShift(arr, j, i)
                        xorVar = (ls3 ^ modEight) - 256
                    xorlist[j] = xorVar ^ int(arr[j][i], 16)
            finalxorlist[i] = (xorlist[0] ^ xorlist[1] ^ xorlist[2] ^ xorlist[3])
            mixcolumn[k][i] = hex(finalxorlist[i])[2:]
    return mixcolumn

def hexToInt(arr):
    intarr = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            intarr[i][j] = int(arr[i][j], 16)
    return intarr

def leftShift(a, i, j):
    c = int(a[i][j], 16)
    leftShifthex = c << 1
    return leftShifthex


def bitVector(arr, i, j):
    binary = list(("{0:08b}".format(int(arr[i][j], 16))))
    for i in range(len(binary)):
        binary[i] = int(binary[i])
    return binary

def SingleShift(s):
    s[3][3], s[0][3], s[1][3], s[2][3] = s[0][3], s[1][3], s[2][3], s[3][3]


def SingleSubstitute(arrr):
    for i in range(4):
        arrr[i][3] = s_box[arrr[i][3]]


def opForKeys(galoistemp, arr, roundKeys):
    for i in range(4):
        arr[i][0] = roundKeys[i][0] ^ galoistemp[i][3]
    for i in range(1, 3):
        for j in range(4):
            arr[j][i] = arr[j][i - 1] ^ roundKeys[j][i]
    for i in range(4):
        arr[i][3] = roundKeys[i][3] ^ arr[i][2]


    return arr


def generateRoundKey(galoistemp, const, roundKeys):
    arrays = [[0 for i in range(4)] for j in range(4)]
    SingleShift(galoistemp)

    SingleSubstitute(galoistemp)

    if const == 8:
        galoistemp[0][3] = galoistemp[0][3] ^ 27
    elif const == 9:
        galoistemp[0][3] = galoistemp[0][3] ^ 54
    else:
        galoistemp[0][3] = galoistemp[0][3] ^ (2 ** const)

    arrays = opForKeys(galoistemp, arrays, roundKeys)
    return arrays

def arrcpy(arr1, arr2):
    for i in range(4):
        for j in range(4):
            arr2[i][j] = arr1[i][j]
    return arr2

def arrToStr(array1):
    encryptStr = ""
    for i in range(4):
        for j in range(4):
            charc = chr(array1[j][i])
            encryptStr += charc
    return encryptStr
