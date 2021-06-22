Assets and resources
====================

DAVE is designed with use as part of a larger system in mind. In such a system various sources for assets and resources may exist.
For example a shared library with officially approved assets, an library with project assets that are still under construction, a personal folder with the items you are working on at that moment.

On the other hand, DAVE can also be used completely separated from the rest of the world.

Assets and resources are FILES on a file-system somewhere. Assets are files with a .dave_asset extension and can be imported into a scene or can be opened as a scene. Resources are all other type of files that may be needed such as .obj or .stl files for visuals or buoyancy, hydrodynamic databases and so on.

A Scene contains a list of locations where assets and resources can be found. This list is in `Scene.resources_paths`. By default it is initialized (in `constants.py`) to

1. the `resources` subdirectory in the DAVE python source folder
2. the `DAVE_models` subdirectory in the users home folder.

You are free to add more locations or remove existing locations by either changing the initilization in constants.py for a system-wide change or by changing the `resources_paths` list of the current Scene object.
For example:

.. code-block:: python

   s = Scene()
   s.resources_paths.append(r'c:/data') # append to the end of the list
   s.resources_paths.insert(0, r'c:/data/copy_of_very_official_stuff') # insert at top of list

The order of the list is important.
The list is considered to be ordered from most-official to least-official. So, for the default list, a resource in the `resources` subfolder of the DAVE installation is considered of higher rank than a resource with the same name in the users DAVE_assets folder.

In a typical workflow an asset would first be created in a local or project folder. Then it would be checked as approved. Once approved it would be moved to an official (write protected) folder.

Files and resources
--------------------
So how do we differentiate a "file" from a "resource"? And how do we get from a "resource" to the corresponding file?

Easy:
- Anything that needs to be obtained from the resource system starts with `res:`
- Anything else is a file.

So `res: cube.obj` means the file `cube.obj` from the resource paths. Similarly `c:\data\cube.obj` means the the file cube.obj from c:\data

Nodes that work with resources have a `.path` property. The path is read/write and can be set to either a file (str) or a resource (res: file). To obtain the file that the resource points to use the `.file_path` property. This is read-only.



Loading and saving resources
-----------------------------
The path to a resource can be obtained using Scene.get_resource_path(name). This will loop over the resources_paths **from top to bottom**. It will return the full path to the first items found. More official assets or resources take precedence over less official ones.

If a resource with the same name is present in both the `resources` directory and the `DAVE_models` directory then a link to the one in the `resources` directory is returned.

When saving resoures the folders are evaluated from bottom to top. The first folder with write access is used to save the item. So this is exactly opposite from loading resources. **A resource is saved in the least official folder.**

It is also possible to load or save resources using the full path. In that case the whole system is circumpassed.

Subfolders
~~~~~~~~~~~
The Scene object will *not* walk through sub-folders when looking for an asset or resource. This means that subfolders add to the uniqueness of the filename.
A file called `attempt1/box.obj` is different from a file `attempt2/box.obj`


Examples
==========

.. code-block:: python

    s = Scene()
    filename = s.get_resource_path('buoyancy cheetah.obj')  # will return the official buoyancy cheetah.obj

    s.save_asset('empty')                 # assets saved in home-folder / DAVE_assets / empty.dave_asset
    s.save_asset('subfolder/empty')       # assets saved in home-folder / DAVE_assets / subfolder / empty.dave_asset

    s.get_resource_path('empty.dave_asset')           #  will return "home-folder / DAVE_assets / empty.dave_asset"
                                                      # EXCEPT is a file named `empty.dave_asset` exists in the `resources` folder.
    s.get_resource_path('subfolder/empty.dave_asset') #  will return "home-folder / DAVE_assets / empty.dave_asset"

    s.save_asset(r'c:\data\test.abc')     # will save as c:\data\test.abs

Summary
========

- If a file with the same name exists in a more official location, then that file gets priority above a file with the same name in a less official location.
- Saving files without specifying the full path will store them in the least official folder
- The resources_paths can be edited either in constants.py or in the Scene object.
