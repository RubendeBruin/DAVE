"""Consider a mesh and a contact-ball.
The contact-ball has its meshes set to []. This means it reacts to all meshes.
But when the mesh is deleted, the contact-ball should not be deleted. At this moment it however is."""

from DAVE import *
def test_issue_112():


    s = Scene()

    # auto generated python code
    # By MS12H
    # Time: 2024-04-14 15:18:43 UTC

    # To be able to distinguish the important number (eg: fixed positions) from
    # non-important numbers (eg: a position that is solved by the static solver) we use a dummy-function called 'solved'.
    # For anything written as solved(number) that actual number does not influence the static solution

    def solved(number):
        return number


    # Environment settings
    s.g = 9.80665
    s.waterlevel = 0.0
    s.rho_air = 0.00126
    s.rho_water = 1.025
    s.wind_direction = 0.0
    s.wind_velocity = 0.0
    s.current_direction = 0.0
    s.current_velocity = 0.0



    # code for Frame
    s.new_frame(name='Frame',
               position=(0,
                         0,
                         0),
               rotation=(0,
                         0,
                         0),
               fixed =(True, True, True, True, True, True),
                )

    # code for Point
    s.new_point(name='Point',
              parent='Frame',
              position=(0,
                        0,
                        4))

    # code for Contactmesh
    mesh = s.new_contactmesh(name='Contactmesh', parent='Frame')
    mesh.trimesh.load_file(r'res: plane.obj', scale = (6,6,1), rotation = (0,0,0), offset = (0,0,0))

    # code for Contactball
    s.new_contactball(name='Contactball',
                      parent='Point',
                      radius=1,
                      k=9999,
                      meshes = [])

    # Limits

    # Watches

    # Tags

    # Colors

    s.delete('Contactmesh')

    s['Contactball']  # verify that Contactball was not deleted
