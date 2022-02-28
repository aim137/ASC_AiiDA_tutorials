from aiida.engine import run
from aiida.plugins import DataFactory
from aiida.plugins import CalculationFactory
from aiida.orm import Code, Dict
from time import sleep
import numpy as np
from matplotlib import pyplot as plt


#----------- 1 INPUT PARAMETERS

parameters = {
	'CONTROL': {
		'calculation': 'scf',
		'disk_io': 'low',
	},
	'SYSTEM': {
		'ecutwfc': 45.,
		'ecutrho': 350.,
	},
	'ELECTRONS': {
		'conv_thr': 1.e-8,
		'diagonalization': 'cg',
	},
}

#Create abstract class Dict
Dict = DataFactory('dict')
#Create an instance of the class Dict, immediately passing the dictionary 'parameters'
aiida_datatype_parameters = Dict(dict=parameters)

#----------- 2 STRUCTURE

#Create abstract class StructureData
StructureData = DataFactory('structure')
alat = 2.46842 #Angstroms
lattice_vectors = [
                   [alat, 0., 0.], 
                   [-alat/2., 0.8660254*alat, 0.], 
                   [0., 0., 8.]
                  ]
#Create an instance of the class StructureData, immediately passing the list 'lattice_vectors'
aiida_datatype_structure = StructureData(cell=lattice_vectors)
aiida_datatype_structure.append_atom(position=(0., 0., 0.), symbols='C')
aiida_datatype_structure.append_atom(position=(2/3.*lattice_vectors[0][0]+1/3.*lattice_vectors[1][0], 1/3.*lattice_vectors[1][1], 0.), symbols='C')

#----------- 3 PSEUDOPOTENTIALS

pseudos_family = load_group('SSSP/1.1/PBE/efficiency')
aiida_datatype_pseudos = pseudos_family.get_pseudos(structure=aiida_datatype_structure)

#----------- 4 K-POINT GRID

KpointsData = DataFactory('array.kpoints')
kpoints = KpointsData()
kpoints.set_kpoints_mesh([3,3,1])
aiida_datatype_kpoints = kpoints

#Up to here, this is almost exactly what we had in the first tutorial, i.e.,
#we set up the all the necessary inputs for the calculation. In the first
#tutorial, we would add the data generated to the builder. Then, we would
#just run the builder. At variance, here we are storing this data in
#variables called aiida_datatype, which we will use later.

### ############################################################ ### 
### ############################################################ ### 
### ############################################################ ### 
###                                                              ###
### Have a go at programming the functions from scratch          ### 
###                                                              ###
### or                                                           ### 
###                                                              ###
### use complete the blanks in the following                     ### 
###                                                              ###
### ############################################################ ### 
### ############################################################ ### 
### ############################################################ ### 

### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### Define the functions

def setup_builder_for_calculation(_for_builder_parameters, _for_builder_structure, _for_builder_kpoints):
  """
  Function to set up the builder for a single calculation
  Inputs:
  _for_builder_parameters: type Dict; input parameters for pw.x calculation
  _for_builder_structure: type StructureData; structure for pw.x calculation
  _for_builder_parameters: type Dict; input parameters for pw.x calculation
  Returns:
  builder
  """
  code = Code.get_from_string('qe6.7_pw_default@HPC_Lobster')
  builder = code.get_builder()
 
  builder.parameters = _for_builder_parameters
  builder.structure = _for_builder_structure
  builder.kpoints = _for_builder_kpoints

  pseudos_family = load_group('SSSP/1.1/PBE/efficiency')
  builder.pseudos = pseudos_family.get_pseudos(structure=_for_builder_structure)

  builder.metadata.options.queue_name="main"
  builder.metadata.options.resources={
                                     'tot_num_mpiprocs':14,
                                     'num_machines':1,
                                     'num_mpiprocs_per_machine':14,
                                     'num_cores_per_mpiproc':1,
                                     }
  builder.metadata.computer = code.get_remote_computer()
  builder.metadata.options.max_wallclock_seconds = 60*10

  return builder


def stretch_unit_cell(orig_structure,factor):
  """
  Function to return a modified structure by stretching it vertically
  Inputs:
  orig_structure: type StructureData; original structure
  factor: type float; to stretch or compress the z component of LV3
  Returns:
  stretched structure: Aiida structure data type
  vacuum size in A: type float
  """
  newLVs = orig_structure.cell
  newLVs[2][2] *= factor
  new_structure = StructureData(cell=newLVs)
  for atom in orig_structure.attributes['sites']:
    new_structure.append_atom(position=atom['position'], symbols=atom['kind_name'])
  
  return new_structure, newLVs[2][2]


def run_all_calculations(min_factor=0.6,max_factor=1.2,num_factors=5):
  """
  Function to run all the calculations with different cells,
  get the results and compare them. Returns a list of dictonaries
  with the relevant data.
  Inputs: 
  min_factor. type float. default 0.6
  max_factor. type float. default 1.2
  num_factors. type int.  default 5
  Returns: 
  list of dictionaries. the list runs over calculations.
  each dictionary contains the vacuum and energy of the calculation.
  """

  list_of_factors=[]
  for i in range(num_factors):
    new_factor = (max_factor-min_factor)/(num_factors-1)*i+min_factor
    list_of_factors.append(new_factor)

  list_of_results = []
  calculation_counter = 0
  for factor in list_of_factors:
    calculation_counter += 1
    
    dictionary_of_results = {}

    # call the function to generate a new structure
    # complete!

    # store the new vacuum in the dictionay, under the key 'Vacuum'
    dictionary_of_results['Vacuum'] = # complete here!

    # call the function to generate a new builder 
    # complete!

    print(f'Running calculation No. {calculation_counter} out of {len(list_of_factors)} with factor {factor}')
    # Running the builder
    calc_scf = run(builder)
    sleep(100)
    # get the final energy of the calculation and store it in:
    energy = # complete here!
    print(f'Finished calculation No. {calculation_counter} with energy {energy} eV')
 
    # store the retrieved energy in the dictionary, under the key 'Energy'
    # complete!

    # finally appending the dictionary of this run to the list of dictionaries
    list_of_results.append(dictionary_of_results)
  
  return list_of_results
   

### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### Execute the functions

list_of_final_results = run_all_calculations()

### Plot
x = np.zeros(len(list_of_final_results))
y = np.zeros(len(list_of_final_results))
for i in range(len(list_of_final_results)):
  x[i] = list_of_final_results[i]['Vacuum']
  y[i] = (list_of_final_results[i]['Energy']-list_of_final_results[-1]['Energy'])*1000

plt.plot(x,y,marker='o')
plt.xlabel(f'Vacuum [A]')
plt.ylabel(f'Energy Difference [meV]')
plt.style.use('ggplot')
plt.savefig('vacuum_convergence.pdf')

with open('summary.txt','w') as file:
 file.write('Vacuum[A]     Energy[eV]    \n')
 for i in range(len(list_of_final_results)):
   file.write(str(x[i])+'  '+str(y[i])+'  '+'\n')


### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### Check your results:
#list_of_final_results = []
#list_of_final_results.append({'Vacuum':4.8,'Energy':-501.15162505635}) # Units of A and eV
#list_of_final_results.append({'Vacuum':6.0,'Energy':-501.28168186355})
#list_of_final_results.append({'Vacuum':7.2,'Energy':-501.29921919201})
#list_of_final_results.append({'Vacuum':8.4,'Energy':-501.30130031862})
#list_of_final_results.append({'Vacuum':9.6,'Energy':-501.30181951181})
