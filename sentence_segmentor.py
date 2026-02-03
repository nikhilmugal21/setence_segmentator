import streamlit as st
import nltk
from nltk import Tree
import streamlit.components.v1 as components

# ---- One-time downloads (cached) ----
@st.cache_resource
def setup_nltk():
    import nltk
    nltk.download("punkt", quiet=True)
    try:
        nltk.download("punkt_tab", quiet=True)
    except Exception:
        pass
    nltk.download("averaged_perceptron_tagger", quiet=True)

setup_nltk()
)

# ---- Chunk grammar (simple, like your example) ----
# NP: (Det) (Adj*) (Noun+)
# VP: Verb + (NP) + (optional PP)
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
    return tree

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
        t = chunk_sentence(sentence)
        svg = tree_to_svg_html(t)

        st.subheader("Segmented diagram")
        # Streamlit displays SVG via HTML component reliably
        components.html(svg, height=420, scrolling=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
