from aiida import orm
from aiida.orm.nodes.data.upf import get_pseudos_from_structure
from aiida.engine import run,submit, calcfunction, workfunction
from aiida.plugins import DataFactory
from aiida.plugins import CalculationFactory
from aiida.orm import Code, Dict, Float, Int
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

#----------- 3 K-POINT GRID

KpointsData = DataFactory('array.kpoints')
kpoints = KpointsData()
kpoints.set_kpoints_mesh([3,3,1])
aiida_datatype_kpoints = kpoints

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

#Up to here, this is almost exactly what we had in the second tutorial.
#Note that we are not interested in tracking the provenance of the function
#that creates the builder and thus, it is not decorated.
#We are interested in tracking the remaining functions. Then, those that
#create data will be decorated as @calcfunctions. Those that call processes
#will be @workfunctions. Both these functions work with AiiDA data types, e.g., Float)

@calcfunction
def stretch_unit_cell(orig_structure,aiida_factor):
  """
  Function to return a modified structure by stretching it vertically
  Inputs:
  orig_structure: type StructureData; original structure
  factor: type aiida Float; to stretch or compress the z component of LV3
  Returns:
  dictionary of data type Dict containing:
   stretched structure: Aiida structure data type
   vacuum size in A: type Float (not float)
  """
  factor = aiida_factor.value
  newLVs = orig_structure.cell
  newLVs[2][2] *= factor
  vacuum = Float(newLVs[2][2])
  new_structure = StructureData(cell=newLVs)
  for atom in orig_structure.attributes['sites']:
    new_structure.append_atom(position=atom['position'], symbols=atom['kind_name'])
  
  dict_to_return = {'structure':new_structure, 'vacuum':vacuum}
  return dict_to_return

#We are adding a function to process the energies
#We do want this function fo be recorded in the provenance, so
#complete the following decorator
@#complete here
def process_energies(min_factor, max_factor, num_factors,**input_aiida_dictionary):
  """
  Function to analyze the energies and return the minimum factor that keeps the energy
  difference with the last calculation below a certain threshold
  Inputs:
  calcjob node
  Returns:
  dictionary of data type Dict containing:
   dictionary with energies: type Dict (not dict)
   optimum factor: type Float (not float)
  """
  energies = {}
  for calc,result in input_aiida_dictionary.items():
    energies[calc] = result.dict.energy
  last_calc = calc
  calculation_counter = 0 
  for calc in energies.keys():
    calculation_counter += 1
    energies[calc] -= energies[last_calc]

  calculation_counter = 0 
  for calc in energies.keys():
    if (energies[calc] < 0.001): # 1 meV
      #the next line calculates the factor corresponding to the calculation which satisfied the condition in the if statement
      factor_to_return = Float((max_factor.value-min_factor.value)/(num_factors.value-1)*calculation_counter+#complete with min_factor#)
      break
    calculation_counter += 1

  dictionary_to_return = {'Energies':Dict(dict=energies), 'Factor':factor_to_return}
  return dictionary_to_return


@workfunction
def FindVacuumWorkFunction(min_factor=lambda: orm.Float(0.6), max_factor=lambda: orm.Float(1.2), num_factors=lambda: orm.Int(5)):
  """
  Function to run all the calculations with different cells,
  get the results and compare them. Returns a list of dictonaries
  with the relevant data.
  Inputs: 
  min_factor. type Float. default 0.6
  max_factor. type Float. default 1.2
  num_factors. type Int.  default 5
  """

  list_of_factors=[]
  for i in range(num_factors.value):
    new_factor = Float((max_factor.value-min_factor.value)/(num_factors.value-1)*i+min_factor.value)
    list_of_factors.append(new_factor)  

  list_of_results = []
  dictionary_of_calculations = {}
  stretched_structures = {}
  calculation_counter = 0
  for factor in list_of_factors:
    calculation_counter += 1
    
    dictionary_of_results = {}
    returned_dict = stretch_unit_cell(orig_structure=#complete#, aiida_factor=#complete#)
    stretched_structures['calc'+str(calculation_counter)] = returned_dict['structure']
    vacuum = returned_dict['vacuum']
    dictionary_of_results['Vacuum'] = vacuum
 
    builder = setup_builder_for_calculation(aiida_datatype_parameters, 
                                            stretched_structures['calc'+str(calculation_counter)], 
                                            aiida_datatype_kpoints
                                            )
    print(f'Running calculation No. {calculation_counter} out of {len(list_of_factors)} with factor {factor.value}')
    calc_scf = run(builder)
    sleep(10)
    dictionary_of_calculations['calc'+str(calculation_counter)] = calc_scf['output_parameters']
    print(f'Finished calculation No. {calculation_counter}')
 
    dictionary_of_results['Energy'] = calc_scf['output_parameters'].attributes[#complete the key you want from this dict#]
    list_of_results.append(dictionary_of_results)


  aiida_dictionary_of_calculations = Dict(dict=dictionary_of_calculations)
  returned_processed_energies = process_energies(min_factor=min_factor,
                                                 max_factor=max_factor,
                                                 num_factors=num_factors,
                                                 **aiida_dictionary_of_calculations
                                                 )  
  final_factor = returned_processed_energies['Factor']
  final_energies = returned_processed_energies['Energies'].attributes

  #Plot
  x = np.zeros(len(list_of_results))
  y = np.zeros(len(list_of_results))
  for i in range(len(list_of_results)):
    x[i] = list_of_results[i]['Vacuum']
  i = 0
  for calc in final_energies.keys():
    y[i] = final_energies[calc] * 1000
    i += 1
  
  plt.plot(x,y,marker='o')
  plt.xlabel(f'Vacuum [A]')
  plt.ylabel(f'Energy Difference [meV]')
  plt.style.use('ggplot')
  plt.savefig('vacuum_convergence.pdf')
  
  #Report
  with open('summary.txt','w') as file:
   file.write('Vacuum[A]     Energy[meV]    \n')
   for i in range(len(list_of_results)):
     file.write(str(x[i])+'  '+str(y[i])+'  '+'\n')
  
  final_structure = stretch_unit_cell(orig_structure=aiida_datatype_structure, aiida_factor=final_factor)
  return final_structure['structure'] 


### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><
### Execute the WorkFunction

structure_from_now_on = FindVacuumWorkFunction(#complete#)

