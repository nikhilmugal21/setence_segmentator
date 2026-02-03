# NP/VP Sentence Segmenter (Streamlit)

A small Streamlit app that takes an **English sentence**, performs **POS tagging + rule-based chunking**, and renders a **syntactic diagram** showing phrase-level structure (e.g., **NP**, **VP**, **PP**) along with tags like **DT** (determiner), **JJ** (adjective), **NN** (noun), **VB** (verb), etc.

This is useful for quick demos, teaching basic phrase structure, and experimenting with shallow parsing.

---

## Features

- Tokenization + POS tagging for English
- Phrase chunking with a configurable grammar:
  - **NP**: determiner + adjectives + noun(s)
  - **VP**: verb + optional NP/PP
  - **PP**: preposition + NP
- Diagram visualization of the chunked structure (tree-style)

---

## Example

Input: The old man bought a red rose.
Output: **NP**: The / old / man
        **VP**: bought + **NP** (a / red / rose)
