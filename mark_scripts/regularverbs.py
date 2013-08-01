"""regularverbs.py extracts regular verbs and their inflections
from CHILDES files."""

import lx, re, xmlchat

childes_dir = "/usr/local/data/CHILDES/data-xml/English-USA/Brent"

for xmlfile in lx.findfiles(childes_dir, re.compile(r".*\.xml")):
    roles, utterances = xmlchat.readfile(xmlfile)
    for utt in utterances:
        id = utt['who']
        role = roles[id]['role']
        if role in ["Mother","Father"]:
            for morph in utt.get('mor', []):
                if morph['c'] == 'v':
                    print morph

