from aiida.orm.nodes.data.upf import get_pseudos_from_structure
from aiida.orm.computers import Computer
from aiida.engine import submit
from aiida.plugins import DataFactory
from aiida.plugins import CalculationFactory
from aiida.orm import Code
from aiida.orm import Dict
from time import sleep


#----------- 0 GET CODE

code = Code.get_from_string('qe6.7_pw_default@HPC_Lobster')
builder = code.get_builder()

#----------- 1 INPUT PARAMETERS

parameters = {
	'CONTROL': {
		'calculation': 'scf',
		'disk_io': 'low',
	},
	'SYSTEM': {
		'ecutwfc': 15.,
		'ecutrho': 120.,
		'nbnd'   : 10,
		'ibrav'  : 2,
	},
	'ELECTRONS': {
		'conv_thr': 1.e-6,
	},
}

#Create abstract class Dict
Dict = DataFactory('dict')
#Create an instance of the class Dict, immediately passing the dictionary 'parameters'
builder.parameters = Dict(dict=parameters)

#----------- 2 STRUCTURE

#Create abstract class StructureData
StructureData = DataFactory('structure')
alat = 5.431 #Angstroms
lattice_vectors = [
[-alat/2. , 0.00000 , alat/2.], 
[0.000000 , alat/2. , alat/2.], 
[-alat/2. , alat/2. , 0.00000]
]
#Create an instance of the class StructureData, immediately passing the list 'lattice_vectors'
structure = StructureData(cell=lattice_vectors)
structure.append_atom(position=(0., 0., 0.), symbols='Si')
structure.append_atom(position=(0.25*alat, 0.25*alat, 0.25*alat), symbols='Si')

builder.structure = structure

#----------- 3 PSEUDOPOTENTIALS

builder.pseudos = get_pseudos_from_structure(structure, 'SSSP_eff')

#----------- 4 K-POINT GRID

KpointsData = DataFactory('array.kpoints')
kpoints = KpointsData()
kpoints.set_kpoints_mesh([2,2,2])
builder.kpoints = kpoints

#----------- 5 COMPUTER OPTIONS

builder.metadata.options.queue_name="main"
builder.metadata.options.resources={
                                   'tot_num_mpiprocs':28,
                                   'num_machines':1,
                                   'num_mpiprocs_per_machine':28,
                                   'num_cores_per_mpiproc':1,
                                   }
builder.metadata.computer = code.get_remote_computer()
builder.metadata.options.max_wallclock_seconds = 60*10

#calcjob is the calculation node
calc_scf = submit(builder)


#Continue this script in the following way

#Run a relaxation of the previous calculation

#Wait for both calculations to finish

#Output a 'summary.txt' file where the following is printed
#Final Energy of the scf calculation in eV
#Final energy of the relaxation in eV
#Difference in meV
