"""xmlchat.py is a Python module for reading CHILDES files
in XML format written by Mark Johnson, 15th March 2005.
You should use this if you need the utterance word targets.
It may also be handy for obtaining morphological forms.

CHILDES data files in XML format are available from:

http://childes.psy.cmu.edu/data-xml/

You will need to download and unzip these before this program
can read them.

The actual XML format is described in an XML Schema document:

http://xml.talkbank.org/talkbank.xsd

The Schema is described in:

http://xml.talkbank.org:8888/talkbank/talkbank.html

This document makes extensive reference to the original CLAN
documentation, available from:

http://childes.psy.cmu.edu/manuals/CHAT.pdf
"""

import re, xml.parsers.expat

# fields to save from a mor entry
_morph_features = ["c","s","stem","mk","mpfx","menx"]

_filename = None
_participants = None        # dictionary of participant information
_utterances = None          # sequence of utterances in file
_utterance = None           # utterance dictionary of current utterance
_words = None               # words of current utterance
_word = None                # current word
_morphs = None              # morphemes of current utterance
_morph = None               # current morpheme

_collect_data = False       # when True, collect char data
_data = None                # variable to collect char data in

_age_re = re.compile(r"P(?P<Year>\d+)Y(?P<Month>\d+)M((?P<Day>\d+)D)?")

# These are my handler functions, which will be called by the
# Expat XML parser.

def _start_element(name, attrs):
    global _collect_data, _data
    global _context, _morph, _morph_features, _morphs
    global _participants, _utterance, _utterances
    global _word, _words
    if name == "w" or (name in _morph_features and _morph != None):
        _collect_data = True
        _data = ""
    elif name == "u":
        _words = []
        attrs["words"] = _words
        _utterance = attrs
        _utterances.append(attrs)
    elif name == "t":
        _utterance["t"] = attrs["type"]
    elif name == "participant":
        _participants[attrs["id"]] = attrs
        agestr = attrs.get("age", None)
        if agestr:
            age_match = _age_re.match(agestr)
            if age_match:
                attrs["months"] = ( 12*int(age_match.group('Year')) + 
                                    int(age_match.group('Month')) )
    elif name == "mor":
        _morphs = []
        _utterance["mor"] = _morphs
    elif name == "mw" and _morphs != None:
        _context = "mw"
        _morph = {}
        _morphs.append(_morph)
        
def _char_data(data):
    global _collect_data, _data
    if _collect_data:
        _data += data.strip()

def _end_element(name):
    global _collect_data, _data, _words, _morph
    global _morphs, _morph_features
    if name == "w":
        _words.append(_data)
        _data = None
        _collect_data = False
    elif name == "mw":
        _morph = None
    elif name == "mor":
        _morphs = None
    elif name in _morph_features and _morph != None:
        _morph[name] = _data
        _collect_data = False
        _data = None

def readfile(filename):
    """readfile reads the contents of a CHAT file in XML format.
    It returns a tuple (participants,utterances), where participants
    is a dictionary mapping from identifiers to information about
    these identifiers, and a list of utterances."""
    global _filename, _participants, _utterances, _context
    _participants = {}
    _utterances = []
    _filename = filename
    f = file(filename, "rU")
    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = _start_element
    parser.EndElementHandler = _end_element
    parser.CharacterDataHandler = _char_data
    parser.buffer_text = True
    parser.returns_unicode = False
    parser.ParseFile(f)
    _filename = None
    return (_participants,_utterances)

