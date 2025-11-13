import streamlit as st
#from wordle_lib.wordle_solver import *
import random
import time
import wordle_lib.solver

st.markdown('## Wordle Solver ⬛🟨🟩')
st.markdown('For a given solution and initial guess, this program tries to solve the \
          Wordle puzzle! It is not a knockoff of the game&mdash;you have to choose the \
          initial guess _and_ the solution. It just shows a sequence of guesses that \
          can be made. \
          \n\nWhen the program runs, it shows the guesses it makes, and the information \
          gathered through each guess. The output shown is not very clear, and I may fix \
          this some day! But for now I think it is still fun to use.')
st.write('For more details on how this program works, please visit the [repository](https://github.com/ekestelman/wordle).') # add link

# are we not using this?
def assign_ans():
  with open('wordle_lib/word_list', 'r') as f:
    wordlist = f.read().split()

  return random.choice(wordlist)

with open('wordle_lib/word_list', 'r') as f:
  #st.write(time.time())  # test if this keeps getting rerun!
  wordlist = f.read().split()

if 'ans' not in st.session_state:
  st.session_state.ans = random.choice(wordlist)

if 'first' not in st.session_state:
  st.session_state.first = 'crane'

def update_input(key):
  # does using callback make us rerun file read?
  # is it so bad if it does?
  st.session_state[key] = random.choice(wordlist)

# TODO restrictions on soln
#st.button(label='randomize', key='rand_first', 
# this is a cool and simple option too
#if st.button(label='randomize', key='rand_ans'):
#  ans = random.choice(wordlist)
ans = st.text_input(label='Solution', value=st.session_state.ans).lower()
st.button(label='randomize', key='rand_ans', on_click=update_input, args=['ans'])

first = st.text_input(label='Starting guess', value=st.session_state.first).lower()
st.button(label='randomize', key='rand_first', on_click=update_input, args=['first'])

# This is good for actual usage, but may be useful to comment out for testing
# (can use made up words to test how code is handling certain situations).
if ans not in wordlist:
  st.write(f'**{ans}** is not in the [word list](https://github.com/ekestelman/wordle/blob/39e412fea5cc09550aeb86fd273933b6894154e6/word_list)! Please choose a different `Solution`.')
else:
  st.write(first, '->', ans)

  wordle_lib.solver.solve(ans, first=first, show=True)

