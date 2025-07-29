import streamlit as st
import pandas as pd
import numpy as np
import random

st.title("🎲 Random Number Table Generator")

# Input widgets
start_num = st.number_input("From which number (inclusive)", value=1000, step=1)
end_num = st.number_input("Till what number (exclusive)", value=8000, step=1)
num_columns = st.number_input("Number of columns in output", value=20, step=1)
total_numbers = st.number_input("Total random numbers to generate", value=540, step=1)

if st.button("Generate Table"):
    if end_num - start_num < total_numbers:
        st.error("Range too small for the number of unique values requested.")
    else:
        # Step 1: Generate sorted random numbers
        random_numbers = sorted(random.sample(range(start_num, end_num), total_numbers))

        # Step 2: Pad to fill complete table
        rows = (total_numbers + num_columns - 1) // num_columns
        random_numbers += [None] * (rows * num_columns - total_numbers)

        # Step 3: Arrange column-wise
        array = np.array(random_numbers).reshape((rows, num_columns), order='F')
        df = pd.DataFrame(array)

        # Step 4: Set column names to 1-based index
        df.columns = [str(i) for i in range(1, num_columns + 1)]

        # Step 5: Download option
        st.dataframe(df)
        st.download_button("📥 Download Excel File", df.to_excel(index=False, engine='openpyxl'), file_name="sorted_random_table.xlsx")

