import streamlit as st
import pandas as pd
import numpy as np

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
st.markdown("<h2 style='text-align: center; color: #5243AA;'>Welcome to our pub finder app! 🎉</h2>", unsafe_allow_html=True)

# Add an image of a pub
st.image('pub.jpg', use_column_width=True)

# Display some basic information about the dataset
st.write(f"The dataset contains **{len(pub_data)}** pub locations.")
st.write(f"The dataset covers **{len(pub_data['local_authority'].unique())}** local authorities.")
st.markdown("<h2 style='text-align: center; color: #7F45FA;'>Pub Data! 🎉</h2>", unsafe_allow_html=True)
st.markdown("<style>div.stDataFrame div[data-testid='stHorizontalBlock'] div[data-testid='stDataFrameContainer'] {margin: 0 auto;}</style>", unsafe_allow_html=True)
st.write(pub_data)

#  Display some statistics about the dataset
st.write("Here are some statistics about the dataset:")
# st.write(pub_data.describe())
stats = pub_data.describe().T
stats['count'] = stats['count'].astype(int)
stats = stats[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
st.dataframe(stats.style.highlight_max(axis=0, color='#EB6864'))

# Add a fun fact about pubs in the UK
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("🤓 Fun fact: Did you know that the oldest pub in the UK, Ye Olde Fighting Cocks, is over 1,200 years old and located in St Albans, England? 🏰")

# Add a footer with some information about the app
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Data source: https://www.getthedata.com/open-pubs")
st.sidebar.image('banner_top.png', use_column_width=True)
