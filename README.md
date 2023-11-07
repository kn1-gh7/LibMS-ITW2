<!-- # fuzzy-computing-machine -->

CSE 205 Project

Made by _Yuval Goyal_ and _Arnav Kumar Sinha_.

Roll No  : 22075097, 22075013

Group No.: 35

# A library management system


---
### Quickstart:

Firstly set up `mysql` server with user `root` and password = `password`.

Also add a database named `libdb` to the said server.

```console
$ python3 -m venv project_venv
$ source ./project_venv/bin/activate

$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

$ pip install -r requirements.txt

$ mkdir library_management_system
$ cd library_management_system

$ django-admin startproject libms .
$ python3 manage.py startapp main

```
> [!NOTE]
> NOTE: You will need to set up the `genres` table and the  `transaction_types` table in the database, either through the admin panel, or directly in the mysql server