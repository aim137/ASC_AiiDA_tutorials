# Tutorial 1 - Parsing

In this tutorial, we will use Quantum Espresso to calculate the energy of Silicon bulk. First, we will calculate the energy of a given structure (see input file included in the assignment). We will then ask QE to optimise the structure and obtain a new (lower) energy. Finally, we will compare those energies and print the difference.
This must be done in a single script that executes all steps from start to finish. In the first part of the tutorial, it will be a bash script that will run on an HPC cluster (Young or Lobster). In the second part, we’ll write an Aiida script that runs in your local computer, making use of the same HPC cluster as before.


🔴 **Bear in mind that the script must work from start to finish without any user intervention. That’s the whole point.** 

We’ll compare how easy is to do that in either bash or Aiida.

## Part A - Bash

In this part of the tutorial, you will run calculations in Lobster, without using Aiida. You will first run a single-point calculation, where neither the size of the cell nor position of the atoms are changed.
1. Run the calculation included in the assignment 
  - See directory `1a.bash_lobster`
    - This includes everything that is required for this first run, i.e., a minimal bash script, the QE input file and the pseudopotential.
  - Copy all files in `1a.bash_lobster` to the cluster.
  - Log in to the cluster and submit the calculation – work in the scratch directory.
  - Read the output file.
2. Extend the script provided in order to
  - Parse the output to get the final energy
    - Hint: use the `grep` command to get the line where the energy is and pipe it (“|”) to `awk` to get the right column.
  - Run a second QE calculation 
    - a relaxation instead of a single-point calculation 
    - The script must edit the input file, changing `scf` to `vc-relax`.
      - use the `sed` command to achieve this
  - Parse both output files in order to get the final energy in each case
  - Calculate the energy difference
  - Print out a file reporting
    - Energy of first run in eV
    - Energy of second run in eV
    - Energy difference in meV


## Part B - AiiDA

In this part, follow the same steps as in part 1, but using AiiDA. A minimal Aiida script can be found in `1b.aiida_lobster`. 
This will run the first (scf) calculation through AiiDA.
You will have to extend that AiiDA script in order to add the same steps as before, i.e., run a new calculation, compare the energies and print out the result.
