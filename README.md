# TwitterPersonalProfessional
This code was written for a research project that aimed to automatically determine whether a tweet referred to a user's personal or professional activities.
Reference for expandHashtag function: http://ceur-ws.org/Vol-1202/paper11.pdf

Vocabulary and normalisation resources were obtained here: https://noisy-text.github.io/norm-shared-task.html#resource

Note: The 'scowl' file used in the StringFunctions.py file differs slightly from the one given at the link. The original contains a letter for each capitalised letter in the English language. The capitalised letters which are not words (e.g. 'K', 'M' etc.) have been removed.

The pattern library isn't available for Python 3 and Python 2.7 couldn't handle the unicode for the emojis. This is why the replaceEmojis function and its unit tests are in separate files.

You're free to use this code however you like, just please leave a comment to say what you're using it for. Also, if you see any way the code could be improved, please leave a comment as well.
