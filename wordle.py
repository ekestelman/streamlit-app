import streamlit as st
#from wordle_lib.wordle_solver import *
import random
import time
import wordle_lib.solver

# this program needs has a lot of modules which will make the directory messy,
# so I may try it later

st.markdown('For a given solution and initial guess, this program tries to solve the \
          Wordle puzzle! It is not a knockoff of the game&mdash;you have to choose the \
          initial guess _and_ the solution. It just shows a sequence of guesses that \
          can be made. \
          \n\nWhen the program runs, it shows the guesses it makes, and the information \
          gathered through each guess. The output shown is not very clear, and I may fix \
          this some day! But for now I think it is still fun to use.')

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
ans = st.text_input(label='Solution', value=st.session_state.ans)
st.button(label='randomize', key='rand_ans', on_click=update_input, args=['ans'])

first = st.text_input(label='Starting guess', value=st.session_state.first)
st.button(label='randomize', key='rand_first', on_click=update_input, args=['first'])

st.write(first, '->', ans)

wordle_lib.solver.solve(ans, first=first, show=True)

