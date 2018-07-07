Por favor
=========

Publishing static documentation the easiest way possible!

Install
-------

```shell
$ pip install porfavor
```

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
$ # porfavor publish <server's domain or IP address> \
>                    <project name> \
>                    <documentation root>
$ porfavor publish localhost my_amazing_project docs/_build/html/
Connecting to host on localhost...
Connected successfully!
Publishing content for project 'my_amazing_project'
100%|███████████████████████████████████████████| 108/108 [00:03<00:00, 34.77 files/s]
Finished publishing successfully!
```

Alternatively, you can write the following script, to make deployment more
automatic:

```python
from porfavor import publish

if __name__ == '__main__':
    publish(host="localhost",
            project="project_name",
            root_dir="root_dir")
```
