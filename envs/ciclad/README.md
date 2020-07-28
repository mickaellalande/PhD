## CICLAD environments

- **ciclad_v0** (28/07/2020 updated version of my work environment + jupyter-lab + intake)

**Installation**:
```bash
conda create -n ciclad_v0
conda activate ciclad_v0

# Need to install first esmpy separatly (https://github.com/JiaweiZhuang/xESMF/issues/47#issuecomment-582421822)
conda install esmpy
conda install xesmf dask

# Need matplotlib<=3.2 for Proplot (https://github.com/lukelbd/proplot/issues/210)
# Need nodejs>=10.0 for installing dask extension in jupyter-lab
# xarray and other packages already installed with dask previously
conda install jupyter jupyterlab "nodejs>=10.0" psutil netcdf4 proplot cartopy "matplotlib<=3.2" intake-esm python-graphviz

# Fot testing xESMF
pip install pytest  
pytest -v --pyargs xesmf  #all need to pass

# Launch jupyter-lab on your own port (xxxx)
jupyter lab --port xxxx --ip 0.0.0.0 --no-browser

# SSH tunel on your own terminal (with the port + the CICLAD node)
ssh -L xxxx:cicladxx:xxxx login@ciclad2.ipsl.jussieu.fr

# Problem with dask extension
404 GET /dask/clusters?1595927028221 (172.20.3.252) 4.28ms referer=http://127.0.0.1:7227/lab

# New tunel for dask
ssh -L 8787:cicladxx:8787 login@ciclad2.ipsl.jussieu.fr

```
