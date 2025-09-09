
import re
from collections import Counter

doc = """
Wow! The printer (model: HP-LaserJet_5000) isn't working—again. 
I've tried everything: unplugging it, restarting the computer, 
even yelling "FIX IT!" 😤. Still, no luck. The error message reads: 
“Device not found @ COM1: retry?”. Meanwhile, the IT guy (Ronald, I think?) 
said: “Try reinstalling the driver—maybe it’s corrupted.” Honestly, I’m not sure 
what’s going on... Could it be the cable (the thick one, not the twisty one)? 
Or maybe the port’s fried? Either way, it’s a mess. #printerproblems #techfail
"""

def clean_text(text):
    # Remove punctuation and special characters, keep letters and digits
    return re.sub(r'[^\w\s]', '', text).lower()

def get_word_frequencies(text):
    words = text.split()
    return Counter(words)

cleaned = clean_text(doc)
word_freq = get_word_frequencies(cleaned)

print(word_freq)
