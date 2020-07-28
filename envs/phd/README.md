## PhD environments

- **phd_v3** (28/07/2020 update from work + intake + jupyter-lab)

**Installation**:

```bash
conda create -n phd_v3
conda activate phd_v3

# Need to install first esmpy separatly (https://github.com/JiaweiZhuang/xESMF/issues/47#issuecomment-582421822)
conda install esmpy
conda install xesmf dask

# Need matplotlib<=3.2 for Proplot (https://github.com/lukelbd/proplot/issues/210)
# Need nodejs>=10.0 for installing dask extension in jupyter-lab
# xarray and other packages already installed with dask previously
conda install jupyter jupyterlab "nodejs>=10.0" netcdf4 proplot cartopy "matplotlib<=3.2" intake-esm python-graphviz

# Fot testing xESMF
pip install pytest  
pytest -v --pyargs xesmf  #all need to pass

# For automatically have other environments available
# https://github.com/Anaconda-Platform/nb_conda_kernels
# https://stackoverflow.com/questions/39604271/conda-environments-not-showing-up-in-jupyter-notebook
conda install nb_conda_kernels

# Configure jupyter
# https://jupyter-notebook.readthedocs.io/en/stable/public_server.html
jupyter notebook --generate-config
gvim ~/.jupyter/jupyter_notebook_config.py

# https://stackoverflow.com/questions/42848130/why-i-cant-access-remote-jupyter-notebook-server
c.NotebookApp.allow_origin = '*'
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 7227
c.NotebookApp.open_browser = False

# Launch jupyter lab
jupyter lab

# SSH tunnel
ssh -L 7227:ciclad14:7227 mlalande@ciclad2.ipsl.jussieu.fr

```

**[Kernels for different environments](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments)**:

```bash
python -m ipykernel install --user --name phd_v3

# Launch jupyter-lab on your own port (xxxx)
jupyter lab --port xxxx --ip 0.0.0.0 --no-browser

# SSH tunel on your own terminal (with the port + the CICLAD node)
ssh -L xxxx:cicladxx:xxxx login@ciclad2.ipsl.jussieu.fr

# Problem with dask extension
404 GET /dask/clusters?1595927028221 (172.20.3.252) 4.28ms referer=http://127.0.0.1:7227/lab

# New tunel for dask
ssh -L 8787:cicladxx:8787 login@ciclad2.ipsl.jussieu.fr

```

- ~~phd_v2~~ (20/07/2020 work -> phd updated version for xarray -> html and proplot -> shading, made on CICLAD)
    - bug with the last version of Matplotlib 3.3 (https://github.com/lukelbd/proplot/issues/210)
- work_v1 (made the 24/06/2020 on Jean-Zay)
- **work** (made on CICLAD -> didn't work on Jean-Zay?)
