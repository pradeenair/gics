import streamlit as st
import requests
from bs4 import BeautifulSoup

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
                # Retrieve the company's profile page from Yahoo Finance
                url = f"https://finance.yahoo.com/quote/{company_name}/profile?p={company_name}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract the GICS classifications from the page
                gics_sector = soup.select('span:contains("GICS Sector") + span')[0].text
                industry_group = soup.select('span:contains("GICS Industry Group") + span')[0].text
                industry = soup.select('span:contains("GICS Sub-Industry") + span')[0].text
                sub_industry = soup.select('span:contains("Full Time Employees") + span')[0].text

                # Display the results
                st.write(f"- GICS Sector: {gics_sector}")
                st.write(f"- Industry Group: {industry_group}")
                st.write(f"- Industry: {industry}")
                st.write(f"- Sub-Industry: {sub_industry}")
            except Exception as e:
                st.write(f"Error: Could not retrieve information for this company. Exception: {e}")
    else:
        st.write("No company names found in the uploaded file.")
