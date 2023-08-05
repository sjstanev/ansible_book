### Change python command to start python3
   sudo apt install python-is-python3

### Add python3-vent module
   sudo apt install python3-venv

### Create virtual env and set prompt to "Ansible"
   python -m venv .venv --prompt "Ansible"

### Activate venv
   source .venv/bin/activate

### Enter 'deactivate' to leave virtula environment

### Upgrade your pip by running:
   python -m pip install --upgrade pip

### Can test module ping 
   ansible nginx -i inventory/inventory.ini -m ping

### If you create ansible.cfg file for example:
   # [defaults]
   # inventory = inventory/inventory.ini
   # stdout_callback = yaml
   # callback_enable = timer

   ansible nginx -m ping

### You can execute arbitrary commands with the 'command' module
### If you want tou pass an argument to module with the '-a' flag
   ansible nginx -m command -a uptime

### If you need privileged access, pass in the -b or --become flag

    # -k, --ask-pass: ask for connection password
    # -K, --ask-become-pass: ask for privilege escalation password

   ansible nginx -b -K -a "tail /var/log/dmesg" 

### You can install Midnight Commander on Ubuntu by using the following command:
   ansible nginx -b -K -m package -a name=mc

### Use Dockerfile and docker-compose.yml file to create virtual environment
   docker-compose up -d

### you can use yamllint to find typos in YAML that you won’t find when you use the string format.
   yamllint <playbook.yml>

### Ansible ships with the ansible-doc command-line tool
   ansible-doc <module-name>


### Plays
'''
Looking at the YAML, it should be clear that a playbook is a list of dictionaries. 
Specifically, a playbook is a list of plays.
Think of a play as the thing that connects to a group of hosts and a list of things to do on those hosts for you. 
'''

### Modules

'''
Modules are scripts that come packaged with Ansible and perform some kind of action on a host. 
That’s a pretty generic description, but there is enormous variety among Ansible modules. 
Recall from Chapter 1 that Ansible executes a task on a host by generating a custom script based on the module name and arguments, 
and then copies this script to the host and runs it.
'''