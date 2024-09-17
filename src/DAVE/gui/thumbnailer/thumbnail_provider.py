"""Thumbnail provider module.

Thumbnails can be provided for all kinds of files.
Once created, the thumbnail is stored for future use.

Storing is done in the DAVE user folder, in a subfolder called 'thumbnails'.



"""
from pathlib import Path

from PySide6.QtGui import QPixmap

from DAVE.helpers.singleton_class import Singleton
from DAVE.settings import default_user_dir

import hashlib

from .dave_thumbnails import give_pixmap_from_DAVE_model
from .vtk_thumbnails import give_pixmap_from_3dfile

def generate_file_hash(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
@Singleton
class ThumbnailProvider(object):
    def __init__(self):
        self.tumbnail_folder = default_user_dir / 'thumbnails'
        self.tumbnail_folder.mkdir(parents=True, exist_ok=True)

    def to_filename(self, hash):
        return self.tumbnail_folder / ('T' + hash + '.png')
    def get_thumbnail_from_cache(self, hash):
        # Get the thumbnail from the cache
        if self.to_filename(hash).exists():
            return QPixmap(str(self.to_filename(hash)))
        print(f'No thumbnail found in cache for {str(self.to_filename(hash))}')
        return None

    def get_thumbnail(self, path : Path) -> QPixmap:
        # Get the thumbnail for the given path

        # Check if the thumbnail is in the cache
        hash = generate_file_hash(path)

        t = self.get_thumbnail_from_cache(hash)
        if t is not None:
            return t

        t = self._create_thumbnail(path)

        # Save the thumbnail to the cache
        fname = self.to_filename(hash)
        print(f'Saving thumbnail to cache as {fname}')

        t.save(str(fname))

        return t

    def _create_thumbnail(self, path):
        # Create a thumbnail of the given path

        print('Creating thumbnail for', path)

        # check file type
        if path.suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            return QPixmap(str(path))

        if path.suffix in ['.glb', '.obj', '.stl', '.gltf']:
            # Create a thumbnail for a 3D model
            return give_pixmap_from_3dfile(str(path))

        if path.suffix == '.dave':
            # Create a thumbnail for a DAVE file
            return give_pixmap_from_DAVE_model(path)

        return QPixmap()

