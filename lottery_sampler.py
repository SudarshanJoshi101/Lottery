import streamlit as st
import pandas as pd
import random
import io

# User inputs
start = st.number_input("Enter start number (inclusive)", value=1000)
end = st.number_input("Enter end number (exclusive)", value=8000)
total_numbers = st.number_input("Enter how many random numbers you want", value=540)
columns = st.number_input("Enter number of columns in the output", value=20)

if st.button("Generate Table"):
    if end - start < total_numbers:
        st.error("Range is too small for the number of unique values requested.")
    else:
        numbers = random.sample(range(start, end), int(total_numbers))
        
        # Sort and reshape numbers column-wise
        numbers.sort()
        rows = (total_numbers + columns - 1) // columns
        padded = numbers + [""] * (rows * columns - len(numbers))
        matrix = [padded[i::rows] for i in range(rows)]
        df = pd.DataFrame(matrix).transpose()
        df.index += 1  # 1-based indexing
        df.columns = [str(i + 1) for i in range(df.shape[1])]

        st.dataframe(df)

        # Save to Excel in-memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Download button
        st.download_button(
            label="📥 Download Excel File",
            data=output,
            file_name="sorted_random_table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
