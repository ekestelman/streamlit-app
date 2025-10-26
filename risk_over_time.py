import streamlit as st
#import rot
import unicodeit
from rot_lib.strats_module import *
from scipy.stats import lognorm
from time import time

def update_inputs(param, src=None):
  # callback function
  # key is parameter, source is tool used for input
  if src is None:
    # lazy: assume input type (src) will be str of len 5
    src = param[-5:]
    param = param[:-5]
  out = {'slide': 'input', 'input': 'slide'}[src]
  st.session_state[param + out] = st.session_state[param + src]
#x = st.number_input(label='x', value=0, key='xinput', on_change=updatex, args=('x', 'input'))
#x = st.slider(label='', value=x, key='xslider', on_change=updatex, args=('x', 'slider'))
#st.write(x, st.session_state.xinput, st.session_state.xslider)


# Better to have this in module or dict?
years = 10
mu = .1
sigma = .15
mu2 = .15
sigma2 = .25
benchmark = .08
principal = 1.  # type has to match st input type
input_rows = 7  # nrows = ninputs

#st.write('# Welcome to my streamlit app :wave:')
#st.write('This is a place to explore my coding projects.')
st.write('## Investment Risk Over Time :chart:')
st.write('This project is for comparing investments of different expected returns and variances. Choose the following parameters, and see the results.')

# Changing values later does not change this line
# Make sure that values match supposed inputs!
st.write(years, principal, benchmark, mu, sigma, mu2, sigma2)

# border arg only in later versions
col1, col2 = st.columns([1,2], vertical_alignment='center')

input_grid = [st.columns([1,2]) for _ in range(input_rows)]

# XXX does this actually work with t=0? Yes!
# if you set a value in num_input, slider changes to reflect that input. But the other
# way around is not true. Then if you want to use the num_input val again, just hitting
# enter on it won't work. Val has to change to update / initiate rerun
# Better to have slider on left or right? Better to update text on slider or slider on text?
# FIXME set input to x, set slider to y, set input to z then back to x, val returns to y.
# this only happens when the changes are made before the program fully runs! If it is
# allowed to run fully, then this does not occur.
current_row = 0
years = input_grid[current_row][0].number_input(label='Time (truncates to integer)',
        min_value=0, value=years, key='time_input', on_change=update_inputs, 
        args=['time_input'])
years = input_grid[current_row][1].slider(label='', min_value=0, max_value=60, 
        value=years, key='time_slide', on_change=update_inputs, args=['time_slide'])
current_row += 1

# XXX Projected growth plot is normalized and does not depend on principal, want to 
# change this?
# CDF is using principal.
principal = input_grid[current_row][0].number_input(label='Principal', min_value=0.,
            value=principal, step=.1, key='principal_input', on_change=update_inputs,
            args=('principal_', 'input'))
# Makes more sense to give options in thousands?
# .1 step might represent $100
principal = input_grid[current_row][1].slider(label='', min_value=0., max_value=50.,
            value=principal, step=.1, key='principal_slide', on_change=update_inputs,
            args=('principal_', 'slide'))
current_row += 1

# TODO option to exclude benchmark?
benchmark = input_grid[current_row][0].number_input('Benchmark Rate', value=benchmark, format='%.15g')
benchmark = input_grid[current_row][1].slider(label='', min_value=-0., max_value=.5, value=benchmark, format='%.15g')
current_row += 1

benchmark = (1 + benchmark) ** years * principal

# format = '%.' + [decimal places] + 'g' for 'general' format
# can use min_value and max_value to restrict inputs for number_input
# need key for sliders if labels (and all args) are repeated
mu = input_grid[current_row][0].number_input(label=unicodeit.replace('\mu^*'), value=mu, format='%.15g')
# TODO maybe take out the slider label if we also have the text input?
# change slider step now that we have reduced the range?
mu = input_grid[current_row][1].slider(label='', min_value=-0., max_value=.3, value=mu, format='%.15g', key='mu1')
current_row += 1
sigma = input_grid[current_row][0].number_input(label=unicodeit.replace('\sigma^*'), \
                        min_value=0., value=sigma, format='%.15g')
sigma = input_grid[current_row][1].slider('', min_value=0., max_value=.3, value=sigma, format='%.15g', key='sig1')
current_row += 1

mu2 = input_grid[current_row][0].number_input(label=unicodeit.replace('\mu^*_2'), value=mu2, format='%.15g')
mu2 = input_grid[current_row][1].slider(label='', min_value=-0., max_value=.3, value=mu2, format='%.15g', key='mu2')
current_row += 1
sigma2 = input_grid[current_row][0].number_input(label=unicodeit.replace('\sigma^*_2'), \
                         min_value=0., value=sigma2, format='%.15g')
sigma2 = input_grid[current_row][1].slider('', min_value=0., max_value=.3, value=sigma2, format='%.15g', key='sig2')
current_row += 1

st.write('Years:', years)
st.write('Principle:', principal)
st.write('Benchmark:', benchmark)
mu += 1; mu2 += 1
st.write(unicodeit.replace('\mu')+':', mu)
st.write(unicodeit.replace('\sigma')+':', sigma)
st.write(unicodeit.replace('\mu_2')+':', mu2)
st.write(unicodeit.replace('\sigma_2')+':', sigma2)

# unicodeit seems to only support x and numbers as subscript, not Z.
# Can use '<sub>Z</sub>' in st.write() with unsafe_allow_html=True
# or '$_Z$'.
#st.write(unicodeit.replace('\mu')+'<sub>Z</sub>:', get_mu(mu, sigma),
#         unsafe_allow_html=True)
st.write('$\mu_Z$:', get_mu(mu, sigma))
#st.html(unicodeit.replace('\sigma')+'<sub>Z</sub>:' + str(get_sig(mu, sigma)))
st.write('$\sigma_Z$:', get_sig(mu, sigma))
st.write('$\mu_{Z_2}$:', get_mu(mu2, sigma2))
st.write('$\sigma_{Z_2}$:', get_sig(mu2, sigma2))

st.write('Expected outcomes for strats 1 and 2:', mu**years, mu2**years)

tstart = time()
# Try a checkbox to indicate if input is mu, sigma of norm, lognorm, or mu* sig*
# self.summary = summarize() prints results?
strat1 = Strat(mu, sigma, years, principal)
strat2 = Strat(mu2, sigma2, years, principal)

st.write('got strats')
st.write(time() - tstart); tstart = time()

compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
# have to edit print commands
st.write('done compare')
st.write(time() - tstart); tstart = time()

st.write('pdf')
fig, ax = plt.subplots()
strats = [strat1.roi_dstr, strat2.roi_dstr]
ax.hist(strats, 15 * int(strat1.years**0.5), 
        density=True, 
        label=[strat1.label, strat2.label])
# for pdf
#x = np.linspace(min(strats[0]), max(strats[0]), 1000)
#ax.vlines(benchmark, 0, color='black', linestyles='--', label='Benchmark')
# TODO param show_benchmark T/F
ax.axvline(x=benchmark, color='black', ls='--', 
           label='benchmark = ' + str(round(benchmark, 2)))
ax.set_title('PDF')
ax.set_xlabel('Amount')
ax.legend()
st.pyplot(fig)

st.write(time() - tstart); tstart = time()

st.write('cdf')
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
ax.vlines(benchmark, 0, 1, color='black', linestyles='--',
          label='benchmark = ' + str(round(benchmark, 2)))
ax.legend()
st.pyplot(fig)

st.write(time() - tstart); tstart = time()

st.write('dstr_over_time plot')
# Note: we set this to 15 years because the graph may look silly otherwise
st.pyplot(strat1.dstr_over_time(years=15, normalize=True))
strat1.recalc(years)
# Can try executing recalc in dstr func call, or find out how to rerun otherwise.
# time set doesn't really matter for this graph
st.write(time() - tstart); tstart = time()

st.write('yearly compare plot')
# TODO button to flip A and B strats (show P(A>B) or P(B>A))
# TODO in yearly_plot func, automatically set P(S>S') where S is strat with
# either higher expected val or higher std. Also name strats/params consistently
# (e.g., mu_A, mu_B)
# TODO yearly_plot (compare) and dstr_over_time (single spread) could be made to
# depend on years, or can be created just once with no need to change if
# different years is chosen. Maybe should be moved to bottom instead of top?
yearly_plot(strat1, strat2, stop=30, step=3)
# Need to run recalc?
strat1.recalc(years)
strat2.recalc(years)
# TODO this plot is slow! leave it last, or change the implementation.
st.write(time() - tstart); tstart = time()

