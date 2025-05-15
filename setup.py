import os
from setuptools import setup, find_packages

# Para incluir el README.md como descripción larga.
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Un generador avanzado de progresiones de acordes MIDI basado en teoría musical."

setup(
    name="chorderizer",
    version="0.1.1",  # Versión inicial de tu proyecto
    author="Julio César Martinez", 
    author_email="julioglez.93@gmail.com",  
    description="Un generador avanzado de progresiones de acordes MIDI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julesklord/Chorderizer",  # URL del proyecto
    package_dir={"": "src"},  # Le dice a setuptools que los paquetes están en src/
    packages=find_packages(where="src"),  # Encuentra automáticamente el paquete 'chorderizer' en src/
    python_requires=">=3.7",  # Basado en el uso de type hints y f-strings
    install_requires=[
        "mido>=1.2.9",  # Dependencia principal
    ],
    entry_points={
        "console_scripts": [
            "chorderizer=chorderizer.chorderizer:main",  # Permite ejecutar 'chorderizer' desde la terminal
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha", # O Beta, Production/Stable según corresponda
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # Elige tu licencia y actualiza aquí
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Artistic Software",
        "Operating System :: OS Independent",
    ],
)