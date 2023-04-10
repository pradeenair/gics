import streamlit as st
import requests

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
                # Retrieve the company's information from the Google Knowledge Graph API
                url = f"https://kgsearch.googleapis.com/v1/entities:search?query={company_name}&types=Organization&limit=1&indent=True&key=<YOUR_API_KEY>"
                response = requests.get(url)
                data = response.json()

                # Extract the GICS classifications and number of employees from the API response
                gics_sector = data['itemListElement'][0]['result']['industry']
                industry_group = data['itemListElement'][0]['result']['industryGroup']
                industry = data['itemListElement'][0]['result']['industryCode']
                sub_industry = data['itemListElement'][0]['result']['subIndustryCode']
                employees = data['itemListElement'][0]['result'].get('employees')

                # Display the results
                st.write(f"- GICS Sector: {gics_sector}")
                st.write(f"- Industry Group: {industry_group}")
                st.write(f"- Industry: {industry}")
                st.write(f"- Sub-Industry: {sub_industry}")
                if employees:
                    st.write(f"- Number of Employees: {employees}")
                else:
                    st.write("- Number of Employees: Not available")
            except Exception as e:
                st.write(f"Error: Could not retrieve information for this company. Exception: {e}")
    else:
        st.write("No company names found in the uploaded file.")
