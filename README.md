# Rendering 2D images from 3D objects using OpenGL

## Installation
**Conda**
- `conda env create -f environment.yml`

**Virtual Environment**
- `virtualenv -p $(which python3.6) .venv`
- `source .venv/bin/activate`
- `pip install pygame pyopengl`

## Run
- For a sample illustration of pyOpenGL: `python -m play.main`
- For an example on how to load `.stl` files using pyOpenGL: `python -m play.load_stl`
