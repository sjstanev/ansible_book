### ansible_book
based on Ansible Up and Running examples

# Change python command to start python3
sudo apt install python-is-python3

# Add python3-vent module
sudo apt install python3-venv

# Create virtual env and set prompt to "Ansible"
python -m venv .venv --prompt "Ansible"

# Activate venv
source .venv/bin/activate

# Enter 'deactivate' to leave virtula environment

# Upgrade your pip by running:
python -m pip install --upgrade pip

# Can test module ping 
ansible nginx -i inventory/inventory.ini -m ping
