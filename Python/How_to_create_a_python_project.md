## Python package to manage users on a server based on an “inventory” JSON file. 

Linux Academy final assignment in "Python 3 Scripting for System Administrators"

The first step in this process is going to be setting up the project’s directory structure and metadata.

Create a project folder called hr (short for “human resources”).

```
$ mkdir hr
$ cd hr
$ mkdir -p src/hr tests
$ touch src/hr/__init__.py tests/.keep README.rst
```

Set up the directories to put the project’s source code and tests. You can then utilize pipenv to add dependency management:

Note: Ensure that which has been installed and is in your $PATH

```
$ pipenv --python python3.6 install --dev pytest pytest-mock
```

Create the setup.py with metadata and package discovery.

```
from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='hr',
    version='0.1.0',
    description='Commandline user management utility',
    long_description=readme,
    author='Ivan Omar',
    author_email='ivan.omar@mypython.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[]
)
```

Set the project up in source control and make your initial commit.

```
$ git init
$ curl https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore -o .gitignore
$ git add --all .
$ git commit -m 'Initial commit.'
```

The ideal usage of the hr command is:

```
$ hr path/to/inventory.json
Adding user 'kevin'
Added user 'kevin'
Updating user 'lisa'
Updated user 'lisa'
Removing user 'alex'
Removed user 'alex'
```

The alternative usage of the CLI will be to pass a --export flag like so:

```
$ hr --export path/to/inventory.json
```

This --export flag won’t take any arguments. Instead, you’ll want to default the value of this field to False and set the value to True if the flag is present.

Ensure the following with the tests:

An error is raised if no arguments are passed to the parser.
No error is raised if a path is given as an argument.
The export value is set to True if the --export flag is given.

*tests/test_cli.py*

```
import pytest

from hr import cli

@pytest.fixture()
def parser():
    return cli.create_parser()

def test_parser_fails_without_arguments(parser):
    """
    Without a path, the parser should exit with an error.
    """
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_parser_succeeds_with_a_path(parser):
    """
    With a path, the parser should exit with an error.
    """
    args = parser.parse_args(['/some/path'])
    assert args.path == '/some/path'

def test_parser_export_flag(parser):
    """
    The `export` value should default to False, but set
    to True when passed to the parser.
    """
    args = parser.parse_args(['/some/path'])
    assert args.export == False

    args = parser.parse_args(['--export', '/some/path'])
    assert args.export == True
```

*src/hr/cli.py*

```
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to the inventory file (JSON)')
    parser.add_argument('--export', action='store_true', help='export current settings to inventory file')
    return parser
```

Create a module in your package to work with user information. You’ll want to be able to do the following:

Received a list of user dictionaries and ensure that the system’s users match.
Have a function that can create a user with the given information if no user exists by that name.
Have a function that can update a user based on a user dictionary.
Have a function that can remove a user with a given username.
The create, update, and remove functions should print that they are creating/updating/removing the user before executing the command.
The user information will come in the form of a dictionary shaped like this:

```
{
  'name': 'kevin',
  'groups': ['wheel', 'dev'],
  'password': '$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/'
}
```

The password values will be SHA512 encrypted.

Hint: You can generate an encrypted password in Python that is usable with usermod -p with this snippet:

```
import crypt

crypt.crypt('password', crypt.mksalt(crypt.METHOD_SHA512))
```

*tests/test_users.py*

```
import pytest
import subprocess

from hr import users

# encrypted version of 'password'
password = '$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/'

user_dict = {
    'name': 'kevin',
    'groups': ['wheel', 'dev'],
    'password': password
}

def test_users_add(mocker):
    """
    Given a user dictionary. `users.add(...)` should
    utilize `useradd` to create a user with the password
    and groups.
    """
    mocker.patch('subprocess.call')
    users.add(user_dict)
    subprocess.call.assert_called_with([
        'useradd',
        '-p',
        password,
        '-G',
        'wheel,dev',
        'kevin',
    ])

def test_users_remove(mocker):
    """
    Given a user dictionary, `users.remove(...)` should
    utilize `userdel` to delete the user.
    """
    mocker.patch('subprocess.call')
    users.remove(user_dict)
    subprocess.call.assert_called_with([
        'userdel',
        '-r',
        'kevin',
    ])

def test_users_update(mocker):
    """
    Given a user dictionary, `users.update(...)` should
    utilize `usermod` to set the groups and password for the
    user.
    """
    mocker.patch('subprocess.call')
    users.update(user_dict)
    subprocess.call.assert_called_with([
        'usermod',
        '-p',
        password,
        '-G',
        'wheel,dev',
        'kevin',
    ])

def test_users_sync(mocker):
    """
    Given a list of user dictionaries, `users.sync(...)` should
    create missing users, remove extra non-system users, and update
    existing users. A list of existing usernames can be passed in
    or default users will be used.
    """
    existing_user_names = ['kevin', 'bob']
    users_info = [
        user_dict,
        {
            'name': 'jose',
            'groups': ['wheel'],
            'password': password
        }
    ]
    mocker.patch('subprocess.call')
    users.sync(users_info, existing_user_names)

    subprocess.call.assert_has_calls([
        mocker.call([
            'usermod',
            '-p',
            password,
            '-G',
            'wheel,dev',
            'kevin',
        ]),
        mocker.call([
            'useradd',
            '-p',
            password,
            '-G',
            'wheel',
            'jose',
        ]),
        mocker.call([
            'userdel',
            '-r',
            'bob',
        ]),
    ])
```

Notice: Since there were multiple calls made to subprocess.call within the sync test we used a different assertion method called assert_has_calls which takes a list of mocker.call objects. 

The mocker.call method wraps the content we would otherwise have put in an assert_called_with assertion.

*src/hr/users.py*

```
import pwd
import subprocess
import sys

def add(user_info):
    print(f"Adding user '{user_info['name']}'")
    try:
        subprocess.call([
            'useradd',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print(f"Failed to add user '{user_info['name']}'")
        sys.exit(1)

def remove(user_info):
    print(f"Removing user '{user_info['name']}'")
    try:
        subprocess.call([
            'userdel',
            '-r',
            user_info['name']
        ])
    except:
        print(f"Failed to remove user '{user_info['name']}'")
        sys.exit(1)

def update(user_info):
    print(f"Updating user '{user_info['name']}'")
    try:
        subprocess.call([
            'usermod',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print(f"Failed to update user '{user_info['name']}'")
        sys.exit(1)

def sync(users, existing_user_names=None):
    existing_user_names = (existing_user_names or _user_names())
    user_names = [user['name'] for user in users]
    for user in users:
        if user['name'] not in existing_user_names:
            add(user)
        elif user['name'] in existing_user_names:
            update(user)
    for user_name in existing_user_names:
        if not user_name in user_names:
            remove({ 'name': user_name })

def _groups_str(user_info):
    return ','.join(user_info['groups'] or [])

def _user_names():
    return [user.pw_name for user in pwd.getpwall()
            if user.pw_uid >= 1000 and 'home' in user.pw_dir]
```

I utilized the pwd module to get a list of all of the users on the system and determined which ones weren’t system users by looking for UIDs over 999 and ensuring that the user’s directory was under home. 
Additionally, the join method on str was used to combine a list of values into a single string separated by commas. This action is roughly equivalent to:

```
index = 0
group_str = ""
for group in groups:
    if index == 0:
        group_str += group
    else:
        group_str += ",%s" % group
    index+=1
```

To manually test this you’ll need to (temporarily) run the following from within your project’s directory:

```
sudo pip3.6 install -e .
```

Now we need to implement a module to interact with the user inventory file. The inventory file is a JSON file that holds user information. 

The module needs to:

Have a function to read a given inventory file, parse the JSON, and return a list of user dictionaries.
Have a function that takes a path, and produces an inventory file based on the current state of the system. An optional parameter could be the specific users to export.

Example inventory JSON file:

```
[
  {
    "name": "kevin",
    "groups": ["wheel", "dev"],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  },
  {
    "name": "lisa",
    "groups": ["wheel"],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  },
  {
    "name": "jim",
    "groups": [],
    "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"
  }
]
```

Hint: If you’re writing tests for this code you’ll need to heavily rely on mocking to make the interactions with modules like grp, pwd, and spwd consistent.

*tests/test_inventory.py*

```
import tempfile

from hr import inventory

def test_inventory_load():
    """
    `inventory.load` takes a path to a file and parses it as JSON
    """
    inv_file = tempfile.NamedTemporaryFile(delete=False)
    inv_file.write(b"""
    [
      {
        "name": "kevin",
        "groups": ["wheel", "dev"],
        "password": "password_one"
      },
      {
        "name": "lisa",
        "groups": ["wheel"],
        "password": "password_two"
      },
      {
        "name": "jim",
        "groups": [],
        "password": "password_three"
      }
    ]
    """)
    inv_file.close()
    users_list = inventory.load(inv_file.name)
    assert users_list[0] == {
        'name': 'kevin',
        'groups': ['wheel', 'dev'],
        'password': 'password_one'
    }
    assert users_list[1] == {
        'name': 'lisa',
        'groups': ['wheel'],
        'password': 'password_two'
    }
    assert users_list[2] == {
        'name': 'jim',
        'groups': [],
        'password': 'password_three'
    }

def test_inventory_dump(mocker):
    """
    `inventory.dump` takes a destination path and optional list of users to export then exports the existing user information.
    """
    dest_file = tempfile.NamedTemporaryFile(delete=False)
    dest_file.close()

    # spwd.getspnam can't be used by non-root user normally.
    # Mock the implemntation so that we can test.
    mocker.patch('spwd.getspnam', return_value=mocker.Mock(sp_pwd='password'))

    # grp.getgrall will return the values from the test machine.
    # To get consistent results we need to mock this.
    mocker.patch('grp.getgrall', return_value=[
        mocker.Mock(gr_name='super', gr_mem=['bob']),
        mocker.Mock(gr_name='other', gr_mem=[]),
        mocker.Mock(gr_name='wheel', gr_mem=['bob', 'kevin']),
    ])

    inventory.dump(dest_file.name, ['kevin', 'bob'])

    with open(dest_file.name) as f:
        assert f.read() == """[{"name": "kevin", "groups": ["wheel"], "password": "password"}, {"name": "bob", "groups": ["super", "wheel"], "password": "password"}]"""
```

Notice that we had to jump through quite a few hoops to get the tests to work consistently for the dump function. The test_inventory_dump required so much mocking that it is debatable as to whether or not it’s worth the effort to test. 
Here’s the implementation of the module:

*src/hr/inventory.py*

```
import grp
import json
import spwd

from .helpers import user_names

def load(path):
    with open(path) as f:
        return json.load(f)

def dump(path, user_names=user_names()):
    users = []
    for user_name in user_names:
        password = spwd.getspnam(user_name).sp_pwd
        groups = _groups_for_user(user_name)
        users.append({
            'name': user_name,
            'groups': groups,
            'password': password
        })
    with open(path, 'w') as f:
        json.dump(users, f)

def _groups_for_user(user_name):
    return [g.gr_name for g in grp.getgrall() if user_name in g.gr_mem]
```

The default list of user_names for the dump function used the same code that was used previously in the users module so it was extracted into a new helpers module to be used in both.

```
import pwd

def user_names():
    return [user.pw_name for user in pwd.getpwall()
            if user.pw_uid >= 1000 and 'home' in user.pw_dir]
``` 

Here’s the updated users module:

*src/hr/users.py*

```
import pwd
import subprocess
import sys

from .helpers import user_names

def add(user_info):
    print("Adding user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'useradd',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print("Failed to add user '%s'" % user_info['name'])
        sys.exit(1)

def remove(user_info):
    print("Removing user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'userdel',
            '-r',
            user_info['name']
        ])
    except:
        print("Failed to remove user '%s'" % user_info['name'])
        sys.exit(1)

def update(user_info):
    print("Updating user '%s'" % user_info['name'])
    try:
        subprocess.call([
            'usermod',
            '-p',
            user_info['password'],
            '-G',
            _groups_str(user_info),
            user_info['name'],
        ])
    except:
        print("Failed to update user '%s'" % user_info['name'])
        sys.exit(1)

def sync(users, existing_user_names=user_names()):
    user_names = [user['name'] for user in users]
    for user in users:
        if user['name'] not in existing_user_names:
            add(user)
        elif user['name'] in existing_user_names:
            update(user)
    for user_name in existing_user_names:
        if not user_name in user_names:
            remove({ 'name': user_name })

def _groups_str(user_info):
    return ','.join(user_info['groups'] or [])
```

Load the Python3.6 REPL as root to interact with the new inventory module:

```
$ sudo python3.6
>>> from hr import inventory
>>> inventory.dump('./inventory.json')
>>> exit()
```

Now you can look at the new inventory.json file to see that it dumped the users properly.

```
$ cat inventory.json
[{"name": "kevin", "groups": ["wheel"], "password": "$6$HXdlMJqcV8LZ1DIF$LCXVxmaI/ySqNtLI6b64LszjM0V5AfD.ABaUcf4j9aJWse2t3Jr2AoB1zZxUfCr8SOG0XiMODVj2ajcQbZ4H4/"}]
```

Wire the pieces together and modify the package metadata to create a console script when installed.

Implement main function that ties all of the modules together based on input to the CLI parser.
Modify the setup.py so that when installed there is an hr console script.


Example main function that was added to the cli module:

*src/hr/cli.py*

```
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='the path to the inventory file (JSON)')
    parser.add_argument('--export', action='store_true', help='export current settings to inventory file')
    return parser

def main():
    from hr import inventory, users

    args = create_parser().parse_args()

    if args.export:
        inventory.dump(args.path)
    else:
        users_info = inventory.load(args.path)
        users.sync(users_info)
```

Modifications for the setup.py file necessary to create a console script:

*setup.py*

```
from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='hr',
    version='0.1.0',
    description='Commandline user management utility',
    long_description=readme,
    author='Your Name',
    author_email='person@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': 'hr=hr.cli:main',
    },
)
```

Install it using sudo pip3.6 so ti runs with sudo:

```
$ sudo pip3.6 install -e .
$ sudo hr --help
usage: hr [-h] [--export] path

positional arguments:
  path        the path to the inventory file (JSON)

optional arguments:
  -h, --help  show this help message and exit
  --export    export current settings to inventory file
```

Build a wheel for the package and use it to install the hr tool on your system.

Extra metadata file:

*MANIFEST.in*

```
include README.rst
recursive-include tests *.py
```

Using the pipenv shell, this is the command to build the wheel:

```
(h4-YsGEiW1S) $ python setup.py bdist_wheel
```

Lastly, here’s how you would install this wheel for the root user to be able to use (run from project directory):

```
$ sudo pip3.6 install --upgrade dist/hr-0.1.0-py3-none-any.whl
```