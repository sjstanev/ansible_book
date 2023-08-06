# Ansible

> Use Ansible to manage devices

## Table of Contents

- [Install](#install)
- [Basic Usage](#basic-usage)
- [Inventory](#inventory)
- [Variables and Facts](#variables-and-facts)
---
## Install

Change python command to start python3
   ```sh
   $ sudo apt install python-is-python3
   ```

Add python3-vent module
   ```sh
   $ sudo apt install python3-venv
   ```

Create virtual env and set prompt to "Ansible"
   ```sh
   $ python -m venv .venv --prompt "Ansible"
   ```
Activate venv
   ```sh
   $ source .venv/bin/activate
   ```
Enter 'deactivate' to leave virtula environment
Upgrade your pip by running:
   ```sh
   $ python -m pip install --upgrade pip
   ```
You can test module ping by entring:
   ```sh
   $ ansible nginx -i inventory/inventory.ini -m ping
   ```
If you create ansible.cfg file for example:

   ```
      [defaults]
      inventory = inventory/inventory.ini
      stdout_callback = yaml
      callback_enable = timer
   ```
   ```sh
   $ ansible nginx -m ping
   ```
You can execute arbitrary commands with the `command` module
If you want tou pass an argument to module with the '-a' flag
   ```sh
   $ ansible nginx -m command -a uptime
   ```
If you need privileged access, pass in the `-b` or `--become` flag

    # -k, --ask-pass: ask for connection password
    # -K, --ask-become-pass: ask for privilege escalation password

   ```sh
   $ ansible nginx -b -K -a "tail /var/log/dmesg" 
   ```
You can install Midnight Commander on Ubuntu by using the following command:
   ```sh
   $ ansible nginx -b -K -m package -a name=mc
   ```
Use `Dockerfile` and `docker-compose.yml` file to create virtual environment
   ```sh
   $ docker-compose up -d
   ```
you can use yamllint to find typos in YAML that you won’t find when you use the string format.
   ```sh
   $ yamllint <playbook.yml>
   ```
Ansible ships with the ansible-doc command-line tool
   ```sh
   $ ansible-doc <module-name>
   ```
Generating TLS Certificate
   ```sh
   $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -subj /CN=target1 \
     -keyout files/nginx.key -out files/nginx.crt
   ```
---
## Basic Usage

- [Playbook](#Playbook)
- [Plays](#Plays)
- [Modules](#Modules)
- [Variables](#Variables)
- [Loops](#Loops)
- [Handlers](#Handlers)
- [Testing](#Testing)
- [Validation](#Validation)

* **Playbook**

![Playbook](https://github.com/sjstanev/ansible_book/blob/febe60b9572588f6c722c942775efe9044fe6dfd/images/playbook.png?raw=true)
<a name="Plays"></a>
  * **Plays**

Looking at the YAML, it should be clear that a playbook is a list of dictionaries. 
Specifically, a playbook is a list of plays. 
Think of a play as the thing that connects to a group of hosts and a list of things to do on those hosts for you. 

<a name="Modules"></a>
* **Modules**

Modules are scripts that come packaged with Ansible and perform some kind of action on a host. 
Ansible executes a task on a host by generating a custom script based on the module name and arguments, 
and then copies this script to the host and runs it.
<a name="Variables"></a>
* **Variables**

Variables can be used in tasks, as well as in template files. You reference variables by using *{{ variable }}*

<a name="loops"></a>
* **Loops**

When you want to run a task with each item from a list, you can use loop. A loop executes the task multiple times, each time replacing `item` with different values from the specified list:
   ```
    - name: Copy Certificates files
      copy:
         src: "{{ item }}"
         dest: "{{ tls_dir }}"
         mode: '0600'
      loop:
         - "{{ key_file }}"
         - "{{ cert_file }}"
      notify: Restart nginx
   ```
<a name="Handlers"></a>
* **Handlers**

Handlers are one of the conditional forms that Ansible supports. A handler is similar to a task, but it runs only if it has been notified by a task. 
A task will fire the notification if Ansible recognizes that the task has changed the state of the system.
   ```
      handlers:
      - name: Restart nginx
         service:
            name: nginx
            state: restarted
   ```
Handlers usually run at the end of the play after all of the tasks have been run. To force a notified handler in the middle of a play, we use these two lines of code:
   ```
      - name: Restart nginx
        meta: flush_handlers
   ```
If a play contains multiple handlers, the handlers always run in the order that they are defined in the handlers section, not the notification order. 
They run only once, even if they are notified multiple times.
<a name="Testing"></a>
* **Testing**

   ```
      - name: "Make test! https://localhost:8443/index.html"
         delegate_to: localhost
         become: false
         uri:
         url: 'https://localhost:8443/index.html'
         validate_certs: false
         return_content: true
         register: this
         failed_when: "'Running on ' not in this.content"
   ```
<a name="Validation"></a>
* **Validation**

Use `yamllint` and|or `ansible-lint` that is a Python tool to helps you find potential problems in playbooks.
   ```
         $ ansible-playbook --syntax-check webservers-tls.yml
         $ ansible-lint webservers-tls.yml
         $ yamllint webservers-tls.yml
         $ ansible-inventory --host testserver -i inventory/vagrant.ini
         $ vagrant validate
   ```
---
## Inventory

- [Behavioral Inventory Parameters](#behavioral-inventory-parameters)
- [Groups of Groups](#groups-of-groups)
- [Host and Group Variables](#host-and-group-variables)
- [Dynamic Inventory](#dynamic-inventory)
- [The Interface for a Dynamic Inventory Script](#the-interface-for-a-dynamic-inventory-script)
- [Add_Host and Group at Runtime](#add_host-and-group_by)

The Ansible inventory is a very flexible object: it can be a file (in several formats), a directory, or an executable, and some executables are bundled as plug-ins.
   ```
   [defaults]
   inventory = inventory

   [inventory]
   enable_plugins = host_list, script, auto, yaml, ini, toml
   ```
# Behavioral Inventory Parameters

| Name | Default | Description |
| -----| ------- | ----------- |
| ansible_host | Name of host | Hostname or IP address to SSH to |
| ansible_port | 22 | Port to SSH to |
| ansible_user | $USER | User to SSH as |
| ansible_password | (None) |	Password to use for SSH authentication |
| ansible_connection |smart | How Ansible will connect to host |
| ansible_shell_type | sh | Shell to use for commands |
| ansible_python_interpreter | /usr/bin/python | Python interpreter on host |
| ansible_ssh_private_key_file | (None) | SSH private key to use for SSH authentication |

Changing Behavioral Parameter Defaults
You can override some of the behavioral parameter default values in the inventory file, or you can override them in the defaults section of the ansible.cfg file

# Groups of Groups
Ansible also allows you to define groups that are made up of other groups.

```
[flask:children]
web
task
```
# Host and Group Variables

You can create a separate variable file for each host and each group. Ansible expects these variable files to be in YAML format.
It looks for host variable files in a directory called `host_vars` and group variable files in a directory called `group_vars`.
If we choose YAML dictionaries, we access the variables with dot notation like this:

```
"{{ db.primary.host }}"
"{{ db['primary']['host'] }}"
```

Contrast that to how we would otherwise access them:

```
"{{ db_primary_host }}"
```
# Dynamic Inventory
If the inventory file is marked executable, Ansible will assume it is a dynamic inventory script and will execute the file instead of reading it.
```
$ chmod +x vagrant.py
```

# The Interface for a Dynamic Inventory Script
```
$ ansible-inventory -i inventory/hosts --host=target1
```
*Ansible includes a script that functions as a dynamic inventory script for the static inventory provided with the -i command-line argument: `ansible-inventory`.*

# Breaking the Inventory into Multiple Files

If you want to have both a regular inventory file and a dynamic inventory script, 
just put them all in the same directory and configure Ansible to use that directory as the inventory. 
You can do this via the inventory parameter in ansible.cfg or by using the -i flag on the command line. 
Ansible will process all of the files and merge the results into a single inventory.

<a name="add_host-and-group_by"></a>
# Adding Entries at Runtime with add_host and group_by

Ansible will let you add hosts and groups to the inventory during the execution of a playbook.
The `add_host` module adds a host to the inventory,
This is useful if you’re using Ansible to provision new virtual machine instances inside an IaaS cloud.
If a new host comes online while a playbook is executing, the dynamic inventory script will not pick up this new host.
This is because the dynamic inventory script is executed at the beginning of the playbook.
if any new hosts are added while the playbook is executing, Ansible won’t see them.
```
- name: Add the new host
  add_host
    name: target1
    groups: web,db
    myvar: new_value
```
---
# Variables and Facts
- [Variables](#variables)
- [Facts](#facts)
## Variables
Ansible’s support for variables in strings or in other variables, including a certain type of variable that Ansible calls a `fact`.
- Defining Variables in Playbooks
- Defining Variables in Separate Files  - `vars_files`
- Directory Layout - `host_vars` and `group_vars`

## Viewing the Values of Variables
Variable Interpolation
```
- name: Display the variable
  debug:
    msg: "The file used was {{ conf_file }}"
```

Variables can be concatenated between the double braces by using the tilde operator ~, as shown here:
```
- name: Concatenate variables
  debug:
    msg: "The email address is: {{ username ~'@'~ domain_name }}/"
```
## Registering Variables
If you have to set the value of a variable based on the result of a task (Ansible module returns results in JSON format) and 
to use these results leter, you create a *registered variable* using the `register` clause when invoking a module.
```
- name: Capture output of hostname
  command: hostname
  register: device_hostname
```
   *to find out what a module returns is to register a variable and then output that variable with the `debug` module*
```
---
- name: Show return value of command module
  hosts: target1
  gather_facts: false
  tasks:
    - name: Capture output of whoami command
      command: whoami
      register: login

    - debug: var=login
    - debug: msg="Logged in as user {{ login.stdout }}"
...
```
### Ignoring when a module returns an error
```
- name: Run myprog
  command: /opt/myprog
  register: result
  ignore_errors: true

- debug: var=result
```
## Accessing Dictionary Keys in a Variable
If a variable contains a dictionary, you can access the keys of the dictionary by using either a `dot (.)` or a `subscript ([])`.
```
{{ result.stat }}
```
or
```
{{ result['stat'] }}
```
This rule applies to multiple dereferences, so all of the following are equivalent:
```
   result['stat']['mode']
   result['stat'].mode
   result.stat['mode']
   result.stat.mode
```
A big advantage of subscript notation is that you can use variables in the brackets (these are not quoted):
```
- name: Display result.stat detail
  debug: var=result['stat'][stat_key]
```
## Facts
 - Viewing All Facts Associated with a Server
Ansible implements fact collecting through the use of a special module called the `setup` module.
```
$ ansible ubuntu -m setup
```
Viewing a Subset of Facts
```
ansible target1 -b -k -m setup -a 'filter=ansible_uptime_seconds'
```
* **Local Facts**

Ansible provides an additional mechanism for associating facts with a host. You can place one or more files on the remote host machine in the /etc/ansible/facts.d directory. Ansible will recognize the file if it is:

    - In .ini format
    - In JSON format
    - An executable that takes no arguments and outputs JSON on the standard output stream

```
[git]
title=Ansible and Git
authors=Me
publisher=Me
```
* **Using set_fact to Define a New Variable**

Ansible also allows you to set a fact (effectively the same as defining a new variable) in a task by using the `set_fact` module.
```
- name: Set nginx_state
  when: ansible_facts.services.nginx.state is defined
  set_fact:
    nginx_state: "{{ ansible_facts.services.nginx.state }}"
```
## Built-In Variables
| Parameter | Description |
| --------- | ----------- |
| hostvars | A dict whose keys are Ansible hostnames and values are dicts that map variable names to values |
| inventory_hostname | The name of the current host as known in the Ansible inventory, might include domain name |
| inventory_hostname_short | Name of the current host as known by Ansible, without the domain name (e.g., myhost) |
| group_names | A list of all groups that the current host is a member of |
| groups | A dict whose keys are Ansible group names and values are a list of hostnames that are members of the group. Includes all and ungrouped groups: {“all”: [...], “web”: [...], “ungrouped”: [...]} |
| ansible_check_mode | A boolean that is true when running in check mode (see “Check Mode”) |
| ansible_play_batch | A list of the inventory hostnames that are active in the current batch (see “Running on a Batch of Hosts at a Time”) |
| ansible_play_hosts | A list of all of the inventory hostnames that are active in the current play |
| ansible_version | A dict with Ansible version info: {“full”: 2.3.1.0”, “major”: 2, “minor”: 3, “revision”: 1, “string”: “2.3.1.0”} |

hostvars
```
{{ hostvars['db.example.com'].ansible_eth1.ipv4.address }}
```

## Hostvars Versus host_vars
`hostvars` is computed when you run Ansible, while `host_vars` is a directory that you can use to define variables for a particular system.

## Inventory_hostname
```
ubuntu ansible_host=192.168.4.10
```
   * *then inventory_hostname would be ubuntu.*
     
Output all of the variables associated with the current host with the help of the `hostvars` and `inventory_hostname` variables:

```
- debug: var=hostvars[inventory_hostname]
```

## Extra Variables on the Command Line

Variables set by passing `-e var=value` to `ansible-playbook` have the highest precedence, which means you can use this to override variables that are already defined. 
Specify `-e` multiple times to pass as many variable values as you need.

Ansible also allows you to pass a file containing the variables instead of passing them directly on the command line by passing `@filename.yml` as the argument to `-e`:

```
ansible-playbook target1.yml -e @filename.yml
```
