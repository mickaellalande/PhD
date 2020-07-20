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

- phd_v2 (20/07/2020 work -> phd updated version for xarray -> html and proplot -> shading, made on CICLAD)
- work_v1 (made the 24/06/2020 on Jean-Zay)
- work (made on CICLAD -> didn't work on Jean-Zay?)

## Proplot environments

- proplot_v0.6.4 (20/07/2020 for testing bar bug)
