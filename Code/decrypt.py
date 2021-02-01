import base64
from os import path

import encrypt as en
from encrypt import padding

a = [[0 for i in range(4)] for j in range(4)]
arr = [[0 for i in range(4)] for j in range(4)]
temp = [[0 for i in range(4)] for j in range(4)]
temp1 = [[0 for i in range(4)] for j in range(4)]
state2 = [[0 for i in range(4)] for j in range(4)]
state4 = [[0 for i in range(4)] for j in range(4)]
state5 = [[0 for i in range(4)] for j in range(4)]
rKeys = [[0 for i in range(44)] for j in range(4)]

roundKeys = [[0 for i in range(4)] for j in range(4)]


def strToArr(s):
    array = [[0 for i in range(4)] for j in range(4)]
    # sl = " "
    i = 0
    ch = 0
    for i in range(4):
        for j in range(4):
            current = int(ord(s[ch]))

            array[j][i] = current
            ch = ch + 1
    return array


def decryptOtherFile():
    image = input("\n\n\t\t\t\t>> Enter file to be decrypted(with extension):  ")

    if not path.exists(image):
        print("\t\t\t\tFile not found!!!!")
        return

    print("\n\n\n\t\t\t\tDecryption is under process, Please Wait.........")
    with open(image, "rb") as img_file:
        temp = base64.b64encode(img_file.read())
    temp = temp.decode('utf-8')
    # print(temp)
    d = base64.b64decode(temp)
    encrypted = d.decode("UTF-8")

    # encrypted = en.encrypt()
    name = image.split('.')[0]
    ext = image.split('.')[1]

    # encrypted = en.readFromFile(name + '.txt')
    f = open("login.exe", "r")
    userf = f.readline()
    key = padding(f.readline())
    f.close()

    roundKeys = en.strToArr(key)
    setMatrices(roundKeys, 0)
    temp1 = en.strToArr(key)
    for i in range(0, 10):
        arr = en.generateRoundKey(temp1, i, roundKeys)
        current = 4 * i + 4
        setMatrices(arr, current)
        en.arrcpy(arr, temp1)
        en.arrcpy(arr, roundKeys)
    entext = ""
    decrypstring = ""
    for i in range(len(encrypted) // 16 if len(encrypted) % 16 == 0 else len(encrypted) // 16 + 1):
        entext = encrypted[i * 16:(i + 1) * 16]
        entext = en.padding(entext)
        state5 = en.strToArr(entext)
        # print("State5", state5)
        # print("state5", state5)

        state4 = invSetMatrices(40)

        en.AddRoundConstant(state5, state4)

        for i in range(8, -1, -1):
            invRowShift(state5)
            state5 = en.intToHexArr(state5)

            state5 = inv_Substitute(state5)
            state5 = en.hexToInt(state5)

            state4 = invSetMatrices((4 * i) + 4)

            en.AddRoundConstant(state5, state4)
            state5 = invMixCol(state5, invconstantCol)

        state5 = invRowShift(state5)
        state5 = en.intToHexArr(state5)
        state5 = inv_Substitute(state5)
        state5 = en.hexToInt(state5)
        state4 = invSetMatrices(0)
        state5 = en.AddRoundConstant(state5, state4)

        decrypstring += en.arrToStr(state5)

    imgdata = base64.b64decode(decrypstring)
    with open(name.replace(name[-4:], "_dec") + '.' + ext, 'wb') as f:
        f.write(imgdata)

    print("\n\n\t\t\t\tFile Decryption successful")


def decryptText():
    filename = input("\n\n\t\t\t\t>> select file which you want to decrypt from the folder(): ")
    fname = filename.split('.')[0]
    ext = '.exe'

    dFile = fname + ext

    if not path.exists(dFile):
        print("\n\t\t\t\t_._._.File not found!!!!._._._")
        return
    encryptstring = en.readFromFile(dFile)
    f = open("login.exe", "r")
    userf = f.readline()
    passf = f.readline()
    f.close()
    key = padding(passf)

    entext = ""
    decrypstring = ""
    for i in range(len(encryptstring) // 16 if len(encryptstring) % 16 == 0 else len(encryptstring) // 16 + 1):
        entext = encryptstring[i * 16:(i + 1) * 16]
        entext = padding(entext)
        state5 = strToArr(entext)
        # print("State5", state5)
        # print("state5", state5)

        roundKeys = en.strToArr(key)

        setMatrices(roundKeys, 0)
        temp1 = en.strToArr(key)
        for i in range(0, 10):
            arr = en.generateRoundKey(temp1, i, roundKeys)
            current = 4 * i + 4
            setMatrices(arr, current)
            en.arrcpy(arr, temp1)
            en.arrcpy(arr, roundKeys)

        state4 = invSetMatrices(40)

        en.AddRoundConstant(state5, state4)

        for i in range(8, -1, -1):
            invRowShift(state5)
            state5 = en.intToHexArr(state5)

            state5 = inv_Substitute(state5)
            state5 = en.hexToInt(state5)

            state4 = invSetMatrices((4 * i) + 4)

            en.AddRoundConstant(state5, state4)
            state5 = invMixCol(state5, invconstantCol)

        state5 = invRowShift(state5)
        state5 = en.intToHexArr(state5)
        state5 = inv_Substitute(state5)
        state5 = en.hexToInt(state5)
        state4 = invSetMatrices(0)
        state5 = en.AddRoundConstant(state5, state4)
        # print("stat5", state5)
        decrypstring += en.arrToStr(state5)

    print("\n\t\t\t\t   Decrypted Message:  ", decrypstring)


inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


def invSetMatrices(start):
    array = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            array[i][j] = rKeys[i][start + j]
    return array


def invRowShift(a):
    m = 1
    for i in range(1, 4):
        for l in range(m):
            if m > 0:
                temp = a[i][3]
                for k in range(3, 0, -1):
                    a[i][k] = a[i][k - 1]
                a[i][0] = temp
        m = m + 1
    return a


def inv_Substitute(a):
    for i in range(4):
        for j in range(4):
            a[i][j] = hex(inv_s_box[int(a[i][j], 16)])[2:]
    return a


def galoisMult(a, b):
    msb = 0
    p = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        b >>= 1
        # print("b af", bin(b))
        msb = a & 128
        a <<= 1
        if msb == 128:
            a ^= 27
    return p % 256


def invMixCol(arr, const):
    invMixCol = [[0 for i in range(4)] for j in range(4)]
    for k in range(4):
        for i in range(4):
            for j in range(4):
                invMixCol[k][i] ^= (galoisMult(arr[j][i], const[k][j]))
    return invMixCol


invcArry = ['0x0E', '0x0B', '0x0D', '0x09',
            '0x09', '0x0E', '0x0B', '0x0D',
            '0x0D', '0x09', '0x0E', '0x0B',
            '0x0B', '0x0D', '0x09', '0x0E']

invconstantCol = [[0 for i in range(4)] for j in range(4)]

for i in range(4):
    for j in range(4):
        invconstantCol[i][j] = int(invcArry[i + j + 3 * i], 16)


def setMatrices(arrr, start):
    for i in range(4):
        for j in range(4):
            rKeys[i][start + j] = arrr[i][j]
    return rKeys
