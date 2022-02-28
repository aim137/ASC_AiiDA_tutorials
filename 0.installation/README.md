#ASC Aiida installation guide – Conda environment

##Install Anaconda

If you haven’t already, install anaconda from [here] (I’d recommend the graphical installer).
Please note the following warning before proceeding:
-Do not change mac’s default python. Mac has python 2.7 by default and this should not be changed. Aiida requires the default to be ≥ 3.7. This is the reason why we’ll install Aiida inside a Conda environment where python3 is the default, leaving the rest of your computer unchanged. 

##Install Aiida

Instructions to install Aiida via a Conda environment can be found here.

Continue with the instructions in the section ‘Setup profile’.

Install the Quantum Espresso plugin

Finally, set up a computer and a code in AiiDA. Read the generic instructions here to understand what this is about. 
After doing that, use instructions tailored to Lobster (our computer) in the files computer.yml provided in 1aiida_configfiles. Make sure you change paths to files in your computer and cluster. 
Our code will be pw.x, the Quantum Espresso executable for plane-wave DFT calculations. Use the file code.yml provided in 1aiida_configfiles.
