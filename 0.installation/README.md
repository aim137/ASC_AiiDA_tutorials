# ASC AiiDA installation guide

## Install Anaconda

If you haven’t already, install anaconda from [here](https://docs.anaconda.com/anaconda/install/mac-os/) - I’d recommend the graphical installer.
Please note the following warning before proceeding:

:warning: Do NOT change mac’s default python Mac has python 2.7 by default and this should not be changed. Aiida requires the default to be ≥ 3.7. This is the reason why we’ll install Aiida inside a Conda environment where python3 is the default, leaving the rest of your computer unchanged. 

## Install and setup AiiDA

Instructions to install AiiDA via a Conda environment can be found [here](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_conda.html). Continue with the instructions in the section ‘Setup profile’.

After finishing this, you can check tne output of `verdi status` - you should get 5 successful tests. If you get a `ConnectionError` in `rabbitmq`, you'll need to add a line to your `/etc/hosts` file. 

🔴 Very carefully and making sure you don't change anything else but adding this one line,
- open the file with superuser permissions, e.g., `sudo nano /etc/hosts`
- add a last line containing your computer number, e.g., `127.0.0.1  mp144126`
- save the file
- issue the command `reentry scan`
- try `verdi status` again

### AiiDA Plugins

Install the Quantum Espresso plugin by issuing the command `pip install aiida-quantumespresso`. More information [here](https://aiida-quantumespresso.readthedocs.io/en/latest/). You can test this worked with `verdi plugin list`.

Install the aiida-pseudo plugin by issuing the command `pip install aiida-pseudo`. More information [here](https://aiida-pseudo.readthedocs.io/en/latest/).

Then, install the standard solid-state pseudopotentials family ([SSSP](https://www.materialscloud.org/discover/sssp/table/efficiency)) with the command `aiida-pseudo install sssp`. 

### Setup ssh open connection to Lobster
AiiDA and 2FA are not very close friends for reasons that will become clear later on - for now, we need to find a way to circumvent 2FA.

- If you haven't already, start an agent with `$(eval-agent -s)`
- add Lobster key with `ssh-add -l ~/.ssh/my_lobster_key`
- edit the `~/.ssh/config` file, it should look like
```
Host lobster
    Hostname lobster.phy.qub.ac.uk
    User my_username
    IdentityFile ~/.ssh/my_lobster_key
    ServerAliveInterval 120
    ControlPath ~/.ssh/controlpaths/%C
    ProxyJump titus
    LocalForward 2222 localhost:22
Host lobster_aiida
    Hostname localhost
    User my_username
    Port 2222
```
- log in to Lobster with `ssh lobster` using 2FA and leave that connection open

### Setup computer and code
Finally, set up a `computer` and a `code` in AiiDA. Read the generic instructions here to understand what this is about and how to use `.yml` files. 
After doing that, use instructions tailored to Lobster (our `computer`) in the files `computer.yml` provided in `1aiida_configfiles`. Our `code` will be `pw.x`, the Quantum Espresso executable for plane-wave DFT calculations. Use the file `code.yml` provided in `1aiida_configfiles`.

Make sure you edit the `.yml` files, changing the paths to files in your computer and cluster. 

- go to `1aiida_configfiles/1Lobster`
- type in `verdi computer setup --config computer.yml`
- type in `verdi computer configure ssh HPC_Lobster`
  - use defaults except for Username (use your Lobster username) and Port number (use 2222)
- type in `verdi code setup --config 1code_pw.x/code.yml`

