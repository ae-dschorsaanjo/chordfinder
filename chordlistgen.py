#! /usr/bin/env python3


from os import listdir
from re import compile


ROOTS = [
    ['C', ''],
    ['C#', 'Db'],
    ['D', ''],
    ['Eb', 'Fb'],
    ['E', ''],
    ['F', ''],
    ['F#', 'Gb'],
    ['G', ''],
    ['Ab', 'G#'],
    ['A', ''],
    ['Bb', 'A#'],
    ['B', ''],
]
CHORDS = [
    ['', 'Major'],
    ['5', 'Power'],
    ['6', 'Major 6th'],
    ['7', 'Dominant 7th'],
    ['M7', 'Major 7th'],
    ['m', 'minor'],
    ['m6', 'minor 6th, diminished 7th'],
    ['m7', 'minor 7th'],
    ['mM7', 'minor Major 7th'],
    ['sus2', 'suspended 2nd'],
    ['sus4', 'suspended 4th'],
    ['+', 'augmented'],
    ['°', 'diminished'],
]
CLASS_MAP = {
    'C': 'c',
    'C#': 'db',
    'D': 'd',
    'Eb': 'eb',
    'E': 'e',
    'F': 'f',
    'F#': 'gb',
    'G': 'g',
    'Ab': 'ab',
    'A': 'a',
    'Bb': 'bb',
    'B': 'b',
    '': 'major',
    '5': 'power',
    '6': 'major6',
    '7': 'dom7',
    'M7': 'major7',
    'm': 'minor',
    'm6': 'minor6',
    'm7': 'minor7',
    'mM7': 'minormajor7',
    'sus2': 'sus2',
    'sus4': 'sus4',
    '+': 'aug',
    '°': 'dim',
}
EXT = 'svg'
IMG_DIR = 'chords'
OUT_HTML = 'index.html'

# --- ids used in template for string.format()

ID_ROOTS = 'roots'
ID_CHORDS = 'chords'
ID_CHORDLIST = 'chordlist'
ID_IMGS = 'chordimgs'
ID_ROOTFILTER = 'rootfilter'
ID_CHORDFILTER = 'chordfilter'
ID_ID_SEPARATOR = 'idseparator'
NAME_ROOT_FILTER = 'filter-root'
NAME_CHORD_FILTER = 'filter-chord'
SELECTOR_TEMPLATE = (
    '<div class="filterline">\n'
    '\t<input type="checkbox" id="{id_prefix}-{id}" name="{id_prefix}-{id}">'
    '<label for="{id_prefix}-{id}">\n'
    '\t<span class="mainname">{name}</span>\n'
    '\t<span class="secondaryname">{name2}</span>\n'
    '\t</label>'
    '</div>'
)
IMAGE_SECTION_TEMPLATE = '<section id="{root}">\n{chords}</section>\n'
IMAGE_CHORD_TEMPLATE = '<span class="{chord}">\n{imgs}</span>'
IMAGE_TEMPLATE = '<img src="{path}">\n'


def file_path(dir, filename, extension=EXT) -> str:
    return f"{dir}/{filename}.{extension}"


def list_all(dir) -> list[str]:
    files = []
    for c in listdir(dir):
        if c.endswith(EXT):
            files.append(c)
    return files


def get_chord(chordlist, root, chord) -> list[str]:
    if chord == "+":
        chord = "\\+"  # escape '+'
    if root == "C#":
        root = "Db"
    elif root == "F#":
        root = "Gb"
    r = compile(f"{root}{chord}_")
    return list(filter(r.match, chordlist))


def gen_selectors(template, src_list, id_prefix) -> str:
    out = []
    for elem in src_list:
        name, name2 = elem[0], elem[1]
        if name2:
            name2 = f"({name2})"
        out.append(template.format(id_prefix=id_prefix,
                                   id=CLASS_MAP[name],
                                   name=name,
                                   name2=name2))
    return "\n".join(out)


def gen_chordlist() -> dict:
    out = {}
    for r in ROOTS:
        out[r[0]] = []
        for c in CHORDS:
            out[r[0]].append(f"'{CLASS_MAP[r[0]]}-{CLASS_MAP[c[0]]}'")
    return out


def gen_imglist(dir=IMG_DIR) -> str:
    # create digestable dictionary
    allimgs = list_all(dir)
    chordtypes = CHORDS#[::-1]  # reverse list, can't search for Major chord
    masterlist = {}
    for r in ROOTS:
        root = r[0]
        masterlist[CLASS_MAP[root]] = {}
        for c in chordtypes:
            chord = c[0]
            tmp = get_chord(allimgs, root, chord)
            chordlist = []
            for t in tmp:
                print(f"root: {root}\tchord: {chord}\tt: {t}")
                chordlist.append(t)
                allimgs.remove(t)
            masterlist[CLASS_MAP[root]][CLASS_MAP[chord]] = chordlist[::-1]
        masterlist[CLASS_MAP[root]][CLASS_MAP[chord]] = masterlist[CLASS_MAP[root]][CLASS_MAP[chord]][::-1]
    if len(allimgs) != 0:  # sanity check
        print(f"There are {len(allimgs)} leftover files. Aborting.")
        exit(1)
    # process dictionary and generate html
    out = ''
    for m in masterlist:
        root = m
        chords = masterlist[root]
        chordspans = ''
        for c in chords:
            imgs = ''.join([IMAGE_TEMPLATE.format(path=f"{IMG_DIR}/{img}")
                           for img in chords[c]])
            chordspans += IMAGE_CHORD_TEMPLATE.format(root=root,
                                                     chord=c,
                                                     imgs=imgs) + "\n"
        out += IMAGE_SECTION_TEMPLATE.format(root=root, chords=chordspans)
    return out


def gen_html(name=OUT_HTML):
    template = ''
    with open("res/template.html", "r") as file:
        template = file.read()
    rootlist = gen_selectors(SELECTOR_TEMPLATE, ROOTS, NAME_ROOT_FILTER)
    chordidlist = gen_selectors(SELECTOR_TEMPLATE, CHORDS, NAME_CHORD_FILTER)
    chordlist = gen_chordlist()
    flat_chordlist = ','.join(
        [f"{chord}" for root in chordlist for chord in chordlist[root]]
    )
    imglist = gen_imglist()
    formats = {
        ID_ROOTS: rootlist,
        ID_CHORDS: chordidlist,
        ID_CHORDLIST: flat_chordlist,
        ID_IMGS: imglist,
        ID_CHORDFILTER: NAME_CHORD_FILTER,
        ID_ROOTFILTER: NAME_ROOT_FILTER,
        ID_ID_SEPARATOR: '-'
    }
    with open(name, 'w', encoding='utf-8') as file:
        file.write(template.format(**formats))


if __name__ == '__main__':
    gen_html()
