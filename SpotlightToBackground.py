"""
Leverage Spotlight for awesome backgrounds in Windows 10.

Maintain copies of all JPEGs downloaded by Microsoft Spotlight in a mirror
location for use by the Windows 10 Background service.
In addition to the standard library, you will need Pillow installed.
    > pip install Pillow>=5.4.1
"""
from hashlib import md5
from imghdr import what
import logging
from os import environ, listdir, makedirs
from os.path import join
from shutil import copy
from PIL import Image


# Constants
# Name of directory in which we will store the JPEG files, and to which we will
# configure as the background slideshow source
COLLECTION_DIR = "Backgrounds"
JPEG_EXTENSION = ".jpg"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Hashing code taken from StackOverflow article:
# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def md5_hash_file(path):
    """Find md5 digest of contents of a file."""
    # We are going to hash in 512 kilobyte chunks
    BUF_SIZE = 512 * 1024
    myhash = md5()

    with open(path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            myhash.update(data)
    return myhash.hexdigest()


def scan_dir_for_jpegs(path):
    """
    Scan a directory for JPEGs.

    Given a path on disk, scan the contents for files that are JPEGs, and
    return a dict of the results keyed by their md5 digests. Files are
    determined to be JPEGs based on their contents, not the names alone.
    We only consider images of at least 1920 pixels width to be good background
    images. This filters out icons, advertising banners, and mobile device
    backgrounds in portrait format.
    """
    census_hit = 0
    incoming = {}
    for candidate in listdir(path):
        fqn = join(path, candidate)
        if what(fqn) == 'jpeg':
            im = Image.open(fqn)
            (width, _) = im.size
            if (width >= 1920):
                census_hit += 1
                digest = md5_hash_file(fqn)
                incoming[digest] = {
                    "fqn": fqn,
                    "name": candidate,
                    "md5": digest
                }
    logger.info("Found {} acceptable JPEGs in {}".format(census_hit, path))
    return incoming


def get_asset_path():
    """Return the path to Microsoft Spotlight assets."""
    root = environ['USERPROFILE']
    branches = [
        "AppData", "Local", "Packages",
        "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy",
        "LocalState", "Assets"]
    return join(root, *branches)


def get_background_path():
    """
    Return the path to where the background images should be stored.

    Also, create said directory if it does not already exist
    """
    root = environ['USERPROFILE']
    path = join(root, COLLECTION_DIR)
    makedirs(path, exist_ok=True)
    return path


def main():
    """Provide main processing sequence."""
    # Figure out the paths for incoming and collected images
    incoming_asset_path = get_asset_path()
    backgrounds_path = get_background_path()

    # Gather a census of the images present in both locations
    incoming_images = scan_dir_for_jpegs(incoming_asset_path)
    existing_images = scan_dir_for_jpegs(backgrounds_path)

    # Find all images in incoming that are not present in collection,
    # then copy them to collection and include .jpg extension on the
    # filename
    new_images = set(incoming_images.keys()) - set(existing_images.keys())
    logger.info("Found {} new images".format(len(new_images)))
    for image in new_images:
        copy_name = incoming_images[image]['name'] + JPEG_EXTENSION
        copy_fqn = join(backgrounds_path, copy_name)
        copy(incoming_images[image]['fqn'], copy_fqn)


if __name__ == "__main__":
    main()
