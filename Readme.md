# Ansible

> Use Ansible to manage devices

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Variables](#Variables)
- [Loops](#Loops)
- [Handlers](#Handlers)
- [Testing](#Testing)
- [Validation](#Validation)

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

## Usage
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

Variables can be used in tasks, as well as in template files. You reference variables by using {{ variable }}

* **Loop**

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