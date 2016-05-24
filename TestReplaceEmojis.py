import ReplaceEmojis
import unittest

class TestCountEmoticons(unittest.TestCase):
    def testReplaceEmojisNoEmojis(self):
            #This should leave the string unchanged
            s = 'This sentence has no emojis in it.';
            self.assertEqual(ReplaceEmojis.replaceEmojis(s), 'This sentence has no emojis in it.');
            
    def testReplaceEmojisNoneOrNotStr(self):
        self.assertRaises(TypeError,ReplaceEmojis.replaceEmojis,None);
        self.assertRaises(TypeError,ReplaceEmojis.replaceEmojis,['a','list']);
        self.assertRaises(TypeError,ReplaceEmojis.replaceEmojis,8);
            
    def testReplaceEmojisRanges(self):
        s = 'This sentence has \U0001F60C two emojis from the first range\U0001F64A.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the first range<emoji>.')
            
        s = 'This sentence has \U00002712 two emojis from the second range\U00002795.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the second range<emoji>.')
            
        s = 'This sentence has \U0001F691 two emojis from the third range\U0001F6A8.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the third range<emoji>.')
            
        s = 'This sentence has \U0001F192 two emojis from the fourth range\U0001F238.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the fourth range<emoji>.')
            
        s = 'This sentence has \U0001F611 two emojis from the fifth range\U0001F62F.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the fifth range<emoji>.')
            
        s = 'This sentence has \U0001F694 two emojis from the sixth range\U0001F6C1.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the sixth range<emoji>.')
            
        s = 'This sentence has \U0001F317 two emojis from the seventh range\U0001F4EF.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> two emojis from the seventh range<emoji>.')
            
        s = 'This sentence has \U0001F415 emojis from multiple ranges\U0001F6A3. The function \U0001F53D should still work\U0001F684.'
        self.assertEqual(ReplaceEmojis.replaceEmojis(s),'This sentence has <emoji> emojis from multiple ranges<emoji>. The function <emoji> should still work<emoji>.')
		
if __name__ == '__main__':
    unittest.main()
