# Common problems in CellPhoneDB

## Installation errors

### Create new virtual-env fails:
Reported on OS:
- Ubuntu 16.04

**Code runed**
```shell
python3 -m venv cpdb-env
```

**Output**
```shell
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt-get install python3-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: ['/home/ubuntu/asd/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']
```

**Solution**

1. Try the solution provided (Install the package)
```shell
sudo apt-get update
sudo apt-get install python3-venv
```
2. If not works, configure the locales
```shell
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales
```

**Note**

If you're runnning  _dpkg-reconfigure locales_ in a container o external server sometimes you can't set it. In this cases, just make the exports when you start the session.