import sys

class Text(object):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return '%s' % self.filename

    def text_to_bytes(self):

        byteList = []

        f = open(self.filename, 'r')
        s = f.read()
        f.close()

        for byte in s:
            byteList.append(ord(byte))

        return byteList

    def hex_to_bytes(self):

        byteList = []
        f = open(self.filename, 'r')

        hexStr = f.read()
        for i in range(0, len(hexStr), 2):
            byte = hexStr[i:i + 2]
            if '\n' in byte:
                continue
            byteList.append(int(byte, 16))

        f.close()
        return byteList

    def bytes_to_text(self, ByteList):

        s = ''
        for byte in ByteList:
            s += chr(byte)

        f = open(self.filename, 'w')

        f.write(s)

        f.close()

    def bytes_to_hex(self, ByteList):

        f = open(self.filename, 'w')

        for byte in ByteList:
            hexStr = '0' + hex(byte)[2:]
            f.write(hexStr[-2:].upper())

        f.close()

    def encrypt(self, Key):

        PlainBytes = self.text_to_bytes()
        KeyBytes = Key.text_to_bytes()
        KeystreamBytes, CipherBytes = crypt(PlainBytes, KeyBytes)
        Keystream = Text('keystream.txt')
        Cipher = Text(self.filename)
        Keystream.bytes_to_hex(KeystreamBytes)
        Cipher.bytes_to_hex(CipherBytes)

    def decrypt(self, Key):

        CipherBytes = self.hex_to_bytes()
        KeyBytes = Key.text_to_bytes()
        KeystreamBytes, PlainBytes = crypt(CipherBytes, KeyBytes)
        Plain = Text(self.filename)
        Keystream = Text('keystream.txt')
        Keystream.bytes_to_hex(KeystreamBytes)
        Plain.bytes_to_text(PlainBytes)


def crypt(PlainBytes, KeyBytes):
    keystreamList = []
    cipherList = []

    keyLen = len(KeyBytes)
    plainLen = len(PlainBytes)
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + KeyBytes[i % keyLen]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    for m in range(plainLen):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        keystreamList.append(k)
        cipherList.append(k ^ PlainBytes[m])

    return keystreamList, cipherList


def main(name, Filename, Action, KeyName='key.txt', *args):
    try:
        f = open(Filename, 'r')
        f.close()
        f = open(KeyName, 'r')
        f.close()
    except IOError:
        print('File(s) do not exist.\nUsage: RC4.py filename encrypt/decrypt [keyfile]')
    else:
        if Action == 'encrypt':
            Plain = Text(Filename)
            Key = Text(KeyName)
            Plain.encrypt(Key)
        elif Action == 'decrypt':
            Cipher = Text(Filename)
            Key = Text(KeyName)
            Cipher.decrypt(Key)
        else:
            print('Usage: RC4.py filename encrypt/decrypt [keyfile]')


if __name__ == '__main__':
    if len (sys.argv) < 4:
        print ('Usage: RC4.py filename encrypt/decrypt [keyfile]')
        sys.exit (1)
    else:
        main(*sys.argv)
