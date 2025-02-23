import streamlit as st
import pathlib
from PIL import Image 

# Load the image
image_path = "/home/lannguyen/Documents/streamlit/align2seq/source/image.png"
img = Image.open(image_path)

# Display image in Streamlit
st.image(
    img,
    caption="This describes the alignment of 2 sequences",
    width=800,
)

# Function to load CSS from a given file path
def load_css(css_file_path):
    try:
        with open(css_file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file_path}")

# Load the external CSS
css_path = pathlib.Path("/home/lannguyen/Documents/streamlit/align2seq/source/style.css")
load_css(css_path)

# Sequence Alignment Function
def seqAlign(seq1, seq2):
    len1, len2 = len(seq1), len(seq2)
    
    type1 = "RNA" if 'U' in seq1 else "DNA"
    type2 = "RNA" if 'U' in seq2 else "DNA"
    
    maxlength = max(len1, len2)
    seq1 = seq1.ljust(maxlength, '-')
    seq2 = seq2.ljust(maxlength, '-')
    
    match_count = 0
    alignment = []
    
    for i in range(maxlength):
        if seq1[i] == seq2[i]:
            alignment.append('|')
            match_count += 1
        else:
            alignment.append(' ')
    
    return type1, type2, seq1, seq2, ''.join(alignment), match_count, maxlength

st.title("Sequence Alignment")  # Displays the main title of the app.

seq1 = st.text_input("Enter Sequence 1:")  # Takes input for DNA/RNA sequences.
seq2 = st.text_input("Enter Sequence 2:")

if st.button("Align Sequences", key="click"):  # Triggers the alignment function when clicked.
    if seq1 and seq2:
        type1, type2, aligned_seq1, aligned_seq2, alignment, match_count, maxlength = seqAlign(seq1, seq2)
        
        st.write(f"**Sequence 1 is {type1}**")  # Displays sequence type and statistics.
        st.write(f"**Sequence 2 is {type2}**")
        st.write(f"Length of Sequence 1: {len(seq1)}")
        st.write(f"Length of Sequence 2: {len(seq2)}")
        
        st.text("Alignment result:")  # Shows the aligned sequences in a formatted way.
        st.text(aligned_seq1)
        st.text(alignment)
        st.text(aligned_seq2)
        
        st.write(f"**Total matching nucleotides: {match_count}/{maxlength}**")
    else:
        st.warning("Please enter both sequences!")  # Alerts if input is missing.
