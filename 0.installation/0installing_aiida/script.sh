#cd to a directory where you want to create a virtual environment
DIR=Aiida_environment
mkdir $DIR
cd $DIR
#create Python environment
python3 -m venv .
#activate the environment
python --version #before activating, this will return 2.7.16
source ./bin/activate #now the environment is activated
python --version #this will now return 3.x.x, whatever 'python3' points to in your mac

