import sys, re

class binaryCyphers:

    def binaryVigenere(self, key, text):

        keyArray = []
        textArray = []
        outArray = []
        keyPlace = 0
        out = ''

        for ch in key:
            keyArray.append(int(ch))

        for ch in text:
            if ch == ' ':
                textArray.append(ch)
            else:
                textArray.append(int(ch))
                #print("int ch = %d"%int(ch))

        lenKey = len(keyArray)
        #print("lenKey = %d"%lenKey)

        for i in range(0, len(textArray)):
            if textArray[i] == ' ':
                #print("Space")
                #outArray.append(textArray[i])
                continue
            else:
                #print("textArray = %d keyArray = %d"%(textArray[i], keyArray[keyPlace%lenKey]))
                outArray.append((textArray[i] + keyArray[keyPlace%lenKey])%2)
                keyPlace += 1
                #print(outArray)

        for i in range(0, len(outArray)):
            if outArray[i] == ' ':
                out = out + ' '
            else:
                out = out + str(outArray[i])

        return out

    def convertCharBinary(self, text):
        return ' '.join(bin(x)[2:].zfill(8) for x in  text.encode('utf-8'))

    def convertBinaryChar(self, binary):
        binary = re.sub('[^0-1]','', binary)
        return ''.join((chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)))

    def run(self):
        exit(0)

if __name__ == "__main__":
    binaryCyphers().run()