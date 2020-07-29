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
conda install jupyter jupyterlab "nodejs>=10.0" netcdf4 proplot cartopy "matplotlib<=3.2" intake-esm python-graphviz nbresuse nc-time-axis

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

# Monitor extension
# https://github.com/jtpio/jupyterlab-system-monitor
jupyterlab-system-monitor

# Code formatter
# https://jupyterlab-code-formatter.readthedocs.io/en/latest/installation.html
conda install nodejs
jupyter labextension install @ryantam626/jupyterlab_code_formatter
conda install -c conda-forge jupyterlab_code_formatter
jupyter serverextension enable --py jupyterlab_code_formatter
conda install black isort

```
