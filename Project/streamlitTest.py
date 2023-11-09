import streamlit as st

st.title('streamlit test')
video_url = st.text_input('paste URL')

if st.button('start analysis'):
    if video_url:
        #analysis
        st.text('yay u pasted a URL good job buds')
        st.text(video_url)
        #show outcome
    else:
        st.warning('u didnt paste a URL >:/')