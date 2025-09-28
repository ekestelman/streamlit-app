import streamlit as st
#import rot
import unicodeit
from strats_module import *
from scipy.stats import lognorm

# Better to have this in module or dict?
years = 10
mu = .1
sigma = .15
mu2 = .15
sigma2 = .25
benchmark = .08

st.write('Hello!')

st.write('I wonder if MD style writing works. $1+1=2$.')

# XXX does this actually work with t=0?
years = st.number_input(label='Time (truncates to integer)', min_value=0, value=years)
years = st.slider(label='', min_value=0, max_value=60, value=years)

principal = 1

benchmark = st.number_input('Benchmark Rate', value=benchmark, format='%.15g')
benchmark = st.slider(label='', min_value=-0., max_value=.5, value=benchmark, format='%.15g')

benchmark = (1 + benchmark) ** years * principal

# format = '%.' + [decimal places] + 'g' for 'general' format
# can use min_value and max_value to restrict inputs for number_input
# need key for sliders if labels (and all args) are repeated
mu = st.number_input(label=unicodeit.replace('\mu^*'), value=mu, format='%.15g')
# TODO maybe take out the slider label if we also have the text input?
# change slider step now that we have reduced the range?
mu = st.slider(label='', min_value=-0., max_value=.3, value=mu, format='%.15g', key='mu1')
sigma = st.number_input(label=unicodeit.replace('\sigma^*'), \
                        min_value=0., value=sigma, format='%.15g')
sigma = st.slider('', min_value=0., max_value=.3, value=sigma, format='%.15g', key='sig1')

mu2 = st.number_input(label=unicodeit.replace('\mu^*_2'), value=mu2, format='%.15g')
mu2 = st.slider(label='', min_value=-0., max_value=.3, value=mu2, format='%.15g', key='mu2')
sigma2 = st.number_input(label=unicodeit.replace('\sigma^*_2'), \
                         min_value=0., value=sigma2, format='%.15g')
sigma2 = st.slider('', min_value=0., max_value=.3, value=sigma2, format='%.15g', key='sig2')

st.write(get_mu(mu, sigma))
st.write(get_sig(mu, sigma))

strat1 = Strat(mu, sigma, years, principal)
strat2 = Strat(mu2, sigma2, years, principal)

st.write('got strats')

compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
# have to edit print commands
st.write('done compare')

st.pyplot(strat1.dstr_over_time(years=15, normalize=True))
strat1.recalc(years)
# Can try executing recalc in dstr func call, or find out how to rerun otherwise.
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
ax.plot(*strat2.cum_dstr(inverse), label=strat2.label)
ax.set_xlabel('Amount')
if inverse:
  ax.set_ylabel('P(>x)')
  ax.set_title('CDF Complement (chance of ending with at least x)')
else:
  ax.set_ylabel('P(<x)')
  ax.set_title('CDF (chance of ending with at most x)')
ax.vlines(benchmark, 0, 1, color='black', linestyles='--')
ax.legend()
st.pyplot(fig)




