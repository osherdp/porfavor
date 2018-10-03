Por favor
=========

[![PyPI](https://badge.fury.io/py/porfavor.svg)](https://pypi.python.org/pypi/porfavor)
[![Build Status](https://travis-ci.com/osherdp/porfavor.svg?branch=master)](https://travis-ci.com/osherdp/porfavor)

Publishing static documentation the easiest way possible!

Install
-------

```console
$ pip install porfavor
```

Use
---

On the server side, you should run the matching server-side implementation.
It listens to any client and puts the given documentation in its right place.

On the server, run:
```console
$ pip install porfavor
...
$ porfavor serve .  # replace '.' with the desired working directory
...
```

Now, to deploy documentation on the server, all you have to do is running
```porfavor publish``` with the right arguments:

```console
$ # porfavor publish <server's URL> \
>                    <project name> \
>                    <documentation root>
$ porfavor publish localhost:5000 my_amazing_project docs/_build/html/
Zipping content of folder 'docs/_build/html'... DONE!
Publishing content for project 'my_amazing_project'... DONE!
```

Alternatively, you can write the following script, to make deployment more
automatic:

```python
from porfavor import publish

if __name__ == '__main__':
    publish(host="localhost:5000",
            project="project_name",
            file_or_directory="root_dir")
```
