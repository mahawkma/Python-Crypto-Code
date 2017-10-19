from pycipher import SimpleSubstitution as SimpleSub
import random
import re
from cryptoClasses.ngram_score import ngram_score
import cryptoClasses.detectEnglish

ngram = input('Please enter the name of the ngram file to try: ')
fitness = ngram_score(ngram) # load our quadgram statistics
#print(fitness)
file = input('Please enter the name of the encrypted text file to crack: ')
ctext=''

with open(file, 'r') as f:
            text = f.read()
            ctext = ctext + text

ctext = re.sub('[^A-Z]','',ctext.upper())

maxkey = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
maxscore = -99e9
parentscore,parentkey = maxscore,maxkey[:]
print ("Substitution Cipher solver, you may have to wait several iterations")
print ("for the correct result. Press ctrl+c to exit program.")
# keep going until we are killed by the user
i = 0
while 1:
    i = i+1
    random.shuffle(parentkey)
    deciphered = SimpleSub(parentkey).decipher(ctext)
    parentscore = fitness.score(deciphered)
    count = 0
    while count < 1000:
        a = random.randint(0,25)
        b = random.randint(0,25)
        child = parentkey[:]
        # swap two characters in the child
        child[a],child[b] = child[b],child[a]
        deciphered = SimpleSub(child).decipher(ctext)
        score = fitness.score(deciphered)
        # if the child was better, replace the parent with it
        if (score > parentscore):
            parentscore = score
            parentkey = child[:]
            count = 0
        count = count+1
    # keep track of best score seen so far
    if parentscore>maxscore:
        maxscore,maxkey = parentscore,parentkey[:]
        print ('\nbest score so far:',maxscore,'on iteration',i)
        ss = SimpleSub(maxkey)
        print ('    best key: '+''.join(maxkey))
        print ('    plaintext: '+ss.decipher(ctext))
