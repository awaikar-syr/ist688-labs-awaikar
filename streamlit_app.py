import streamlit as st

st.set_page_config(page_title="Lab manager", page_icon=": material/edit:")

# Show title and description.
st.title("📄 Ankit's LabSpace")
st.write( "Welcome to the Navigation Pane Lab" )


lab1 = st.Page("lab1.py", title="Lab 1")
lab2 = st.Page("lab2.py", title="Lab 2")
lab3 = st.Page("lab3.py", title="Lab 3")
lab4 = st.Page("lab4.py",title="Lab 4", default= True)

pg = st.navigation([lab4, lab3, lab2, lab1])

pg.run ()

