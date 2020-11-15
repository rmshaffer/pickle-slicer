'''
Core functionality for dumping and loading sliced pickles.
'''

import io
import os.path
import pickle

def _get_chunk_filename(base_filename: str, chunk_number: int) -> str:
    return f"{base_filename}.{chunk_number}"

def dump(obj: object, base_filename: str, max_size: int = 10*1024*1024):
    '''
    Dumps an object to sliced pickle files no larger than the specified size.

    :param obj: The object to be pickled.
    :type obj: object
    :param base_filename: The filename to be used as the base of the sliced pickle
    :type base_filename: str
    filenames. The actual filenames will have `.1`, `.2`, etc. appended.
    :param max_size: The maximum size (in bytes) of each sliced pickle file.
    :type max_size: int
    '''
    if obj is None:
        raise TypeError("obj cannot be None")
    if not isinstance(max_size, int):
        raise TypeError("max_size must be an integer")

    if not str(base_filename):
        raise ValueError("base_filename must be a non-empty string")
    if max_size <= 0:
        raise ValueError("max_size must be a positive integer")

    dumped = pickle.dumps(obj)
    with io.BytesIO(dumped) as byte_stream:
        chunk_number = 1
        chunk = byte_stream.read(max_size)
        while chunk:
            with open(_get_chunk_filename(base_filename, chunk_number), 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk = byte_stream.read(max_size)
            chunk_number += 1

def load(base_filename: str) -> object:
    '''
    Loads an object from sliced pickle files.

    :param base_filename: The filename used as the base of the sliced pickle
    filenames. The actual filenames must have `.1`, `.2`, etc. appended.
    :returns: The unpickled object.
    :rtype: object
    '''
    if not str(base_filename):
        raise ValueError("base_filename must be a non-empty string")

    with io.BytesIO() as byte_stream:
        chunk_number = 1
        while os.path.isfile(_get_chunk_filename(base_filename, chunk_number)):
            with open(_get_chunk_filename(base_filename, chunk_number), 'rb') as chunk_file:
                chunk = chunk_file.read()
                byte_stream.write(chunk)
            chunk_number += 1

        if chunk_number <= 1:
            raise FileNotFoundError(f"No sliced pickles found with base_filename {base_filename}")

        return pickle.loads(byte_stream.getvalue())
