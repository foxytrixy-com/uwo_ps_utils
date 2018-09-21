"""Common util functions
"""
import os

def get_image_paths(directory, ext):
    """Get full paths with given extenstion

    Arguments:
        directory (str): Image directory path
        ext (str): Extenstion filter to add to list

    Return:
        full paths (list)
    """
    image_files = []
    for (dirpath, _, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(ext):
                image_files.append(os.sep.join([dirpath, filename]))
    return image_files