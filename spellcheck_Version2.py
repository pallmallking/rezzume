from spellchecker import SpellChecker

def check_spelling(text):
    spell = SpellChecker()
    words = text.split()
    misspelled = spell.unknown(words)
    return list(misspelled)