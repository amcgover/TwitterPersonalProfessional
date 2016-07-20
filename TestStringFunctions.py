 #!/usr/bin/python
 # -*- coding: iso-8859-1 -*-

import StringFunctions
import unittest

class TestStringFunctions(unittest.TestCase):
        
    def testCleanPostNoneOrNotStr(self):
        self.assertRaises(TypeError,StringFunctions.cleanPost,None);
        self.assertRaises(TypeError,StringFunctions.cleanPost,['a','list']);
        self.assertRaises(TypeError,StringFunctions.cleanPost,8);
        
    def testCleanPost(self):
        preCleaning = "@userOne This has      multiple spaces ,@userTwo and goooood,     elongation as wellllll @UserThree."
        desiredOutput = ("AT_USER This has multiple spaces ,AT_USER and good, elongation as well AT_USER.",2)
        self.assertEqual(desiredOutput,StringFunctions.cleanPost(preCleaning));  
        
    def testExpandHashtagNoneOrNotStr(self):
        self.assertRaises(TypeError,StringFunctions.expandHashtag,None);
        self.assertRaises(TypeError,StringFunctions.expandHashtag,['a','list']);
        self.assertRaises(TypeError,StringFunctions.expandHashtag,8);
        
    def testExpandHashtagLengthOneOrNoHashSymbol(self):
        self.assertEqual(None,StringFunctions.expandHashtag('#'));
        self.assertEqual(None,StringFunctions.expandHashtag('thesearesomewords'));
        
    def testExpandHashtagReturnsCorrectOutput(self):
        desiredOutput = 'is this a joke';
        self.assertEqual(desiredOutput,StringFunctions.expandHashtag('#isthisajoke'))
        
        desiredOutput = 'living the dream';
        self.assertEqual(desiredOutput,StringFunctions.expandHashtag('#livingthedream'))
        
        desiredOutput = 'sorry not sorry';
        self.assertEqual(desiredOutput,StringFunctions.expandHashtag('#sorrynotsorry'))
        
        desiredOutput = 'ithet'
        self.assertEqual(desiredOutput,StringFunctions.expandHashtag('#ithet'))
        
    def testExpandHashtagChatSpeak(self):
        desiredOutput = 'smh';
        self.assertEqual(desiredOutput,StringFunctions.expandHashtag('#smh'));
    
    def testExtractFeatures(self):
        desiredOutputFirst = {'Normalisations':0.14285714285714285, 'Emojis':0.07142857142857142, 'Exclamations':0.07142857142857142, 'Stops':0.5, 'Profanity':0.0, 
                              'Academic':0.14285714285714285, 'NumTokens':14.0, 'AvgWordLength':3.75, 'Sentiment':0.4375}
        desiredOutputSecond = {'Normalisations':0.0, 'Emojis':0.1111111111111111, 'Exclamations':0.2222222222222222, 'Stops':0.3888888888888889, 'Profanity':0.05555555555555555, 
                              'Academic':0.1111111111111111, 'NumTokens':18.0, 'AvgWordLength':3.75, 'Sentiment':0.5}
        output = StringFunctions.extractFeatures('TestTweetFile.json')
        self.assertEqual(desiredOutputFirst, output[0]);
        self.assertEqual(desiredOutputSecond, output[1]);
    
    def testInVocabularyTrue(self):        
        wordsToSearch = ["A", "ABM's", "ABMs", "ABS", "York's", "Yorkie", "Yorkie's", "a", "bespatters", "bespeak", "bespeaking", "decimator", "decimeter", "decimeter's", "intestine", "intestine's", "intestines", "zygotes", "zygotic", "zymase", "étuis"];
        
        for word in wordsToSearch:
            self.assertEqual(True, StringFunctions.inVocabulary(word),'%s not found' % word);
            
    def testInVocabularyFalse(self):        
        wordsToSearch = ["Dese", "Wurds", "Arn't", "ine", "teh", " dikshunary"]
        
        for word in wordsToSearch:
           self.assertEqual(False, StringFunctions.inVocabulary(word),'%s was found' % word);
        
    def testNormaliseNoneOrNotStr(self):
        self.assertRaises(TypeError,StringFunctions.normalise,None);
        self.assertRaises(TypeError,StringFunctions.normalise,['a','list']);
        self.assertRaises(TypeError,StringFunctions.normalise,8);
        
    def testNormalisePostCorrectOutput(self):
        input = "@userOne This has      multiple spaces ,@userTwo and goooood b&     elongation tooooo don't u tthink @UserThree."
        desiredOutput = ("AT_USER This has multiple spaces ,AT_USER and good banned elongation too don't you think AT_USER.", 5)
        self.assertEqual(StringFunctions.normalise(input), desiredOutput);
        input = "Gud status isn't it?"
        desiredOutput = ("Good status isn't it?", 1)
        self.assertEqual(StringFunctions.normalise(input), desiredOutput);

    def testNormalisedFormNoneOrNotStr(self):
        self.assertRaises(TypeError,StringFunctions.normalise,None);
        self.assertRaises(TypeError,StringFunctions.normalise,['a','list']);
        self.assertRaises(TypeError,StringFunctions.normalise,8);
        
    def testNormalisedFormCorrectOutput(self):
        normForms = {"20minutes":"minutes","20percent":"percent","20points":"points","8weeks":"weeks","8year":"year","8years":"years","actially":"actually","actiin":"acting","actin":"acting", "konference":"conference","konfidential":"confidential", "konfirm":"confirm","part8":"part","part9":"part","partay":"party","zooo":"zoo","zoot":"woohoo", "zout":"out","zpizza":"pizza"}
        for key,value in normForms.items():
            self.assertEqual(value,StringFunctions.normalisedForm(key));
            
    def testUnescapeNoneOrNotStr(self):
       self.assertRaises(TypeError,StringFunctions.unescape,None);
       self.assertRaises(TypeError,StringFunctions.unescape,['a','list']);
       self.assertRaises(TypeError,StringFunctions.unescape,8);
        
if __name__ == '__main__':
    unittest.main()
