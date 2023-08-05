# Ansible

> Use Ansible to manage devices

## Table of Contents

- [Install](#install)
- [Basic Usage](#basic-usage)
- [Inventory](#inventory)

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

  * **Plays**

Looking at the YAML, it should be clear that a playbook is a list of dictionaries. 
Specifically, a playbook is a list of plays. 
Think of a play as the thing that connects to a group of hosts and a list of things to do on those hosts for you. 


* **Modules**

Modules are scripts that come packaged with Ansible and perform some kind of action on a host. 
Ansible executes a task on a host by generating a custom script based on the module name and arguments, 
and then copies this script to the host and runs it.

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

The Ansible inventory is a very flexible object: it can be a file (in several formats), a directory, or an executable, and some executables are bundled as plug-ins.
   ```
   [defaults]
   inventory = inventory

   [inventory]
   enable_plugins = host_list, script, auto, yaml, ini, toml
   ```
* **Behavioral Inventory Parameters**

| Name | Default | Description |
| -----| ------- | ----------- |
| ansible_host | Name of host | Hostname or IP address to SSH to |
| ansible_port | 22 | Port to SSH to |
| ansible_user | $USER | User to SSH as |
| ansible_password | (None) |	Password to use for SSH authentication |
| ansible_connection |smart | How Ansible will connect to host (see the following section) |
| ansible_shell_type | sh | Shell to use for commands (see the following section) |
| ansible_python_interpreter | /usr/bin/python | Python interpreter on host (see the following section) |
| ansible_ssh_private_key_file | (None) | SSH private key to use for SSH authentication |
