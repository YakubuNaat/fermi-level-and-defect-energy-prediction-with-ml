def enthalpy(h_h,cl_cl,h_cl):
    #h_h is the enthalpy of H-H bond breakage
    #cl_cl is the enthalpy of Cl-Cl bond breakage
    #h_cl is the enthalpy of H-Cl bond formation
    bond_enthalpy= (h_h*0.5 +cl_cl*0.5) - h_cl
    print(f"{bond_enthalpy} kJmol**-1")
enthalpy(432,239,427)