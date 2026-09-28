from pymatgen.ext.matproj import MPRester
from pymatgen.analysis.piezo import PiezoelectricTensor
from pymatgen.symmetry.analyzer import SpacegroupAnalyze
api_key ="JSNhVwG6Nf4t5POzLrhz9pxB3GD6h1xZ"
mpr = MPRester(api_key)
# Query criteria for perovskite structures
query_criteria = {
    'elements': {'$all': ['A', 'B', 'O']},  # Replace 'A', 'B' with actual elements you're interested in
    'nelements': 3,  # Number of elements in the formula
    'anonymous_formula': {'A': 1, 'B': 1, 'O': 3}  # General ABX3 formula
}

# Properties to extract
property= [
    'structure', 'material_id', 'formula_pretty', 'band_gap', 'e_above_hull', 'density',
    'dos', 'bandstructure', 'fermi_level', 'effective_masses', 'formation_energy_per_atom',
    'dielectric', 'piezoelectric', 'ferroelectric','elasticity','thermal_properties']

# Query the database
mpr= MPRester(api_key)
    results = mpr.summary.search(criteria=query_criteria, properties=property)

# Filter and save perovskite structures and properties
for result in results:
    structure = result['structure']
    material_id = result['material_id']
    formula = result['formula_pretty']
    band_gap = result['band_gap']
    e_above_hull = result['e_above_hull']
    density = result['density']
    dos = result.get('dos')
    bandstructure = result.get('bandstructure')
    fermi_level = result.get('fermi_level')
    effective_masses = result.get('effective_masses')
    formation_energy = result.get('formation_energy_per_atom')
    dielectric = result.get('dielectric')
    piezoelectric = result.get('piezoelectric')
    ferroelectric = result.get('ferroelectric')

    # Extract mechanical properties
    elasticity = result.get('elasticity')
    if elasticity:
        bulk_modulus = elasticity.get('K_VRH')  # Bulk modulus
        shear_modulus = elasticity.get('G_VRH')  # Shear modulus

    # Extract thermal properties
    thermal_properties = result.get('thermal_properties')
    if thermal_properties:
        thermal_expansion = thermal_properties.get('thermal_expansion_300K')  # Thermal expansion coefficient
        specific_heat = thermal_properties.get('heat_capacity')  # Specific heat capacity

    # Save structure to a file (e.g., CIF format)
    structure.to(filename=f'{formula}.cif')

    # Print extracted properties
    print(f'Material ID: {material_id}')
    print(f'Formula: {formula}')
    print(f'Band Gap: {band_gap} eV')
    print(f'Energy Above Hull: {e_above_hull} eV/atom')
    print(f'Density: {density} g/cm^3')
    print(f'DOS: {dos}')
    print(f'Band Structure: {bandstructure}')
    print(f'Fermi Level: {fermi_level} eV')
    print(f'Effective Masses: {effective_masses}')
    print(f'Formation Energy: {formation_energy} eV/atom')
    print(f'Dielectric: {dielectric}')
    print(f'Piezoelectric: {piezoelectric}')
    print(f'Ferroelectric: {ferroelectric}')

    # Print mechanical properties
    if elasticity:
        print(f'Bulk Modulus: {bulk_modulus} GPa')
        print(f'Shear Modulus: {shear_modulus} GPa')
    # Print thermal properties
    if thermal_properties:
        print(f'Thermal Expansion Coefficient (300K): {thermal_expansion} /K')
        print(f'Specific Heat Capacity: {specific_heat} J/(g*K)')

    print()
print(f'Extracted {len(results)} perovskite structures.')