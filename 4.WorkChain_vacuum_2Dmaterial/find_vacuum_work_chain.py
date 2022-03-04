from aiida.orm.utils import load_group
from aiida.engine import WorkChain, ToContext, calcfunction
from aiida.orm import Code, Dict, Float, Int, StructureData, KpointsData
from aiida.plugins import CalculationFactory
import numpy as np
from matplotlib import pyplot as plt

PwCalculation = CalculationFactory('quantumespresso.pw')

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


@calcfunction
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
      factor_to_return = Float((max_factor.value-min_factor.value)/(num_factors.value-1)*calculation_counter+min_factor.value)
      break
    calculation_counter += 1

  dictionary_to_return = {'Energies':Dict(dict=energies), 'Factor':factor_to_return}
  return dictionary_to_return

def plot_and_summary(vacuum_data,energies_data):

  x = np.zeros(len(energies_data))
  y = np.zeros(len(energies_data))
  i=0
  for _value in vacuum_data.values():
    x[i] = _value
    i += 1
  i = 0
  for _value in energies_data.values():
    y[i] = _value * 1000
    i += 1

  plt.plot(x,y,marker='o')
  plt.xlabel(f'Vacuum [A]')
  plt.ylabel(f'Energy Difference [meV]')
  plt.style.use('ggplot')
  plt.savefig('vacuum_convergence.pdf')
  plt.close()

  #Report
  with open('summary.txt','w') as file:
   file.write('Vacuum[A]     Energy[meV]    \n')
   for i in range(len(energies_data)):
     file.write(str(x[i])+'  '+str(y[i])+'  '+'\n')


#Here we define a sub-class, which inherits from the WorkChain class
class FindVacuumWorkChain(#complete with the class#):
  """ WorkChain to determine the optimum vacuum for a 2D material
  """
  @classmethod
  def define(cls, spec):
    """ define metod """
    super().define(spec)
    spec.input('parameters', valid_type=Dict)
    spec.input('structure', valid_type=#complete data type#)
    spec.input('#complete#', valid_type=KpointsData) #check line 63 of the file aiida_run4.py
    spec.input('min_factor',valid_type=Float)
    spec.input('max_factor',valid_type=#complete data type#)
    spec.input('num_factors',valid_type=Int)
    spec.output('final_structure',valid_type=StructureData)
    spec.outline(
        cls.loop_over_structures,
        cls.process_calculations,
        cls.#complete#, #see the methods defined below and complete
        )
 
  def loop_over_structures(self):

    list_of_factors=[]
    for i in range(self.inputs.num_factors.value):
      new_factor = Float((self.inputs.max_factor.value-self.inputs.min_factor.value)/(self.inputs.num_factors.value-1)*i+self.inputs.min_factor.value)
      list_of_factors.append(new_factor)

    list_of_results = []
    dictionary_of_calculations = {}
    dictionary_of_vacuums = {}
    stretched_structures = {}
    calculation_counter = 0
    for factor in list_of_factors:
      calculation_counter += 1

      returned_dict = stretch_unit_cell(
                                        orig_structure=self.inputs.structure, 
                                        aiida_factor=factor
                                        )
      stretched_structures['calc'+str(calculation_counter)] = returned_dict['structure']
      dictionary_of_vacuums['calc'+str(calculation_counter)] = returned_dict['vacuum']

      builder = setup_builder_for_calculation(self.inputs.parameters,
                                              stretched_structures['calc'+str(calculation_counter)],
                                              self.inputs.k_points
                                              )

      #read the instructions and note this line will submit a job from within the WorkChain
      #complete the method used to submit the builder#
      calc_scf = #comp.lete#(builder)

      dictionary_of_calculations['calc'+str(calculation_counter)] = calc_scf

    self.ctx.vacuums = dictionary_of_vacuums
    return ToContext(**dictionary_of_calculations)


  def process_calculations(self):

    dictionary_of_calculations = {}
    cc = 0
    for i in range(self.inputs.num_factors.value):
      cc += 1 #calculation_counter
      _energy = self.ctx['calc'+str(cc)].get_outgoing().get_node_by_label('output_parameters')
      #_energy = self.ctx.calculations['calc'+str(cc)]['calc'].outputs.output_parameters
      dictionary_of_calculations['calc'+str(cc)] = _energy

    aiida_dictionary_of_calculations = Dict(dict=dictionary_of_calculations)
    returned_processed_energies = process_energies(min_factor=self.inputs.min_factor,
                                                  max_factor=self.inputs.max_factor,
                                                  num_factors=self.inputs.num_factors,
                                                  **aiida_dictionary_of_calculations
                                                  )

    self.ctx.energies = returned_processed_energies['Energies']

    returned_dict = stretch_unit_cell(
                                      orig_structure=self.inputs.structure,
                                      aiida_factor=returned_processed_energies['Factor']
                                      )
    self.out('final_structure', returned_dict['structure'])


  def results(self):
    
    #complete with the dictionary of vacuums previously imported to the context in 
    #the method loop_over_structures
    tmp_dict_vacuums = #complete#.copy()
    #we use the .copy() method of the dictionary to create a copy and store it in tmp_dict_vacuums
    tmp_dict_energies = self.ctx.energies.attributes.copy()
    plot_and_summary(tmp_dict_vacuums,tmp_dict_energies)




