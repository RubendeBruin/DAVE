import os
import shutil

os.chdir(r'C:\Users\Ruben\source\repos\DAVE')

# clean
shutil.rmtree(r'C:\Users\Ruben\source\repos\DAVE\dist')

# build
os.system('python setup.py sdist')

# get the filename of the created file
files = os.listdir(r'C:\Users\Ruben\source\repos\DAVE\dist')
file = files[0]

command = 'pip install dist/{}'.format(file)

print(command)

os.system(command)