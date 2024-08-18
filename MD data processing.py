'''
Need to ensure you have numpy and matplotlib installed
Changed the folder_path in this program to the one with all following result files
Ensure that the MSD results start with "msd_"
Ensure that the RDF results end with ".rdf"
Ensure that the SAC result's name is "Sauto.dat"
Ensure that the polymer's trajectory file's name is chain_after.lammpstrj
'''


import MD_MSD
import MD_RDF
import MD_RG
import MD_SAC
import MD_E2E
import os

# to be changed
list_folder_path = ['Resources/MD data/n5_repulsive/100f', 'Resources/MD data/n5_repulsive/150f', 'Resources/MD data/n5_repulsive/200f']
folder_path = 'Resources/MD data/end sticky with tests'

'''
if not os.path.exists(folder_path + "/Graphs"):
    os.chdir(folder_path)
    new_folder = "Graphs"
    os.makedirs(new_folder)
    
#MD_MSD.analyze_msd(folder_path)
#MD_RDF.analyze_rdf(folder_path)
#MD_RG.analyze_rg(folder_path)
#MD_SAC.analyze_sac(folder_path)
MD_SAC.analyze_multiple_sac()
#MD_RG.analyze_multiple_rg()
#MD_E2E.analyze_e2e(folder_path)
'''

