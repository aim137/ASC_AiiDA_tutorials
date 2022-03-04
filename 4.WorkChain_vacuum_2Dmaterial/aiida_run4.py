from aiida import orm
from aiida.orm.nodes.data.upf import get_pseudos_from_structure
from aiida.engine import run,submit, calcfunction, workfunction
from aiida.plugins import DataFactory
from aiida.plugins import CalculationFactory
from aiida.orm import Code, Dict, Float, Int
import os
os.system('cp find_vacuum_work_chain.py #complete path_to_anaconda_python#/python3.8/site-packages/aim')
os.system('verdi daemon restart --reset')
from aim.find_vacuum_work_chain import FindVacuumWorkChain


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

#After defining the parameters of our material (pw.x parameters, structure and k-points)
#we instantiate the workchain and submit it in the same step.

submit(FindVacuumWorkChain,
       parameters  = aiida_datatype_parameters,
       structure   = aiida_datatype_structure,
       k_points    = aiida_datatype_kpoints,
       min_factor  = #complete with 0.6#,
       max_factor  = #complete with 1.2#,
       num_factors = Int(5)
       )
