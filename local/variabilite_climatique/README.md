# Biais froid sur le Plateau Tibétain et projections climatiques (CMIP6)

[PAX7STAF - Variabilité Climatique et Environnementale](https://chamilo.univ-grenoble-alpes.fr/courses/PAX7STAF/index.php?id_session=0)

Mickaël LALANDE (mickael.lalande@univ-grenoble-alpes.fr) - Septembre 2020

## Installation de Miniconda/Anaconda

1. **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)**:
   (if you don't already have an installation of Anaconda/Miniconda -> Miniconda is lighter and allows to only install the packages that you need)

If you are on a cluster, try to install it on a different path than the default one (usually it takes some spaces and it is not recommended to have it in your *home*), otherwise make the default installation and put `yes` anytime it ask something.

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
sh Miniconda3-latest-Linux-x86_64.sh 

# This will automatically update your ~/.bashrc so that you can directly have conda in your path
Do you wish the installer to initialize Miniconda3
by running conda init? [yes|no]
[no] >>> yes

source ~/.bashrc  
```

You should have a `(base)` in front of your line in your terminal, that correspond to the **root** environment.

2.  **Add [conda-forge](https://conda-forge.org/docs/user/introduction.html)** and **update** your installation (optional but I recommend):  

```bash
conda config --add channels conda-forge  
conda config --set channel_priority strict  
conda update -n base -c defaults conda  
```

    3. **Create an environment**:

It is recommended not to use the **root** (base) environment so that you keep a clean installation (see the [note](https://conda-forge.org/docs/user/introduction.html) at the end of the page). 

```bash
conda create -n my_env jupyter # ... install any package you want
conda activate my_env
```

**Tip**: You can add `conda activate my_env` in your .bashrc so you don't have to activate it every time.

**Tip 2:** Once you have a environment set-up I advice you to save it (`conda list --explicit > spec-file.txt `) before to do any updates... sometimes you can break everything. Another option is to make versions of your environment, so that before an update or an install of a new package you can clone your environment (`conda create --name myenv_v1 --clone myenv_v0`) with a new version number for example (see https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html for more infos on environments). A good practice can be then to note which version of your environment you are using in your scripts so that you are sure to keep it to work even later.



## Installation de l'environnement de travail pour ce projet

1. **Installation à partir d'un fichier** (dans le dossier [env](env))

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#building-identical-conda-environments

Une des 3 commandes ci-dessous devrait fonctionner (en fonction du système d'exploitation, etc.), testez la première pour commencer :

```bash
conda env create -f phd_v3_fh.yml
conda env create -f phd_v3.yml
conda create --name myenv --file spec-file.txt
```

Ensuite activer l'environnement et lancer jupyter lab ou notebook :
```bash
conda activate phd_v3
jupyter lab
```


2. **Autre option : installation manuelle**

- **phd_v3** (30/07/2020 update from work + intake + jupyter-lab)

```bash
conda create -n phd_v3
conda activate phd_v3

# Need to install first esmpy separatly (https://github.com/JiaweiZhuang/xESMF/issues/47#issuecomment-582421822)
# It looks like it doesn't matter anymore about the order
conda install esmpy
conda install xesmf dask

# Need matplotlib<=3.2 for Proplot (https://github.com/lukelbd/proplot/issues/210)
# Need nodejs>=10.0 for installing dask extension in jupyter-lab
# xarray and other packages already installed with dask previously
conda install jupyter jupyterlab "nodejs>=10.0" netcdf4 proplot cartopy "matplotlib<=3.2" intake-esm python-graphviz nbresuse nc-time-axis

# Fot testing xESMF
pip install pytest  
pytest -v --pyargs xesmf  #all need to pass

# For automatically have other environments available
# https://github.com/Anaconda-Platform/nb_conda_kernels
# https://stackoverflow.com/questions/39604271/conda-environments-not-showing-up-in-jupyter-notebook
conda install nb_conda_kernels

# To get %matplotlib notebook working
# https://stackoverflow.com/questions/51922480/javascript-error-ipython-is-not-defined-in-jupyterlab
# https://github.com/matplotlib/ipympl
conda install ipympl

# Launch jupyter lab
jupyter lab

```
