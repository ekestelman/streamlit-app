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
principal = 1.  # type has to match st input type

st.write('### Welcome to my streamlit app!')
st.write('This is a place to explore my coding projects.')
st.write('### Investment Risk Over Time')
st.write('This project is for comparing investments of differing expected returns and variances. Choose the following parameters, and see the results.')

st.write(years, principal, benchmark, mu, sigma, mu2, sigma2)

# border arg only in later versions
col1, col2 = st.columns([1,2], vertical_alignment='center')

# XXX does this actually work with t=0? Yes!
# if you set a value in num_input, slider changes to reflect that input. But the other
# way around is not true. Then if you want to use the num_input val again, just hitting
# enter on it won't work. Val has to change to update / initiate rerun
# Better to have slider on left or right? Better to update text on slider or slider on text?
# FIXME set input to x, set slider to y, set input to z then back to x, val returns to y.
years = col1.number_input(label='Time (truncates to integer)', min_value=0, value=years)
years = col2.slider(label='', min_value=0, max_value=60, value=years)

principal = col1.number_input(label='Principal', min_value=0., value=principal, step=.1)
# Makes more sense to give options in thousands?
# .1 step might represent $100
principal = col2.slider(label='', min_value=0., max_value=50., value=principal, step=.1)

benchmark = col1.number_input('Benchmark Rate', value=benchmark, format='%.15g')
benchmark = col2.slider(label='', min_value=-0., max_value=.5, value=benchmark, format='%.15g')

benchmark = (1 + benchmark) ** years * principal

# format = '%.' + [decimal places] + 'g' for 'general' format
# can use min_value and max_value to restrict inputs for number_input
# need key for sliders if labels (and all args) are repeated
mu = col1.number_input(label=unicodeit.replace('\mu^*'), value=mu, format='%.15g')
# TODO maybe take out the slider label if we also have the text input?
# change slider step now that we have reduced the range?
mu = col2.slider(label='', min_value=-0., max_value=.3, value=mu, format='%.15g', key='mu1')
sigma = col1.number_input(label=unicodeit.replace('\sigma^*'), \
                        min_value=0., value=sigma, format='%.15g')
sigma = col2.slider('', min_value=0., max_value=.3, value=sigma, format='%.15g', key='sig1')

mu2 = col1.number_input(label=unicodeit.replace('\mu^*_2'), value=mu2, format='%.15g')
mu2 = col2.slider(label='', min_value=-0., max_value=.3, value=mu2, format='%.15g', key='mu2')
sigma2 = col1.number_input(label=unicodeit.replace('\sigma^*_2'), \
                         min_value=0., value=sigma2, format='%.15g')
sigma2 = col2.slider('', min_value=0., max_value=.3, value=sigma2, format='%.15g', key='sig2')

st.write(years, principal, benchmark, mu, sigma, mu2, sigma2)

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




