# Environments

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

- For installing on HPC: https://github.com/mickaellalande/MC-Toolkit/tree/master/conda_environment_xarray_xesmf_proplot
- My xarray environment: https://github.com/mickaellalande/MC-Toolkit/tree/master/conda_environment_xarray_xesmf_proplot/xarray


```bash
conda env list

conda create --name myenv
conda create --name myclone --clone myenv

conda list --explicit > spec-file.txt
conda create --name myenv --file spec-file.txt


conda env export > environment.yml
conda env export --from-history > environment.yml
conda env create -f environment.yml
```

---

## PhD environments

- ~~phd_v2~~ (20/07/2020 work -> phd updated version for xarray -> html and proplot -> shading, made on CICLAD)
    - bug with the last version of Matplotlib 3.3 (https://github.com/lukelbd/proplot/issues/210)
- work_v1 (made the 24/06/2020 on Jean-Zay)
- work (made on CICLAD -> didn't work on Jean-Zay?)

## Proplot environments

- proplot_v0.6.4 (20/07/2020 for testing bar bug)

## Xarray environments

- xarray_v0.16.0 (21/07/2020 for testing time.encoding bug)

## ScipyConf environments

- scipyconf2020 (21/07/2020 for [SciPyConf 2020 tutorials](https://www.scipy2020.scipy.org/tutorial-information) + [videos](https://www.youtube.com/playlist?list=PLYx7XA2nY5Gde-6QO98KUJ9iL_WW4rgYf))