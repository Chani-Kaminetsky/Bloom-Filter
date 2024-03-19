from BitHash import BitHash 
from BitVector import BitVector 

class BloomFilter(object):
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        # n = numKeys
        # d = numHashes
        # Need to return N, which is the estimated number of bits needed
        # P = maxFalsePositive
        
        # Equation B: phi = (1 - P ^^ (1/d))
        # Equation D: N = d / (1 - phi ^^ (1/n))
        
        phi = (1 - maxFalsePositive ** (1/numHashes))
        N = numHashes / (1 - phi ** (1/numKeys))
        
        return int(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        self.__bitVector = BitVector(size = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive))
        self.__bitsSet = 0
        self.__numHashes = numHashes
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        for i in range(self.__numHashes):
            
            #Hash it and find it's location
            hashIndex = BitHash(key, i+1)
            location = hashIndex % len(self.__bitVector)            
            
            #Check if it is full already
            if self.__bitVector[location] == 0:
                #increment the bits set
                self.__bitsSet += 1
                self.__bitVector[location] = 1
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        for i in range(self.__numHashes):
            
            #Hash it and find it's location
            hashIndex = BitHash(key, i+1)
            location = hashIndex % len(self.__bitVector)            
            
            #If it is 0, then it for sure is not there
            if self.__bitVector[location] == 0:
                return False     
        
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        # n = numKeys
        # d = numHashes
        # P = maxFalsePositive
        
        
        #Amount of zeros divided by the total numbers of bits
        phi = (len(self.__bitVector) - self.__bitsSet) / len(self.__bitVector)    
        
        #Equation A
        P = (1 - phi) ** self.__numHashes    
        
        return P 
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__bitsSet


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    file = open("wordlist.txt", "r")
    for i in range (numKeys):
        line = file.readline()
        b.insert(line)
        
    file.close()
        
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    projectedFalsePos = b.falsePositiveRate() * 100
    print("The projected false positive rate should theoretically be", projectedFalsePos)

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    missing = 0
    
    file = open("wordlist.txt", "r")
    for i in range (numKeys):
        line = file.readline()
        if not b.find(line):
            missing += 1
            
    print("There are", missing, "false finds in the bloom filter.")
        
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    falseFinds = 0
    
    for i in range (numKeys):
        line = file.readline()
        if b.find(line):
            falseFinds += 1
    
    percentageOfFalsePos = (falseFinds/numKeys) * 100
        
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print("Percentage rate of false positives is", percentageOfFalsePos)
    

    
if __name__ == '__main__':
    __main()       

