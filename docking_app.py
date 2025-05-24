import streamlit as st
import subprocess
import os
import uuid

def run_vina(protein_path, ligand_path, output_path):
    cmd = [
        'vina', 
        '--receptor', protein_path,
        '--ligand', ligand_path,
        '--center_x', '0', '--center_y', '0', '--center_z', '0',
        '--size_x', '20', '--size_y', '20', '--size_z', '20',
        '--out', output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

st.set_page_config(page_title="Simple Docking App")

st.title("🧪 AutoDock Vina Docking")

protein = st.file_uploader("Upload Protein (PDBQT)", type=['pdbqt'])
ligand = st.file_uploader("Upload Ligand (PDBQT)", type=['pdbqt'])

if st.button("Run Docking"):
    if protein and ligand:
        temp_dir = f"tmp_{uuid.uuid4().hex[:8]}"
        os.makedirs(temp_dir, exist_ok=True)

        protein_path = os.path.join(temp_dir, "protein.pdbqt")
        ligand_path = os.path.join(temp_dir, "ligand.pdbqt")
        output_path = os.path.join(temp_dir, "docked.pdbqt")

        with open(protein_path, 'wb') as f:
            f.write(protein.read())
        with open(ligand_path, 'wb') as f:
            f.write(ligand.read())

        st.info("Running docking...")
        stdout, stderr = run_vina(protein_path, ligand_path, output_path)

        st.subheader("Docking Log")
        st.code(stdout if stdout else stderr)

        if os.path.exists(output_path):
            with open(output_path, "rb") as file:
                st.download_button("Download Docked Complex", file, file_name="docked.pdbqt")

        # Clean up temp files (optional)
        # import shutil; shutil.rmtree(temp_di
