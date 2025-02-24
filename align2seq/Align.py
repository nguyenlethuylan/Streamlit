import streamlit as st
import pathlib
from PIL import Image
import os

# Load the image
image_path = pathlib.Path.cwd() / "source" / "image.png"
if image_path.exists():
    img = Image.open(image_path)
    st.image(img, caption="This describes the alignment of 2 sequences", width=800)
else:
    st.warning("Image file not found!")

# Function to load CSS from a given file path
def load_css(css_file_path):
    if css_file_path.exists():
        with open(css_file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"CSS file not found: {css_file_path}")

# Load external CSS
css_path = pathlib.Path.cwd() / "source" / "style.css"
load_css(css_path)

# Sequence Alignment Function
def seqAlign(seq1, seq2):
    seq1, seq2 = seq1.upper(), seq2.upper()
    type1, type2 = ("RNA" if "U" in seq1 else "DNA"), ("RNA" if "U" in seq2 else "DNA")

    # Pad sequences to the same length
    max_len = max(len(seq1), len(seq2))
    seq1, seq2 = seq1.ljust(max_len, '-'), seq2.ljust(max_len, '-')

    # Compute alignment
    alignment = "".join("|" if a == b and a != "-" else " " for a, b in zip(seq1, seq2))
    match_count = alignment.count("|")

    return type1, type2, seq1, seq2, alignment, match_count, max_len

# Function to split long sequences into multiple lines
def split_sequence(seq, line_length=50):
    return [seq[i:i+line_length] for i in range(0, len(seq), line_length)]

# Streamlit UI
st.title("Sequence Alignment Tool")

seq1 = st.text_area("Enter Sequence 1:")
seq2 = st.text_area("Enter Sequence 2:")

if st.button("Align Sequences"):
    if seq1 and seq2:
        type1, type2, aligned_seq1, aligned_seq2, alignment, match_count, max_len = seqAlign(seq1, seq2)

        st.success(f"**Sequence 1 is {type1}**")
        st.success(f"**Sequence 2 is {type2}**")
        st.write(f"Length of Sequence 1: **{len(seq1)}**")
        st.write(f"Length of Sequence 2: **{len(seq2)}**")

        # Split the alignment result into multiple lines
        split_seq1 = split_sequence(aligned_seq1)
        split_align = split_sequence(alignment)
        split_seq2 = split_sequence(aligned_seq2)

        # Display alignment result in Streamlit
        st.markdown("### **Alignment Result:**")
        alignment_text = ""
        for s1, al, s2 in zip(split_seq1, split_align, split_seq2):
            alignment_text += f"{s1}\n{al}\n{s2}\n\n"

        st.code(alignment_text, language="plaintext")

        # Write the result to a .txt file for download
        result_text = f"Sequence 1 ({type1}):\n{seq1}\n\n"
        result_text += f"Sequence 2 ({type2}):\n{seq2}\n\n"
        result_text += f"Alignment Result:\n{alignment_text}\n"
        result_text += f"Total Matching Nucleotides: {match_count}/{max_len}\n"

        result_file = "alignment_result.txt"
        with open(result_file, "w") as f:
            f.write(result_text)

        # Provide a download button for the alignment result
        st.download_button(label="Download Alignment Result", data=result_text, file_name=result_file, mime="text/plain")
    else:
        st.warning("Please enter both sequences!")
