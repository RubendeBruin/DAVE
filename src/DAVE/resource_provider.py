"""Resource supply for DAVE.

from the documentation:

The content of these files is not stored in the DAVE model itself, they are read when the model is loaded or when the
node is updated. The DAVE model only stores the location and name of the file it needs to read.

The name and location of the file ("resource") can be provided to DAVE using the full path of the file.
For example: `c:/users/yourname/model.dave` . While this will work fine for you, it will give issues when sharing
your model with somebody else. Therefore DAVE provides the following options to point to a file in a "standard location"

`res: model.dave`  Add `res: ` in front of a filename to locate the file in the "resource" system
`cd: model.dave` Add `cd:` in front of a filename to read the file from the "current directory"

The Scene object will *not* walk through sub-folders when looking for an asset or resource.
This means that subfolders add to the uniqueness of the filename.
A file called `res: attempt1/box.obj` is different from a file `res: attempt2/box.obj`

A Scene contains a list of locations where assets and resources can be found.
The standard resource paths (on top)  can not be changed in the GUI.

The order of the list is important.
The list is considered to be ordered from most-official to least-official. So, for the default list,
a resource in the `resources` subfolder of the DAVE installation is considered of higher rank than a
resource with the same name in the users DAVE_assets folder.


Mappings
--------

The resource system also supports "mappings". A mapping is a way to map a filename to a different filename.
These take the form of a dictionary with the URL as key and the new filename as value.

Install using `DaveResourceProvider.install_mapping()`, remove with remove_mapping()

"""
import warnings
from pathlib import Path

# from DAVE.gui.error_interaction import ErrorInteraction
from DAVE.tools import get_all_files_with_extension, MostLikelyMatch
from DAVE.settings import RESOURCE_PATH


class DaveResourceProvider:
    def __init__(self, cd=None, *args):
        """Create a new resource provider

        all arguments (if any) are paths to folders that contain resources
        """

        self.cd: Path or None = None
        if cd is not None:
            self.cd = Path(cd)

        self.resources_paths: list[Path] = [Path(a) for a in RESOURCE_PATH + list(args)]

        # logging
        self._log = []  # list of tuples (filename, path)

        # mapping
        self.mapping = dict()
        self.mapping_root = None

    def install_mapping(self, root: Path, mapping: dict):
        self.mapping = mapping
        self.mapping_root = Path(root)

    def remove_mapping(self):
        self.mapping = dict()
        self.mapping_root = None

    def addPath(self, path: Path):
        """Add a path to the resource list"""
        assert isinstance(path, Path), "path must be a Path object"

        if path not in self.resources_paths:
            self.resources_paths.append(path)
        else:
            warnings.warn(f"Path {path} already in resource list")

    def log(self, filename: str, path: Path):
        """Add a log entry"""
        self._log.append((filename, path))

    def clearLog(self):
        """Clear the log"""
        self._log = []

    def getLog(self):
        """Get the log"""
        return self._log.copy()

    def get_valid_resource_url(self, resource_url: str, error_interaction = None) -> str:
        """Get a valid resource url
        
        if the provided resource_url is valid, then return it
        if the provided resource_url is not valid, then return a valid one using error_interaction if possible
        otherwise raise FileNotFoundError
        """

        try:
            self.get_resource_path(resource_url, error_interaction=None)
            return resource_url
        except FileNotFoundError as MSG:
            return str(self.get_resource_path(resource_url, error_interaction=error_interaction))



    def get_resource_path(self, filename: str, error_interaction : "ErrorInteraction" or None = None) -> Path:
        """Get a resource path

        filename can be a full path, or a path relative to one of the resource folders
        """
        file = None
        filename = filename.strip()

        if filename in self.mapping:
            file = self.mapping_root / self.mapping[filename]
            if not file.exists():
                raise FileNotFoundError(
                    f"Could not find MAPPED resource for: {filename}"
                )
            return file

        try:
            if filename.startswith("cd:"):
                file = self._get_cd_path(filename[3:].strip())

            elif filename.startswith("res:"):
                file = self._get_resource_path(filename[4:].strip())

            # check if the filename is a full path to a file
            else:
                f = Path(filename)
                if f.is_file():
                    file = f
                else:
                    # gracefully handle the error if use forgot to add 'res:'
                    if not filename.startswith("res:"):
                        try:
                            file = self._get_resource_path(filename)
                            warnings.warn(
                                "Missing 'res:' in resource path, assuming you wanted to use 'res:'"
                            )
                        except FileNotFoundError:
                            raise FileNotFoundError(
                                f"Could not find resource for: {filename}"
                            )
                    else:
                        raise FileNotFoundError(
                            f"Could not find resource for: {filename}"
                        )

        except FileNotFoundError as MSG:

            if error_interaction:
                file = error_interaction.handle_missing_resource(resource_provider = self, resource_name = filename)
                if file is not None:
                    return file
            raise MSG

        self.log(filename, file)

        return file

    def _get_cd_path(self, filename: str) -> Path:
        """Get a resource path

        filename is a path relative to the current directory
        """

        if self.cd is None:
            raise FileNotFoundError(
                f"Could not find resource for CD: {filename}\nNo current directory set"
            )

        # check if the filename is a relative path
        f = self.cd / filename
        if f.exists():
            return f

        # if we get here, the file does not exist
        raise FileNotFoundError(
            f"Could not find resource for CD: {filename}\nDoes not exist: {str(f)}"
        )

    def _get_resource_path(self, filename: str) -> Path:
        """Get a resource path

        filename is a path relative to one of the resource folders
        """

        # check if the filename is a relative path
        for p in self.resources_paths:
            f = p / filename
            if f.is_file():
                return f

        # if we get here, the file does not exist
        #
        # Give some useful feedback
        options = self.get_resource_list(
            extension=filename.split(".")[-1], include_subdirs=True
        )
        guess = MostLikelyMatch(filename, options)

        raise FileNotFoundError(
            f"Could not find resource for RES: {filename}, did you mean: {guess} ?"
        )


    def get_resource_list(
        self, extension, include_subdirs=False, include_current_dir=True
    ):
        """Returns a list of all UNIQUE resources (strings) with given extension in any of the resource-paths

        extension: (str) extension to look for, for example 'dave' or '.dave' ; can be a list of extensions
        include_subdirs : do a recursive search
        include_current_dir : return 'cd:' based resources as well

        """
        r = []  # results

        for dir in self.resources_paths:
            try:
                files = get_all_files_with_extension(
                    root_dir=dir, extension=extension, include_subdirs=include_subdirs
                )

                for file in files:
                    file = "res: " + file.replace("\\", "/")
                    if file not in r:
                        r.append(file)

            except FileNotFoundError:
                pass

        if include_current_dir:
            if self.cd is not None:
                files = get_all_files_with_extension(
                    root_dir=self.cd,
                    extension=extension,
                    include_subdirs=include_subdirs,
                )

                for file in files:
                    file = "cd: " + file.replace("\\", "/")
                    if file not in r:
                        r.append(file)
            else:
                warnings.warn(
                    "No current directory set - not returning any 'cd:' resources"
                )

        return r
