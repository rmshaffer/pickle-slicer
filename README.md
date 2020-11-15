# pickleslicer: Automatic slicer and unslicer of pickle files

The `pickleslicer` package provides a convenient way to create and load pickle files
in scenarios where storing many small files is preferable to storing a single large file.

The `pickleslicer` package wraps Python's built-in `pickle` package and has a very similar usage pattern.

## Installation

The package distribution is hosted on PyPI and can be installed via `pip`:

```
pip install pickleslicer
```

## Creating sliced pickle files

To create sliced pickle files, call `pickleslicer.dump()`:

```python
import pickleslicer

obj = {}   # obj can be any Python object
pickleslicer.dump(obj, "myfilename.pickle")
```

This will create sliced pickle files named `myfilename.pickle.1`, `myfilename.pickle.2`, etc., with each file having a maximum size of 10 MB.

To customize the maximum file size, specify the `max_size` parameter:

```python
pickleslicer.dump(obj, "myfilename.pickle", max_size=50*1024*1024)  # 50 MB
```

## Loading sliced pickle files

To load sliced pickle files that have previously been created, call `pickleslicer.load()`:

```python
import pickleslicer

obj = pickleslicer.load("myfilename.pickle")
```

This will load sliced pickle files named `myfilename.pickle.1`, `myfilename.pickle.2`, etc. The unpickled Python object is returned.
