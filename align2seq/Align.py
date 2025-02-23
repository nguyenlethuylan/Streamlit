import streamlit as st

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
    
    return type1, type2, seq1, seq2, ''.join(alignment), match_count, maxlength # The join() method takes all items in an iterable and joins them into one string.

st.title("Sequence Alignment")  # Displays the main title of the app.

seq1 = st.text_input("Enter Sequence 1:") # Takes input for DNA/RNA sequences.
seq2 = st.text_input("Enter Sequence 2:")

if st.button("Align Sequences"): # Triggers the alignment function when clicked.
    if seq1 and seq2:
        type1, type2, aligned_seq1, aligned_seq2, alignment, match_count, maxlength = seqAlign(seq1, seq2)
        
        st.write(f"**Sequence 1 is {type1}**") # Displays sequence type and statistics.
        st.write(f"**Sequence 2 is {type2}**")
        st.write(f"Length of Sequence 1: {len(seq1)}")
        st.write(f"Length of Sequence 2: {len(seq2)}")
        
        st.text("Alignment result:") # Shows the aligned sequences in a formatted way.
        st.text(aligned_seq1)
        st.text(alignment)
        st.text(aligned_seq2)
        
        st.write(f"**Total matching nucleotides: {match_count}/{maxlength}**")
    else:
        st.warning("Please enter both sequences!") # Alerts if input is missing.
