 #!/usr/bin/python
 # -*- coding: iso-8859-1 -*-
from django.utils.encoding import smart_str
import json
import linecache
import math
from nltk.corpus import stopwords
import os
from pattern.en import sentiment
from pattern.en.wordlist import PROFANITY,ACADEMIC
import re
import string

VOCAB_FILE = 'scowl.american.70';
PUNCTUATION = string.punctuation;

def cleanPost(post):
    if type(post) != str:
        raise TypeError('ERROR, either null string or non-string type entered');
    '''This function takes in a text and performs the following actions:
    1. Replace repeated character sequences of length 3+ with sequences of length 2 e.g. goooood should become good.
    2. Replace all sequences of spaces of length 2+ with a single space.
    3. Replace all usernames with 'AT_USER' so usernames don't interfere with linguistic analysis.
    '''
    #First we replace repeated character sequences of length 3+ with sequences of length 2 e.g. goooood should become good.
    threeplusCharacterRepeatPattern = r"(\w)\1{2,}"
    numExtensions = len(re.findall(threeplusCharacterRepeatPattern, post))
    post = re.sub(threeplusCharacterRepeatPattern,r"\1\1",post);
    
    #Then we replace all sequences of spaces of length 2+ with a single space
    twoPlusSpacesPattern = r"( ){2,}"
    post = re.sub(twoPlusSpacesPattern," ",post);    
    
    #Then we replace all usernames with 'AT_USER' so usernames don't interfere with linguistic analysis
    userNamePattern = r"(@([A-Za-z0-9_]+?\b))"
    post = re.sub(userNamePattern,"AT_USER",post);
    
    return post,numExtensions;
    
def createCSVFiles():
    '''This function creates every possible subset of the features extracted and creates an individual CSV file for each subset
    The purpose of this is to determine which subset provides the best classification results'''
    featureSubsets = listPowerset(["Normalisations","Emojis","Exclamations","Stops","Profanity","Academic","NumTokens","Sentiment","AvgWordLength"])
    lengthFeatureSubsets = len(featureSubsets);
    filePath = 'Feature Subsets/Subset'#The folder where the CSV files are being written to
    filesToWrite = [];
    #First write the header for each file
    for i in range(0,len(featureSubsets)):
        fileName = filePath + str(i) + '.csv';
        newFile = open(fileName,'w');
        newFile.write(','.join(featureSubsets[i]) + ',Class\n');
        filesToWrite.append(fileName);
        newFile.close();

    classList = ['personal','professional']
    for classification in classList:
        print(classification.upper())#Used to track progress
        folder = ''#The folder where the tweets are contained. The file 'TestTweetFile.json' gives an example of how the tweets are stored
    
        for file in os.listdir(folder):
            print('Reading %s' % file);#Used to track progress
            for featureVector in extractFeatures(folder+file):#Get the feature vectors for this particular file
                for featureSubsetIndex in range(0,lengthFeatureSubsets):#Split the feature vectors up according to each possible subset and write to a CSV file
                    fileToBeWrittenTo = open(filesToWrite[featureSubsetIndex],'a');
                    for feature in featureSubsets[featureSubsetIndex]:
                        fileToBeWrittenTo.write(str(featureVector[feature])+',')
                    fileToBeWrittenTo.write('%s\n' % classification);
                    fileToBeWrittenTo.close();    
    
def expandHashtag(hashtag):#The reference for this method can be found in the README file
    #This function takes a multiword hashtag and returns a list where each element is a single word from the hashtag. For example #isthisajoke will give back ['is','this','a','joke']
    if type(hashtag) != str:
        raise TypeError('ERROR, either null string or non-string type entered to expandHashtag function')
    
    if len(hashtag) == 1:
        print ("ERROR, can't have a hashtag that only consists of the '#' symbol");
        return None;
        
    if not hashtag.startswith('#'):
        print ("Error, entered string '%s' does not begin with '#' symbol" % hashtag);
        return None;
    
    #Remove the hash symbol    
    hashtag = hashtag[1:]
    original = hashtag;
    
    words_with_start_index = {}
    
    hashtag = list(hashtag);
    
    length = len(hashtag);
    '''This loop performs the following steps:
                          1. Find the largest character subsequence in the hashtag that is a valid english word. Two searches are performed, one from left to right and one from right to left.
                          2. Add the largest such subsequence to the words_with_start_index dictionary with the index of its first character in the string. The longest subsequence may not necessarily be the first word
                          in the hashtag. Thus, these indices are used to determine the order of the words in the hashtag.
                          3. Repeat until all the characters in the hashtag have been accounted for.
                          '''
     
    while hashtag.count(' ') != length:
        largestSub = '';
        for forwardSub in getAllSubstrings(hashtag):
            if ' ' not in forwardSub:
                forwardSub = (''.join(forwardSub));
                if inVocabulary(forwardSub) and len(forwardSub) > len(largestSub):
                    largestSub = forwardSub;
                
        for backwardSub in getAllSubstringsReverse(hashtag):
            if ' ' not in backwardSub:
                backwardSub = (''.join(backwardSub));
                if inVocabulary(backwardSub) and len(backwardSub) > len(largestSub):
                    largestSub = backwardSub;
        
        if largestSub != '':
            for m in re.finditer(largestSub,original):
                startIndex = m.start();
                if hashtag[startIndex] != ' ':#This substring may in fact be part of a larger word. For example 'is' in the hashtag '#isthisajoke'. The word 'is' only appears once. A space appearing in largestSub's
                                              #start position means that largestSub is in fact a part of a larger word that has already been seen.                
                    words_with_start_index[startIndex] = largestSub;
                    for i in range(startIndex,startIndex+len(largestSub)):#Make all of largestSub's letters equal ' ' for the purposes of the previous 'if' statement
                        hashtag[i] = ' ';
        else:
            #There are still characters in the hashtag but we haven't been able to find any subsequence that appears in the lexicon.
            #Return the original hashtag minus the '#' symbol.
            return original;
      
    output = []       
    for _,v in sorted(words_with_start_index.items()):
        output.append(v)
    return ' '.join(output);
    
def extractFeatures(filePath):
    '''
    This script extracts the following features from each tweet
    1. Ratio of unnormalised tokens to the total number of tokens.
    2. Ratio of emojis to the total number of tokens.
    3. Ratio of exclamation points to the total number of tokens.
    4. Ratio of stopwords to the total number of tokens.
    6. Ratio of profane words to the total number of tokens.
    7. Ratio of academic words to the total number of tokens.
    7. Total number of tokens.
    8. Average word length.
    9. Sentiment.
    '''
    
    STOPWORDS = stopwords.words('english');
    tweetList = json.loads((open(filePath)).readline());
    collection = [];
    for tweet in tweetList:
        tweet = smart_str(unescape(tweet['text']));#smart_str handles accented characters so they don't cause an encoding error
        features = {};
        normalisedTuple = normalise(tweet);
        tweet = normalisedTuple[0];
        tweetTokens = tweet.split(' ');
        numTokens = float(len(tweetTokens));
        numExclamations = tweet.count('!');
        numTokens+=numExclamations;
        features['Normalisations'] = normalisedTuple[1] / numTokens;
        features['Emojis'] = (tweet.count('<emoji>')) / numTokens;
        
        academicCount = 0.0;
        profanityCount = 0.0;
        stopCount = 0.0;
        totalWordLength = 0.0;
        wordCount = 0.0;
        firstWordSeen = False;
        for token in tweetTokens:
            if re.search('\w',token) and '<emoji>' not in token:
                token = token.strip(PUNCTUATION).rstrip(PUNCTUATION);
                totalWordLength += len(token)-token.count('!');#Some words will have exclamations within them. We've already counted exclamations as separate tokens so we exclude them in calculations of average word length.
                wordCount += 1;
                        
                if not firstWordSeen and token.istitle():
                    token = token.lower();#Can do this in this function because we're searching the word in specific category lists. It normally wouldn't be advisable since the word could start with a proper noun.
                    firstWordSeen = True;
                    
                if token in ACADEMIC:
                    academicCount += 1;
                if token in PROFANITY:
                    profanityCount += 1;
                if token in STOPWORDS:
                    stopCount += 1;
                    
        features['Exclamations'] = (numExclamations/numTokens);
        features['Stops'] = (stopCount / numTokens);
        features['Profanity'] = profanityCount / numTokens
        features['Academic'] = academicCount / numTokens
        features['NumTokens'] = numTokens;
        features['Sentiment'] = math.fabs(sentiment(tweet)[0])
        features['AvgWordLength'] = totalWordLength / wordCount
        collection.append(features);
    return collection;

def getAllSubstrings(inputString):#From here: http://stackoverflow.com/questions/22469997/how-to-get-all-the-contiguous-substrings-of-a-string-in-python    
    length = len(inputString)
    return [inputString[i:j+1] for i in range(length) for j in range(i,length)]

def getAllSubstringsReverse(inputString):
    length = len(inputString)
    return [inputString[j:i+1] for i in range(length-1,-1,-1) for j in range(i,-1,-1)]
    
def inVocabulary(word):
    #This function checks if a word is in the English language.
    #In the scowl dictionary, first uppercase word is at line 5, last uppercase word is at line 29118
    #In the scowl dictionary, first lowercase word is at line 29119, last lowercase word is at line 165462
    if not os.path.isfile(VOCAB_FILE):
        raise FileNotFoundError("VOCAB_FILE Filepath used in isVocabulary doesn't exist");
        
    if type(word) != str:
        raise TypeError('ERROR. Improper parameter %s passed to isVocabulary function' % str(word));
    
    lower = 29094;
    upper = 165414;
    
    if word[0].isupper():
        lower = 5;
        upper = 29093;
    
    return ( searchFile(word, VOCAB_FILE, lower, upper) != -1);

def listPowerset(lst):#From here: https://gist.github.com/LoveHoly/700c59aba455990328c5
    result = [[]]
    for x in lst:
        # for every additional element in our set
        # the power set consists of the subsets that don't
        # contain this element (just take the previous power set)
        # plus the subsets that do contain the element (use list
        # comprehension to add [x] onto everything in the
        # previous power set)
        result.extend([subset + [x] for subset in result])
    return result
    
def normalise(post):
    if type(post) != str:
        raise TypeError('ERROR, improper parameter passed to normalise function: %s' % post);
    
    #First we clean the post
    cleanPostTuple = cleanPost(post);
    post = cleanPostTuple[0];
    numExtensions = cleanPostTuple[1];
    #Then we replace all hashtags with their expanded versions.
    hashtagPattern = r"(#[A-Za-z0-9_]+?\b)";
    hashes = re.findall(hashtagPattern,post);
            
    for hashtag in hashes:
        post = post.replace(hashtag, expandHashtag(hashtag));
        
    #Now we convert Out of Vocabulary (OOV) words.
    firstWordSeen = False;
    numNormalisations = 0;
    normalisedPost = [];
    for token in post.split(' '):
        normForm = normalisedForm(token) #Some un-normalised expressions have punctuation on the end e.g 'b&' (banned).
        
        if normForm == '':
            cleanedToken = token.lstrip(PUNCTUATION).strip(PUNCTUATION); #Remove punctuation from the beginning and end of the word.
            
            if re.search('\w',cleanedToken) and cleanedToken != 'AT_USER':
                
                inVocab = False
                if not firstWordSeen and cleanedToken.istitle() and not inVocabulary(cleanedToken): #The first letter of the first word in a post may be capitalised.
                    cleanedToken = cleanedToken.lower()
                    
                inVocab = inVocabulary(cleanedToken);
                
                if not inVocab:
                    normForm = normalisedForm(cleanedToken)
                    
                    if normForm != '':
                        if firstWordSeen == False:#We have to title (uppercase the first letter) of the normalised form. Remember that we lowered cleanedToken so that has to be title as well for the replace to work.
                            firstWordSeen = True;
                            cleanedToken = cleanedToken.title()
                            normForm = normForm.title();
                                                        
                        token = token.replace(cleanedToken,normForm);
                        numNormalisations += 1;
        else:
            token = normForm;
            numNormalisations += 1;
        normalisedPost.append(token);            
    return (' '.join(normalisedPost), numNormalisations+numExtensions);

def normalisedForm(word):
    if type(word) != str:
        raise TypeError('ERROR, either null string or non-string type entered');
    
    #This function returns the normalised form of the passed parameter.
    #In the emnlp dictionary, first word beginning with a number is at line 5, last word beginning with a number is at line 857
    #In the emnlp dictionary, first regular word is at line 858, last regular word is at line 41185
    NORM_DICT = 'emnlp_dict_sorted.txt';
    if not os.path.isfile(NORM_DICT):
        raise FileNotFoundError("norm_dict Filepath used in inNormalisationDictionary doesn't exist");
    
    if type(word) != str:
        raise TypeError('ERROR. Improper parameter passed to isNormalisationDictionary function');
        
    lower = 5;
    upper = 857;
    if not re.match('\d',word):
        lower = 858;
        upper = 41185;
        
    normDictIndex = searchFile(word,NORM_DICT,lower,upper);
    
    if normDictIndex != -1:
        return linecache.getline(NORM_DICT,normDictIndex).split('\t')[1].rstrip();
    
    return '';
    
    
def searchFile(word,file,lower,upper):
    while lower <= upper:
        mid = int(math.floor( (lower+upper) / 2));
        mid_word = linecache.getline(file,mid).rstrip();#This function never raises exceptions: https://docs.python.org/3/library/linecache.html
        if '\t' in mid_word:
            mid_word = mid_word.split('\t')[0];
        if mid_word == word:
            return mid;
        elif word < mid_word:
            upper = mid - 1;
        else:
            lower = mid + 1;
    return -1;
 
def unescape(s):#From here: https://wiki.python.org/moin/EscapingHtml
   stringType = type(s).__name__;
   if stringType != 'str' and stringType != 'unicode':
       raise TypeError('ERROR, either null string or non-string type entered');
   s = s.replace("&lt;", "<")
   s = s.replace("&gt;", ">")
   # this has to be last:
   s = s.replace("&amp;", "&")
   return s
