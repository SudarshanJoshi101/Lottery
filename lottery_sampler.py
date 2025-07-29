import streamlit as st
import pandas as pd
import numpy as np
import io

st.title("🎲 Sorted Random Number Generator")

start_num = st.number_input("From which number?", value=1000)
end_num = st.number_input("Till what number?", value=8000)
num_columns = st.number_input("How many columns?", value=20)
num_random = st.number_input("How many numbers to generate?", value=540)

if st.button("Generate"):
    if end_num - start_num < num_random:
        st.error("Range is too small for the number of unique values requested.")
    else:
        random_numbers = np.random.choice(range(start_num, end_num), int(num_random), replace=False)
        random_numbers.sort()

        num_rows = -(-num_random // num_columns)  # ceiling division
        padded = np.append(random_numbers, [np.nan] * (num_rows * num_columns - num_random))
        reshaped = padded.reshape((int(num_columns), num_rows)).T

        df = pd.DataFrame(reshaped, columns=[f"{i+1}" for i in range(int(num_columns))])
        st.dataframe(df)

        # Downloadable Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Download Excel File", output.getvalue(), file_name="sorted_columnwise_output.xlsx")
