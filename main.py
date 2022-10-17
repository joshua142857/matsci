import mp_api.core.client
from mp_api import MPRester

string = "Al Co Cr Cu Fe Hf Mn Mo Nb Ni Ta Ti W Zr V Mg Re Os Rh Ir Pd Pt Ag Au Zn Cd"
elements = string.split(" ")

mpr = MPRester("NUNc2qkYfekFR1DkxzhKvBCAMVAgOLoF")
try:
    docs = mpr.summary.search(chemsys="Al-Fe",
                              is_stable=True,
                              fields=["material_id", "structure"])
    mp_formula = {doc.material_id:  for doc in docs}
    print(mp_formula)
except mp_api.core.client.MPRestError:
    pass
all_fields = ['builder_meta', 'nsites', 'elements', 'nelements', 'composition', 'composition_reduced', 'formula_pretty', 'formula_anonymous', 'chemsys', 'volume', 'density', 'density_atomic', 'symmetry', 'property_name', 'material_id', 'deprecated', 'deprecation_reasons', 'last_updated', 'origins', 'warnings', 'structure', 'task_ids', 'uncorrected_energy_per_atom', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull', 'is_stable', 'equilibrium_reaction_energy_per_atom', 'decomposes_to', 'chemenv_iupac', 'chemenv_iucr', 'xas', 'grain_boundaries', 'band_gap', 'cbm', 'vbm', 'efermi', 'is_gap_direct', 'is_metal', 'es_source_calc_id', 'bandstructure', 'dos', 'dos_energy_up', 'dos_energy_down', 'is_magnetic', 'ordering', 'total_magnetization', 'total_magnetization_normalized_vol', 'total_magnetization_normalized_formula_units', 'num_magnetic_sites', 'num_unique_magnetic_sites', 'types_of_magnetic_species', 'k_voigt', 'k_reuss', 'k_vrh', 'g_voigt', 'g_reuss', 'g_vrh', 'universal_anisotropy', 'homogeneous_poisson', 'e_total', 'e_ionic', 'e_electronic', 'n', 'e_ij_max', 'weighted_surface_energy_EV_PER_ANG2', 'weighted_surface_energy', 'weighted_work_function', 'surface_anisotropy', 'shape_factor', 'has_reconstructed', 'possible_species', 'has_props', 'theoretical']
