import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static


# Load the pub dataset
pub_data = pd.read_csv('open_pubs.csv', header=None)
pub_data.columns = ['fsa_id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority']

# Replace \N values with NaN
pub_data = pub_data.replace('\\N', np.nan)

# Drop rows with NaN values
pub_data = pub_data.dropna()

pub_data['longitude'] = pd.to_numeric(pub_data['longitude'], errors='coerce')
pub_data['latitude'] = pd.to_numeric(pub_data['latitude'], errors='coerce')

# Set the page layout to centered
st.set_page_config(layout="centered")

# Add some styling to the title and subtitle
st.markdown("<h1 style='text-align: center; color: #EB6864; font-weight: bold;'>🍺 Open Pubs Application 🍻</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #5243AA;'>Pub Locations</h2>", unsafe_allow_html=True)

# Allow user to choose between searching by postal code or local authority
search_type = st.radio("Search by:", ('Postal Code', 'Local Authority'))

# Create a list of unique postal codes or local authorities to display in the dropdown menu
if search_type == 'Postal Code':
    search_list = sorted(pub_data['postcode'].unique())
else:
    search_list = sorted(pub_data['local_authority'].unique())

# Allow user to select a postal code or local authority from the dropdown menu
search_value = st.selectbox(f"Select a {search_type}:", search_list)

# Filter the dataset based on the selected postal code or local authority
if search_type == 'Postal Code':
    filtered_data = pub_data[pub_data['postcode'] == search_value]
else:
    filtered_data = pub_data[pub_data['local_authority'] == search_value]

# Display the filtered dataset
st.write(f"Displaying {len(filtered_data)} pubs in {search_value}:")
st.dataframe(filtered_data)

# Create a map centered on the chosen location
m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=13)

# Add markers for each pub in the filtered dataset
for index, row in filtered_data.iterrows():
    folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Display the map
folium_static(m)

# Add a footer with some information about the app
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Data source: https://www.getthedata.com/open-pubs")
st.sidebar.image('banner_top.png', use_column_width=True)
