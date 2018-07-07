Por favor
=========

Publishing static documentation in the easiest way possible!

Install
-------

$ pip install porfavor

Use
---

On the server side, you should run the matching server-side implementation.
It listens to any client and puts the given documentation in its right place.

On the server, run:
```shell
$ pip install porfavor
$ porfavor serve --work-dir .  # replace '.' with the desired working directory
```

Now, to deploy documentation on the server, all you have to do is running
```porfavor publish``` with the right arguments:

```shell
$ porfavor publish localhost project_name root_dir
Connecting to host on localhost...
Connected successfully!
Publishing content for project 'project_name'
100%|███████████████████████████████████████████| 108/108 [00:03<00:00, 34.77 files/s]
Finished publishing successfully!
```

Alternatively, you can write the following script, to make deployment more
automatic:

```python
from porfavor import publish

publish(host="localhost",
        project="project_name",
        root_dir="root_dir")
```
