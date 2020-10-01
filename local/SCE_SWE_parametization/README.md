# SCE/SWE relationship

- Google Doc : https://docs.google.com/document/d/1gK69TtH3feRFu4q0MjmuouC8xG6Gcth6Qe9cbeY5vIM/edit?usp=sharing
- Simulations : https://github.com/mickaellalande/PhD/tree/master/Jean-Zay/SCA_parameterization


## Niu2007 (LMDZOR-STD-REF)

```fortran
! LMDZOR-STD-REF
frac_snow_veg(:) = tanh(snowdepth(:)/(0.025*(snowrho_ave(:)/50.)))
```

[Niu and Yang (2007)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2007JD008674)

Version actuelle dans Orchidée (sauf pour la fraction nobio) dans le fichier `condveg.F90` : [Niu2007.ipynb](Niu2007.ipynb) -> fonctionne plutôt bien donc l’idée serait de modifier celle-là en premier lieux.


## Niu2007-std (LMDZOR-STD-NY07-CUSTOM-200)

Je n’ai rien trouvé en biblio donc j’ai testé une formule qui m’inspirait :

```fortran
! LMDZOR-STD-NY07-CUSTOM-200
! frac_snow_veg(:) = tanh(snowdepth(:)/(0.025*(snowrho_ave(:)*(1+zstd_not_filtered(:)/200.)/50.)))
```

[Niu2007-std.ipynb](Niu2007-std.ipynb) -> utilisation du même principe que pour la densité en rajoutant un terme de std qui ne modifie pas la formule initiale et applatit la courbe pour l'écart-type de la topographie également comme montré dans [Swenson and Lawrence (2012)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2007JD008674). J'ai mis la division par 200 un peu au pif pour le moment.


## Swenson2012 

[Swenson2012.ipynb](Swenson2012.ipynb) -> parait top mais j’ai essayé de rajouter la densité et cela donne un comportement bizarre (autrement top pour la STD), mais d’ailleurs dans leurs papier la formule que je teste est seulement utilisée pour la depletion curve et une autre formule est utilisé pour les périodes d’accumulation. A voir à peut-être tester… le arccos permet d’aller tirer vers des courbes plus piquées (pour std < 200m) et au contraire presque inversées pour std > 200 m ce qui parait plus proche des obs (qui sont seulement locales dans leurs cas).

## Roesch2001

[Roesch2001.ipynb](Roesch2001.ipynb) -> version utilisée par Gerhard à l'époque, il y a de l’idée (formule assez proche finalement de la première), demande de modifier la formule et rajout de la densité à nouveau ?

---

Pour un premier test je pense tester l’option Niu2007-std qui me paraît la plus simple à implémenter sans faire péter la formule initiale. Sachant que c’est basé seulement sur mon feeling. 
