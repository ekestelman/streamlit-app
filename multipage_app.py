import streamlit as st

#rot = st.Page('risk_over_time.py', title='ROT')

#wordle = st.Page('wordle.py', title='Wordle')

#pg = st.navigation([rot, wordle])

#pg.run()

st.navigation([st.Page('landing_page.py', title='Hello World!',
                       icon=':material/public:'),
               st.Page('risk_over_time.py', title='Risk Over Time',
                       icon=':material/finance_mode:'),
               #st.Page('wordle.py', icon='material/flexwrap'), # or crossword?
               ]).run()
