# Python Django Dev to Deployment

A code-along repo for the [Udemy course](https://www.udemy.com/course/python-django-dev-to-deployment/)

## Python Review

### Tuples

- Tuples in python are immutable data structure. You can't reassign values to them once they're initialized.
- You can create a single-value tuple with trailing comma.
- You can't mutate tuples, but you can `delete` them.

### venv

venv is a python module for creating virtual environments.

You can create a virtual environment by:

```bash
# Create a virtual environment in the current directory
python3 -m venv .
```

You can activate the created environment:

```bash
source ./venv/bin/activate
```

Try absolute path if it doesn't work.

Once activated, the python version will default to the version that was used to create this environment.

```bash
(venv) ➜  django-postgresql-realestate python --version
Python 3.9.1
```

Check if the environment is isolated from the main system by:

```bash
pip freeze
# will show no packages installed
```

To leave the environment, you can deactivate it.

```bash
deactivate

pip freeze
# will show all pip packages installed globally
```

### Install Django
