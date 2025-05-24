import streamlit as st
import py3dmol
import os

st.set_page_config(page_title="Docking App (Demo)", layout="wide")
st.title("Protein-Ligand Docking App (Demo Mode)")

st.markdown("""
### ⚠️ Notice
This app is running in **demo mode on Streamlit Cloud**. Due to system restrictions:
- Real molecular docking is **disabled**.
- You can upload PDBQT files and view them in **3D**.
- For actual docking using AutoDock Vina, run the app **locally** on your computer.

To run locally:
```bash
streamlit run docking_app.py
```
""")

# Upload protein and ligand
col1, col2 = st.columns(2)
with col1:
    protein_file = st.file_uploader("Upload Protein (.pdbqt)", type=["pdbqt"], key="protein")
with col2:
    ligand_file = st.file_uploader("Upload Ligand (.pdbqt)", type=["pdbqt"], key="ligand")

# Display in 3D using py3Dmol
def show_3d_structure(pdbqt_data, title):
    view = py3dmol.view(width=400, height=400)
    view.addModel(pdbqt_data, "pdbqt")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    view.setBackgroundColor("white")
    st.subheader(title)
    st.pydeck_chart(view)

if protein_file:
    st.info("Protein file uploaded successfully.")
    protein_data = protein_file.read().decode("utf-8")
    with st.expander("View Protein (3D)"):
        show_3d_structure(protein_data, "Protein Structure")

if ligand_file:
    st.info("Ligand file uploaded successfully.")
    ligand_data = ligand_file.read().decode("utf-8")
    with st.expander("View Ligand (3D)"):
        show_3d_structure(ligand_data, "Ligand Structure")

# Placeholder for docking
if protein_file and ligand_file:
    st.markdown("---")
    st.header("Docking Simulation")
    st.success("✅ Files are ready. If running locally, this is where docking would start.")
    st.code("""
    vina --receptor protein.pdbqt --ligand ligand.pdbqt \
         --center_x 0 --center_y 0 --center_z 0 \
         --size_x 20 --size_y 20 --size_z 20 --out out.pdbqt
    """, language="bash")
    st.warning("🚫 Real docking is disabled on Streamlit Cloud.")
else:
    st.info("Upload both protein and ligand files to begin.")
