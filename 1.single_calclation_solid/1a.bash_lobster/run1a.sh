#!/bin/bash
#SBATCH --no-requeue
#SBATCH --job-name="tuto1a"
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --ntasks-per-node=28
                    CORES=28

module purge
module load qe

INPUT=pw_scf.in

mpirun -n $CORES pw.x -inp $INPUT > stdout


#Continue this script in the following way

#Parse the output to obtain the final energy - use `grep` and `awk`

#Run a relaxation of the previous calculation

#Parse the new output to obtain the final energy

#Output a 'summary.txt' file where the following is printed
#Final Energy of the scf calculation in eV
#Final energy of the relaxation in eV
#Difference in meV
