import streamlit as st
import nltk
from nltk import Tree
import streamlit.components.v1 as components

# ---- One-time downloads (cached) ----
@st.cache_resource
def setup_nltk():
    import nltk

    # Tokenizers
    nltk.download("punkt", quiet=True)
    try:
        nltk.download("punkt_tab", quiet=True)
    except Exception:
        pass

    # POS taggers (old + new naming)
    nltk.download("averaged_perceptron_tagger", quiet=True)
    try:
        nltk.download("averaged_perceptron_tagger_eng", quiet=True)
    except Exception:
        pass

setup_nltk()


# ---- Chunk grammar (simple, like your example) ----
# NP: (Det) (Adj*) (Noun+)
# VP: Verb + (NP) + (optional PP)
PENN_TAG_GLOSSARY = {
    "CC": "Coordinating conjunction",
    "CD": "Cardinal number",
    "DT": "Determiner",
    "EX": "Existential there",
    "FW": "Foreign word",
    "IN": "Preposition/subordinating conjunction",
    "JJ": "Adjective",
    "JJR": "Adjective, comparative",
    "JJS": "Adjective, superlative",
    "LS": "List item marker",
    "MD": "Modal",
    "NN": "Noun, singular or mass",
    "NNS": "Noun, plural",
    "NNP": "Proper noun, singular",
    "NNPS": "Proper noun, plural",
    "PDT": "Predeterminer",
    "POS": "Possessive ending",
    "PRP": "Personal pronoun",
    "PRP$": "Possessive pronoun",
    "RB": "Adverb",
    "RBR": "Adverb, comparative",
    "RBS": "Adverb, superlative",
    "RP": "Particle",
    "SYM": "Symbol",
    "TO": "to",
    "UH": "Interjection",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund/present participle",
    "VBN": "Verb, past participle",
    "VBP": "Verb, non-3rd person singular present",
    "VBZ": "Verb, 3rd person singular present",
    "WDT": "Wh-determiner",
    "WP": "Wh-pronoun",
    "WP$": "Possessive wh-pronoun",
    "WRB": "Wh-adverb",
    ".": "Sentence-final punctuation",
    ",": "Comma",
    ":": "Colon or ellipsis",
    "``": "Opening quotation mark",
    "''": "Closing quotation mark",
    "(": "Left bracket",
    ")": "Right bracket",
}

def build_used_pos_glossary(pos_tags):
    """
    pos_tags: list of (token, tag)
    returns: rows for Streamlit table with only used tags
    """
    used_tags = sorted({tag for _, tag in pos_tags})
    return [
        {
            "POS tag": tag,
            "Meaning": PENN_TAG_GLOSSARY.get(tag, "Unknown tag"),
        }
        for tag in used_tags
    ]


GRAMMAR = r"""
  NP: {<DT>?<JJ.*>*<NN.*>+}
  PP: {<IN><NP>}
  VP: {<VB.*><NP|PP>*}
"""
chunker = nltk.RegexpParser(GRAMMAR)

def chunk_sentence(sent: str) -> Tree:
    tokens = nltk.word_tokenize(sent)
    tags = nltk.pos_tag(tokens)
    tree = chunker.parse(tags)
    return tree, tags

def tree_to_svg_html(tree: Tree) -> str:
    # svgling renders NLTK trees as SVG (no system graphviz needed).
    import svgling
    svg = svgling.draw_tree(tree)._repr_svg_()
    return svg

st.set_page_config(page_title="NP/VP Segmenter", layout="centered")
st.title("English Sentence → NP/VP Segmented Diagram")

sentence = st.text_input(
    "Enter an English sentence",
    value="The old man bought a red rose."
)

if sentence.strip():
    try:
        t, tags = chunk_sentence(sentence)
        svg = tree_to_svg_html(t)

        st.subheader("Segmented diagram")
        # Streamlit displays SVG via HTML component reliably
        svg = tree_to_svg_html(t)
        components.html(svg, height=420, scrolling=True)

        st.subheader("POS tag glossary")
        st.table(build_used_pos_glossary(tags))

    except Exception as e:
        st.error(f"Something went wrong: {e}")
