import os
import pandas as pd
from gpaw import GPAW, PW, FermiDirac
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import BFGS
import numpy as np

# Input and output folder paths
folder_path = "/home/yabdulai/lustre/naat/dftnaat/structures"
output_path = os.path.join(folder_path, 'Lastoutput')
os.makedirs(output_path, exist_ok=True)

# List of transition metal symbols
transition_metals = [
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"
]

# Lists to store data for CSV
data = {
    "Filename": [],
    "Total Energy (eV)": [],
    "Positions": [],
    "Cell Parameters": [],
    "Local Magnetic Moments": [],
    "Total Magnetic Moment": [],
    "HOMO (eV)": [],
    "LUMO (eV)": [],
    "Fermi Level (eV)": [],
    "Band Gap (eV)": [],
    "Chemical Potential (eV)": [],
    "Work Function (eV)": [],
    "Entropy (eV/K)": [],
    "Free Energy (eV)": [],
}

# Loop through all CIF files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".cif"):
        file_path = os.path.join(folder_path, filename)

        # Read the CIF file
        atoms = read(file_path)

        # Check for transition metals in the structure
        dopant_indices = [atom.index for atom in atoms if atom.symbol in transition_metals]
        if not dopant_indices:
            raise ValueError(f"No transition metal dopant found in {filename}. Calculation cannot proceed.")

        # Apply constraints (keep dopant and carbon dioxide fixed)
        adsorbate_indices = []
        for i, atom in enumerate(atoms):
            if atom.symbol == "C":
                oxygens = [j for j in range(len(atoms)) if atoms[j].symbol == "O" and abs(atoms.get_distance(i, j)) < 1.5]
                if len(oxygens) == 2:
                    adsorbate_indices.extend([i] + oxygens)
                    break
        fixed_indices = dopant_indices + adsorbate_indices
        constraints = FixAtoms(indices=fixed_indices)
        atoms.set_constraint(constraints)

        # Set up the GPAW calculator
        calc = GPAW(
            mode=PW(300),  # Plane wave cutoff energy in eV
            xc="PBE",  # Exchange-correlation functional
            kpts=(1, 1, 1),  # K-point grid
            occupations=FermiDirac(0.1),  # Smearing for electronic occupations
            txt=os.path.join(output_path, f"Energy_{filename}.txt"),
            spinpol=True,  # Enable spin polarization for magnetic moments
        )

        # Attach the calculator to the atoms object
        atoms.calc = calc
        print(f"DFT calculations are in progress for {filename}...")

        # Optimize the structure
        optimizer = BFGS(atoms, logfile=os.path.join(output_path, f"Opt_{filename}.log"))
        optimizer.run(fmax=10)  # Convergence criterion: maximum force < 0.1 eV/Å

        # Save the optimized structure
        optimized_structure_path = os.path.join(output_path, f"Optimized_{filename.replace('.cif', '.xyz')}")
        write(optimized_structure_path, atoms)

        # Extract relevant properties
        total_energy = atoms.get_potential_energy()  # Total energy
        positions = atoms.get_positions().tolist()  # Atomic positions
        cell_parameters = atoms.get_cell().tolist()  # Cell parameters
        local_magnetic_moments = atoms.get_magnetic_moments().tolist()  # Local magnetic moments
        total_magnetic_moment = atoms.get_magnetic_moment()  # Total magnetic moment
        homo, lumo = calc.get_homo_lumo()  # HOMO and LUMO
        efermi = calc.get_fermi_level()  # Fermi level
        bandgap = lumo - homo  # Band gap
        chemical_potential = (lumo + homo) / 2  # Chemical potential

        # Calculate work function
        e_potential = calc.get_electrostatic_potential()
        z = np.linspace(0, atoms.get_cell_lengths_and_angles()[2], len(e_potential))
        vacuum_region_start = int(len(z) * 0.85)
        vacuum_region_end = int(len(z))
        vacuum_potential = np.mean(e_potential[vacuum_region_start:vacuum_region_end])
        work_function = vacuum_potential - efermi

        # Read entropy and free energy from GPAW output file
        gpaw_output_file = os.path.join(output_path, f"Energy_{filename}.txt")
        entropy_st = np.nan
        free_energy = np.nan
        with open(gpaw_output_file, 'r') as file:
            for line in file:
                if "Entropy (-ST):" in line:
                    entropy_st = float(line.split()[-1])
                elif "Free energy:" in line:
                    free_energy = float(line.split()[-1])

        # Calculate entropy
        temperature_eV = 0.03  # Temperature in eV
        entropy = entropy_st / temperature_eV

        # Append data to lists
        data["Filename"].append(filename)
        data["Total Energy (eV)"].append(total_energy)
        data["Positions"].append(positions)
        data["Cell Parameters"].append(cell_parameters)
        data["Local Magnetic Moments"].append(local_magnetic_moments)
        data["Total Magnetic Moment"].append(total_magnetic_moment)
        data["HOMO (eV)"].append(homo)
        data["LUMO (eV)"].append(lumo)
        data["Fermi Level (eV)"].append(efermi)
        data["Band Gap (eV)"].append(bandgap)
        data["Chemical Potential (eV)"].append(chemical_potential)
        data["Work Function (eV)"].append(work_function)
        data["Entropy (eV/K)"].append(entropy)
        data["Free Energy (eV)"].append(free_energy)

        # Clean up the calculator after the calculation
        calc.write(os.path.join(output_path, f"Calc_{filename}.gpw"))

# Create a DataFrame to store the results
df = pd.DataFrame(data)

# Save the results to a CSV file
csv_filename = 'energies.csv'
csv_filepath = os.path.join(output_path, csv_filename)
df.to_csv(csv_filepath, index=False)

print(f"Calculations complete. Results saved to {csv_filepath}.")
