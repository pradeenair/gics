import streamlit as st
import yfinance as yf

st.title("Company List Analyzer")

# Upload txt file containing company names
uploaded_file = st.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    # Read the uploaded file
    file_contents = uploaded_file.read()
    file_lines = file_contents.decode().split('\n')

    # Remove empty lines and duplicates
    company_names = list(set([line.strip() for line in file_lines if line.strip()]))

    if len(company_names) > 0:
        # Loop through each company name and retrieve its info
        for company_name in company_names:
            st.write(f"**{company_name}**")
            try:
                # Retrieve stock information from Yahoo Finance
                stock_info = yf.Ticker(company_name).info

                # Extract GICS sector, industry group, industry, and sub-industry
                gics_sector = stock_info['sector']
                industry_group = stock_info['industry']
                industry = stock_info['longBusinessSummary'].split('\n')[0]
                sub_industry = stock_info['longBusinessSummary'].split('\n')[1]

                # Display the results
                st.write(f"- GICS Sector: {gics_sector}")
                st.write(f"- Industry Group: {industry_group}")
                st.write(f"- Industry: {industry}")
                st.write(f"- Sub-Industry: {sub_industry}")
            except:
                st.write("Error: Could not retrieve information for this company.")
    else:
        st.write("No company names found in the uploaded file.")
