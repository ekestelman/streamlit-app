import streamlit as st
#import rot
import unicodeit
from rot_lib.strats_module import *
from scipy.stats import lognorm
from time import time

tstart = time()

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

#TODO add contents
#st.write('# Welcome to my streamlit app :wave:')
#st.write('This is a place to explore my coding projects.')
st.write('## Investment Risk Over Time :chart:')
st.write('This project is for comparing investments of different expected returns and variances. Choose the following parameters, and see the results!')
st.write('Refreshing resets all inputs to defaults. Please wait one second between changing multiple parameters to ensure the program updates correctly. If any text input does not match its slider, please try again.')
st.write('The program works by modeling investment growth using geometric Brownian motion (GBM). The assumption is that returns are lognormally distributed. This may not always be a good assumption! This tool is meant to be fun, and aid (or challenge) our intuition about probability. You are responsible for your own financial decisions.')
# probably just need to wait 1 second for input val to update, not for whole
# program to run.
#st.write('Not sure what to input? See here for more details.')
# jump to bottom, or collpsable section?
# or an info button on each input label?

# Changing values later does not change this line
# Make sure that values match supposed inputs!
#st.write(years, principal, benchmark, mu, sigma, mu2, sigma2)

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
# time could be in years, but really just needs to be consistent with time
# unit of other inputs. Consider an explanation section.
years = input_grid[current_row][0].number_input(
        label='Time', # truncates to integer (obvious)
        min_value=1, value=years, key='time_input', on_change=update_inputs,
        args=['time_input'])
years = input_grid[current_row][1].slider(label='', min_value=1, max_value=60, 
        value=years, key='time_slide', on_change=update_inputs,
        args=['time_slide'])
current_row += 1

# XXX Projected growth plot is normalized and does not depend on principal, want to 
# change this?
# CDF is using principal.
principal = input_grid[current_row][0].number_input(label='Principle', # any units
            min_value=0.,
            value=principal,
            step=.1,
            key='principal_input',
            on_change=update_inputs,
            args=('principal_', 'input'))
# Makes more sense to give options in thousands?
# .1 step might represent $100
principal = input_grid[current_row][1].slider(label='',
            min_value=0.,
            max_value=50.,
            value=principal,
            step=.1,
            key='principal_slide',
            on_change=update_inputs,
            args=('principal_', 'slide'))
current_row += 1

# TODO option to exclude benchmark?
benchmark = input_grid[current_row][0].number_input('Benchmark Rate',
            value=benchmark,
            format='%.15g',
            key='bmark_input',
            on_change=update_inputs,
            args=['bmark_input']
            )
benchmark = input_grid[current_row][1].slider(label='',
            min_value=-0.,
            max_value=.5,
            value=benchmark,
            format='%.15g',
            key='bmark_slide',
            on_change=update_inputs,
            args=['bmark_slide']
            )
current_row += 1

yrly_bmark = benchmark  # keep for later
benchmark = (1 + benchmark) ** years * principal

# format = '%.' + [decimal places] + 'g' for 'general' format
# can use min_value and max_value to restrict inputs for number_input
# need key for sliders if labels (and all args) are repeated
mu = input_grid[current_row][0].number_input(label='Investment A: \
     Expected Value',# \
     # + ' (the mean of the lognormal distribution is this input + 1',
     # maybe this should be explained in a footnote?
     value=mu,
     format='%.15g',
     key='mu1_input',
     on_change=update_inputs,
     args=['mu1_input']
     )
# TODO maybe take out the slider label if we also have the text input?
# change slider step now that we have reduced the range?
mu = input_grid[current_row][1].slider(label='',
     min_value=-0.,
     max_value=.3,
     value=mu,
     format='%.15g',
     key='mu1_slide',
     on_change=update_inputs,
     args=['mu1_slide']
     )
current_row += 1
sigma = input_grid[current_row][0].number_input(label='Investment A: \
        Standard Deviation',
        min_value=0.,
        value=sigma,
        format='%.15g',
        key='sig1_input',
        on_change=update_inputs,
        args=['sig1_input']
        )
sigma = input_grid[current_row][1].slider('',
        min_value=0.,
        max_value=.3,
        value=sigma,
        format='%.15g',
        key='sig1_slide',
        on_change=update_inputs,
        args=['sig1_slide']
        )
current_row += 1

mu2 = input_grid[current_row][0].number_input(label='Investment B: \
      Expected Value',
      value=mu2,
      format='%.15g',
      key='mu2_input',
      on_change=update_inputs,
      args=['mu2_input']
      )
mu2 = input_grid[current_row][1].slider(label='',
      min_value=-0.,
      max_value=.3,
      value=mu2,
      format='%.15g',
      key='mu2_slide',
      on_change=update_inputs,
      args=['mu2_slide']
      )
current_row += 1
sigma2 = input_grid[current_row][0].number_input(label='Investment B: \
         Standard Deviation',
         min_value=0.,
         value=sigma2,
         format='%.15g',
         key='sig2_input',
         on_change=update_inputs,
         args=['sig2_input']
         )
sigma2 = input_grid[current_row][1].slider('',
         min_value=0.,
         max_value=.3,
         value=sigma2,
         format='%.15g',
         key='sig2_slide',
         on_change=update_inputs,
         args=['sig2_slide']
         )
current_row += 1

with st.expander('Debug Outputs'):
  st.write('loading time?', round(time() - tstart, 3))
  st.write('This section just shows some of the parameters, which is useful to check that things are working properly. You may ignore this section.')
  st.write('Years:', years)
  st.write('Principle:', principal)
  st.write('Yearly Bmark:', yrly_bmark)
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

st.write('The following are the theoretical expected values. '
         'The rest of the program uses Monte Carlo methods. '
         'Check back for updates that replace simulated results '
         'with analytical results.')
st.write('Expected outcome for investment A:', round(principal*mu**years, 2))
st.write('Expected outcome for invesmtnet B:', round(principal*mu2**years, 2))

tstart = time()
# Try a checkbox to indicate if input is mu, sigma of norm, lognorm, or mu* sig*
# self.summary = summarize() prints results?
strat1 = Strat(mu, sigma, years, principal)
strat2 = Strat(mu2, sigma2, years, principal)

#st.write('got strats')
#st.write(time() - tstart); tstart = time()

st.write('### Summary of Investments A and B')
compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
# have to edit print commands
#st.write('done compare')
#st.write(time() - tstart);
tstart = time()

st.write(f'### Probability Density Function at Time $t = {years}$')
#st.info('**Note:** Probability density is based on the bars shown, not the total data.', icon=':material/info:')
fig, ax = plt.subplots()
#strats = [strat1.roi_dstr, strat2.roi_dstr]
# including range param ignores outliers, maybe this makes density less accurate?
# may not be a big deal
# ^maybe this is misleading for very large sig on one strat?
# Can we just use xlim instead of range?
# TODO use median and geometric std. Should be * not +
#st.write(strat1.mu_star, strat1.sig_star)
#st.write(strat2.mu_star, strat2.sig_star)
#stds = 3  # number of standard deviations to include
#hist_max = max(strat1.mu_star + strat1.sig_star * stds,
#               strat2.mu_star + strat2.sig_star * stds)
q = .90  # cutoff quantil for hist
hist_max = max(#np.quantile(strat1.roi_dstr, q),
               #np.quantile(strat2.roi_dstr, q),
               np.median(strat1.roi_dstr) * 3,
               np.median(strat2.roi_dstr) * 3,
               )
#maximum = max(max(strat1.roi_dstr), max(strat2.roi_dstr))
#nbins = int(maximum / hist_max * 50) results in way too many bins, too slow.
#st.write(nbins, '=', maximum, '/', hist_max, '* 50')
npts = len(strat1.roi_dstr) # assume both strats have some sampling size
factor = 1  # for testing how weights work
nbins = 40 * factor
bins = np.linspace(0, hist_max * factor, nbins+1)
weights = [[1 / (npts * (bins[1] - bins[0])) for _ in range(npts)] \
           for __ in range(2)]
# XXX changing whether hist uses density or weights seems to affect cdf too??
# Why does density=True result in lower density numbers?
# Expectation: density=True only accounts for data in bins, so numbers should
# be inflated.#
ax.hist([strat1.roi_dstr, strat2.roi_dstr],
        #bins=15 * int(strat1.years**0.5),
        #bins=np.linspace(0, hist_max, 3), # eqv to assigning bins and range
        #bins=2*9,
        bins=bins,
        #bins = nbins,
        #range=(0, hist_max*9),
        # manually normalize so that density can relfect total data
        # weights does not seem to be working as intended
        # These weights result in sum of all heights = 1
        #weights = [[1 / (npts * (bins[1] - bins[0])) for _ in range(npts)] \
        #           for __ in range(2)],
        #weights = [[1 / npts for _ in range(npts)],
        #           [1 / npts for _ in range(npts)]],
        # For PDF, sum of all heights * widths = 1
        weights=weights,
        #density=True,
        label=[strat1.label, strat2.label])
# for pdf
#x = np.linspace(min(strats[0]), max(strats[0]), 1000)
#ax.vlines(benchmark, 0, color='black', linestyles='--', label='Benchmark')
# TODO param show_benchmark T/F
ax.axvline(x=benchmark, color='black', ls='--', 
           #label='benchmark = ' + str(round(benchmark, 2)))
           #label=f'benchmark = {yrly_bmark}')
           #label=f'${bmark_yrly}^{years}=$' + str(round(benchmark, 2)))
           label=f'${principal} \cdot {1+yrly_bmark}^{{{years}}} = '
                 f'{round(benchmark, 2)}$')
           # If we want a label like this, we might also want it to account for
           # principle.
ax.set_title('PDF')
ax.set_xlabel('Amount')
ax.set_ylabel('Probability Density')
ax.set_xlim(0, hist_max)
ax.legend()
st.pyplot(fig)

st.write(round(time() - tstart, 3)); tstart = time()

st.write(f'### Complement of Cumulative Distribution Function at Time '
         f'$t = {years}$')
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
#ax.vlines(benchmark, 0, 1, color='black', linestyles='--',
ax.axvline(benchmark, 0, 1, color='black', ls='--',
          #label='benchmark = ' + str(round(benchmark, 2)))
          #label=f'benchmark = {yrly_bmark}')
          # TODO omit principle coefficient if 1?
          label=f'${principal} \cdot {1+yrly_bmark}^{{{years}}} = '
                f'{round(benchmark, 2)}$')
ax.set_ylim(0, 1)
ax.set_xlim(0, hist_max)
ax.legend()
st.pyplot(fig)

st.write(round(time() - tstart, 3)); tstart = time()

st.write('### Projected Returns Over Time')
if 0:
  # show two plots side by side
  dot_plot_grid = st.columns([1, 1]) # [1,1] is relative width of 2 cols
  dot_plot_grid[0].pyplot(strat1.dstr_over_time(years=15, normalize=False))
  dot_plot_grid[1].pyplot(strat2.dstr_over_time(years=15, normalize=False))
  strat1.recalc(years)
  strat2.recalc(years)
# Note: we set this to 15 years because the graph may look silly otherwise
# May still look good if we use a smaller interval...
# set interval with input? currently hardcoded in strats_module
else:
  # show only one plot, or both in series
  st.pyplot(strat1.dstr_over_time(years=15, normalize=False))
  strat1.recalc(years)
  st.pyplot(strat2.dstr_over_time(years=15, normalize=False, alt_colo=True))
  strat2.recalc(years)
# Can try executing recalc in dstr func call, or find out how to rerun otherwise.
# time set doesn't really matter for this graph
st.write(round(time() - tstart, 3)); tstart = time()

st.write('### Comparison Over Time')
# TODO button to flip A and B strats (show P(A>B) or P(B>A))
# TODO in yearly_plot func, automatically set P(S>S') where S is strat with
# either higher expected val or higher std. Also name strats/params consistently
# (e.g., mu_A, mu_B)
# TODO yearly_plot (compare) and dstr_over_time (single spread) could be made to
# depend on years, or can be created just once with no need to change if
# different years is chosen. Maybe should be moved to bottom instead of top?
yearly_plot(strat1, strat2, stop=30, step=1)
# Need to run recalc?
strat1.recalc(years)
strat2.recalc(years)
# TODO this plot is slow! leave it last, or change the implementation.
st.write(round(time() - tstart, 3)); tstart = time()

