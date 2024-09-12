import streamlit as st

st.set_page_config(page_title="Lab manager", page_icon=": material/edit:")

# Show title and description.
st.title("📄 Ankit's LabSpace")
st.write( "Welcome to the Navigation Pane Lab" )


lab1 = st.Page("lab1.py", title="Lab 1")
lab2 = st.Page("lab2.py", title="Lab 2", default= True)
lab3 = st.Page("lab3.py", title="Lab 3")


pg = st.navigation([lab3, lab2, lab1])

pg.run ()

