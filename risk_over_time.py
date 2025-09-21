import streamlit as st
#import rot
import unicodeit
from strats_module import *

st.write('Hello!')

st.write('I wonder if MD style writing works. $1+1=2$.')

#mu = st.slider('\N{GREEK SMALL LETTER MU}')
mu = st.slider(unicodeit.replace('\mu^*'), min_value=-1., max_value=3., value=0.)
#sigma = st.slider('\N{greek small letter sigma}')
sigma = st.slider(unicodeit.replace('\sigma^*'), min_value=0., max_value=3., value=0.)

st.write(get_mu(mu, sigma))
st.write(get_sig(mu, sigma))
