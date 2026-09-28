from pymatgen.core.periodic_table import Element
from pymatgen.analysis.bond_valence import BVAnalyzer
import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.analysis.local_env import VoronoiNN
import numpy as np
from pymatgen.io.cif import CifParser
from io import StringIO

def extract_features_from_cif(structure):
    vnn = VoronoiNN()
    features = []

    # Basic structural features
    features.append(structure.volume)  # Unit cell volume
    features.append(len(structure))    # Number of atoms
    features.append(structure.density) # Density

    # Atomic features
    atomic_numbers = [site.specie.Z for site in structure]
    features.append(np.mean(atomic_numbers))  # Avg atomic number
    features.append(np.std(atomic_numbers))   # Std of atomic numbers

    atomic_radii = [site.specie.atomic_radius for site in structure]
    features.append(np.mean(atomic_radii))    # Avg atomic radius
    features.append(np.std(atomic_radii))     # Std of atomic radii

    # Coordination and bond features
    coordination_numbers = []
    bond_lengths = []

    # Iterate with enumerate to track site index
    for idx, site in enumerate(structure):
        neighbors = vnn.get_nn_info(structure, idx)  # Use idx instead of site.index
        coordination_numbers.append(len(neighbors))
        bond_lengths.extend([neighbor['weight'] for neighbor in neighbors])

    features.append(np.mean(coordination_numbers))  # Avg coordination number
    features.append(np.std(coordination_numbers))   # Std of coordination numbers
    features.append(np.mean(bond_lengths))          # Avg bond length
    features.append(np.std(bond_lengths))           # Std of bond lengths

    print("extract physical",features)

    return features


def extract_chemical_features(structure):
    features = []
    elements = [site.specie.Z for site in structure]
    
    # Number of unique elements
    features.append(len(set(elements)))
    
    # Electronegativity
    electronegativity = [Element.from_Z(Z).X for Z in elements]
    features.extend([np.mean(electronegativity), np.std(electronegativity)])
    
    # Valence electrons (use ns_valence or default to 0)
    valence_electrons = []
    for Z in elements:
        elem = Element.from_Z(Z)
        valence = elem.ns_valence if hasattr(elem, 'ns_valence') else 0
        valence_electrons.append(valence)
    features.append(np.sum(valence_electrons))
    
    # Handle FloatWithUnit by extracting numerical values
    def get_value(prop):
        return prop.value if hasattr(prop, 'value') else prop

    # Van der Waals radii
    vdw_radii = []
    for Z in elements:
        elem = Element.from_Z(Z)
        radius = get_value(elem.van_der_waals_radius) if elem.van_der_waals_radius else np.nan
        vdw_radii.append(radius)
    
    # Thermal conductivity
    thermal_cond = []
    for Z in elements:
        elem = Element.from_Z(Z)
        cond = get_value(elem.thermal_conductivity) if elem.thermal_conductivity else np.nan
        thermal_cond.append(cond)
    
    # Melting points
    melting_pts = []
    for Z in elements:
        elem = Element.from_Z(Z)
        mp = get_value(elem.melting_point) if elem.melting_point else np.nan
        melting_pts.append(mp)
    
    # Append features with NaN handling
    features.extend([
        np.nanmean(vdw_radii), np.nanstd(vdw_radii),
        np.nanmean(thermal_cond), np.nanstd(thermal_cond),
        np.nanmean(melting_pts), np.nanstd(melting_pts)
    ])
    print("chemical features",features)
    return features


def extract_symmetry_features(structure):
    features = []
    
    # Space group information
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    analyzer = SpacegroupAnalyzer(structure)
    space_group = analyzer.get_space_group_number()
    crystal_system = analyzer.get_crystal_system()
    distance_matrix = structure.distance_matrix
    distances = distance_matrix.flatten()
    distances = distances[distances > 0.1]  # Exclude self-distances
    features.append(np.mean(distances))
    features.append(np.std(distances))
    features.append(space_group)
    features.append(crystal_system)  # Encode crystal system as a categorical feature
    print("symmetry features",features)
    
    return features


def parse(cif):
    parser = CifParser(StringIO(cif))
    structure = parser.get_structures()
    structure = structure[0]

def descriptor(cif):
    parser = CifParser(StringIO(cif))
    structure = parser.get_structures()
    structure = structure[0]
    
    # Extract structural features
    structural_features = extract_features_from_cif(structure)
    
    # Extract chemical features
    chemical_features = extract_chemical_features(structure)
    
    # Extract symmetry features
    symmetry_features = extract_symmetry_features(structure)
    
    # Combine all features
    all_features = structural_features + chemical_features + symmetry_features
    
    return all_features
