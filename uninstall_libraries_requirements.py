import subprocess

# Leer el archivo requirements.txt
with open('requirements.txt', 'r') as file:
    libraries = file.readlines()

# Eliminar los espacios en blanco alrededor de cada línea y eliminar comentarios
libraries = [lib.strip() for lib in libraries if not lib.startswith('#')]

# Desinstalar cada biblioteca
for lib in libraries:
    subprocess.run(['pip', 'uninstall', '-y', lib])
