import streamlit as st
#import rot
import unicodeit
from strats_module import *
from scipy.stats import lognorm

st.write('Hello!')

st.write('I wonder if MD style writing works. $1+1=2$.')

years = st.slider('Time', min_value=1, max_value=60, value=10)

principal = 1

#mu = st.slider('\N{GREEK SMALL LETTER MU}')
mu = st.slider(unicodeit.replace('\mu^*'), min_value=-1., max_value=3., value=0.)
#sigma = st.slider('\N{greek small letter sigma}')
sigma = st.slider(unicodeit.replace('\sigma^*'), min_value=0., max_value=3., value=0.)

mu2 = st.slider(unicodeit.replace('\mu^*_2'), min_value=-1., max_value=3., value=0.)
sigma2 = st.slider(unicodeit.replace('\sigma^*_2'), min_value=0., max_value=3., value=0.)

benchmark = st.slider('Benchmark Rate', min_value=-1., max_value=3., value=0.)

benchmark = (1 + benchmark) ** years * principal

st.write(get_mu(mu, sigma))
st.write(get_sig(mu, sigma))

strat1 = Strat(mu, sigma, years, principal)
strat2 = Strat(mu2, sigma2, years, principal)

st.write('got strats')

compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
# have to edit print commands
st.write('done compare')

st.pyplot(strat1.dstr_over_time(years=15, normalize=True))
# time set doesn't really matter for this graph

st.write('done plot')

# TODO more clever choice of graph bounds (use points of intersection?)
# and/or interactive plots
# split page for less scrolling
# type input / slider
# expected wait time message
inverse = True
fig, ax = plt.subplots()
ax.plot(*strat1.cum_dstr(inverse), label=strat1.label)
ax.plot(*strat2.cum_dstr(inverse), label=strat1.label)
ax.set_xlabel('Amount')
if inverse:
  ax.set_ylabel('P(<x)')
  ax.set_title('CDF Complement (chance of ending with at least x)')
else:
  ax.set_ylabel('P(>x)')
  ax.set_title('CDF (chance of ending with at most x)')
ax.vlines(benchmark, 0, 1, color='black', linestyles='--')
ax.legend()
st.pyplot(fig)




