import usaddress as ad
import pandas as pd
import streamlit as st

st.header("Address Parser")
st.subheader("Please be sure that the address column has a header of 'Address'")

df = pd.DataFrame(None)
uploaded_file = st.file_uploader("Please upload an Excel file with a list of addresses", type = ['xlsx'])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    for i,row in df.iterrows():
        try:
            parsed = ad.tag(row['Address'])
            dt = parsed[0]
            for key,value in dt.items():
                if key == 'AddressNumber':
                    df.loc[i, 'AddressNumber'] = value
                if key == 'AddressNumberPrefix':
                    df.loc[i, 'AddressNumberPrefix'] = value
                if key == 'AddressNumberSuffix':
                    df.loc[i, 'AddressNumberSuffix'] = value
                if key == 'BuildingName':
                    df.loc[i, 'BuildingName'] = value
                if key == 'OccupancyType':
                    df.loc[i, 'OccupancyType'] = value
                if key == 'USPSBoxType':
                    df.loc[i, 'USPSBoxType'] = value
                if key == 'USPSBoxGroupID':
                    df.loc[i, 'USPSBoxGroupID'] = value
                if key == 'USPSBoxGroupType':
                    df.loc[i, 'USPSBoxGroupType'] = value
                if key == 'USPSBoxID':
                    df.loc[i, 'USPSBoxID'] = value
                if  key == 'StreetName':
                    df.loc[i, 'StreetName'] = value
                if key == 'StreetNamePostType':
                    df.loc[i, 'StreetNamePostType'] = value
                if key == 'PlaceName':
                    df.loc[i, 'PlaceName'] = value
                if key == 'StateName':
                    df.loc[i, 'StateName'] = value
                if key == 'ZipCode':
                    df.loc[i, 'ZipCode'] = value
                if key == 'CountryName':
                    df.loc[i, 'CountryName'] = value
        except:
            continue

    
    dwn = df.to_csv(index= False)
    
    st.download_button(label="Download data as CSV"
                       , data = dwn
                       , file_name = 'Address_output.csv'
                       , mime='text/csv')
 
