import streamlit as st
import base64

icon = ':wave:'
img_file = 'face_w_transparent_bgd_2.png'
img_file = None
if img_file:
  # Load image from actual image file
  with open(img_file, 'rb') as f:
    icon = base64.b64encode(f.read()).decode()
  st.markdown(f"""
              <h1> Hello, I'm Eial
              <img src='data:image/png;base64,{icon}' height=64em
               style='vertical-align:-14px; margin-left:10px;'>
              </h1>
              """, unsafe_allow_html=True)

elif 1:
  # Load image from encoded and decoded text file
  with open('img_encoding_file', 'r') as f:
    icon = f.read()
  st.markdown(f"""
              <h1> Hello, I'm Eial
              <img src='data:image/png;base64,{icon}' height=64em
               style='vertical-align:-14px; margin-left:10px;'>
              </h1>
              """, unsafe_allow_html=True)

else:
  #st.write('# Welcome to Eial\'s website :wave:')
  #st.write('# Hello there :wave:') # general kenobi
  st.write('# Hello, I\'m  Eial :wave:')
#st.write('My name is Eial. I majored in pure mathematics and minored in astronomy at Stony Brook University. I currently work as a data analyst for the city of New York, and I like to write code for mathematically-oriented projects.')
st.write('This is a place to explore my coding projects. So far I have only \
          included a few, but you can find my other projects on \
          [Github](https://github.com/ekestelman)!')
st.write('View a summary of my projects below, or use the left panel to navigate to one.')

run_badge = '[![Static Badge](https://img.shields.io/badge/%F0%9F%9A%80-Try%20It!-blue)]'

st.write('## Contents')
st.write('1. [Risk Over Time](#risk-over-time)')
st.write('2. [Wordle Solver](#wordle-solver)')

st.write('## Risk Over Time')
st.write(run_badge + '(risk_over_time)')
st.write('In this project, we explore the relationship between investment risk and time \
          scales.')
st.write('Suppose you are choosing between investment A and investment B. Perhaps A is less volatile, but B has higher potential returns. How do you choose between the two?')
st.write('Input the mean and standard deviation of each investment, assuming that the returns are lognormally distributed. Then, we can compare the probability of one outperforming the other as a function of time. We can also compare the probability that either investment outperforms some benchmark within a given time scale.')

st.write('## Wordle Solver')
st.write(run_badge + '(wordle)')
st.write('This program tries to solve the wordle puzzle in as few guesses as possible. \
          It takes as input your first guess and the solution, so it won\'t help you \
          cheat!')
