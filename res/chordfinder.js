const CHORD_FILTERS = document.querySelectorAll("#chords-container input[type=checkbox]");
const ROOT_FILTERS = document.querySelectorAll("#roots-container input[type=checkbox]");
const EVERY_FILTER = [...ROOT_FILTERS, ...CHORD_FILTERS];
const HIDDEN = 'hidden';
const ROOTS_CONTAINER = document.getElementById("roots-container");
const CHORDS_CONTAINER = document.getElementById("chords-container");
const CHORDS_SEL_ALL = document.getElementById("chords-all");
const ROOTS_SEL_ALL = document.getElementById("roots-all");
const CHORDS_SEL_NONE = document.getElementById("chords-none");
const ROOTS_SEL_NONE = document.getElementById("roots-none");

function getIdFromSelector(selectorID) {
    return selectorID.split("-").pop();
}

var isButtonEvent = false;

function filter() {
    if (isButtonEvent) return;
    let root_yes = [];
    let root_no = [];
    for (const root of ROOT_FILTERS) {
        let id = getIdFromSelector(root.id);
        if (root.checked) root_yes.push(id);
        else root_no.push(id);
    };
    root_yes.forEach(id => {
        document.getElementById(id).style.display = "block";
    });
    root_no.forEach(id => {
        document.getElementById(id).style.display = "none";
    });
    for (const chord of CHORD_FILTERS) {
        let cls = getIdFromSelector(chord.id);
        for (const e of document.querySelectorAll('.' + cls)) {
            e.style.display = (chord.checked ? "inline" : "none");
        };
    };
}

ROOTS_SEL_ALL.addEventListener('click', elem => {
    isButtonEvent = true;
    ROOT_FILTERS.forEach(e => {
        e.checked = true;
    });
    isButtonEvent = false
    filter();
});

ROOTS_SEL_NONE.addEventListener('click', elem => {
    isButtonEvent = true;
    ROOT_FILTERS.forEach(e => {
        e.checked = false;
    });
    isButtonEvent = false
    filter();
});

CHORDS_SEL_ALL.addEventListener('click', elem => {
    isButtonEvent = true;
    CHORD_FILTERS.forEach(e => {
        e.checked = true;
    });
    isButtonEvent = false
    filter();
});

CHORDS_SEL_NONE.addEventListener('click', elem => {
    isButtonEvent = true;
    CHORD_FILTERS.forEach(e => {
        e.checked = false;
    });
    isButtonEvent = false
    filter();
});

EVERY_FILTER.forEach(e => {
    e.addEventListener('change', elem => {
        filter();
    })
});

ROOTS_SEL_ALL.click();
CHORDS_SEL_ALL.click();