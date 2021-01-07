

Salut Mickaël,

Etienne Vignon au LMD est en train de mettre à jour le fichier landice de LMDZ. Tu peux voir nos échanges ci-dessous.

Des glaciers vont apparaître en Himalaya dans les runs LMDZ... Ce sera peut-être plus réaliste, mais le schéma de neige sur les glaciers est à la fois différent et antédiluvien par rapport à ORCHIDEE...

N'hésites pas à contacter Etienne si besoin...

Bonne journée

Martin


-------- Message transféré --------
Sujet : 	Re: fichier landice
Date : 	Thu, 7 Jan 2021 00:20:07 +0100
De : 	Martin MENEGOZ <martin.menegoz@univ-grenoble-alpes.fr>
Pour : 	Etienne Vignon <etienne.vignon@lmd.ipsl.fr>, gerhard krinner <gerhard.krinner@cnrs.fr>
Copie à : 	cecile agosta <cecile.agosta@lsce.ipsl.fr>, frederic.hourdin <hourdin@lmd.jussieu.fr>


Bonjour Etienne,

Meilleurs voeux à toi aussi!

Je m'étais déjà posé la question de savoir pourquoi il n'y a pas de glaciers en Himalaya dans LMDZ. Merci pour ton explication! En fait, comme je me suis pour l'instant toujours intéressé uniquement à la neige dans les configs Himalaya, il était finalement plus simple de ne pas avoir de glaciers dans cette région. Avec de la neige et des glaciers où la physique du modèle diffère, alors il y aura peut-être des complications pour ces zones de haute-montagne? ça va nous pousser à améliorer le modèle sur ces histoires de modules différents pour la neige et les glaciers...

Ceci dit, dans la config actuelle, il y a de la neige permanente en général là ou il y a des glaciers, donc la modification de landice ne devrait pas affecter outre mesure les simulations dans cette région?

En tout cas, merci pour cette démarche qui me semble la plus logique pour ce qui concerne le développement du modèle.

Bonne semaine

Martin

Le 06/01/2021 à 16:05, Etienne Vignon a écrit :
> Bonjour Gerhard, Martin,
>
> Très bonne année à tous les deux et tout mes vœux de bonheur pour vous, vos familles et les collègues grenoblois.
>
> Je vous propose une nouvelle résolution, non pas pour LMDZ pour l'année 2021, tenez vous bien, il s'agit de mettre à jour le fichier landiceref.
> Vous savez, ce fichier que l'on utilise dans l'initialisation de LMDZ pour calculer le pourcentage de surfaces englacées dans chaque maille.
> Je me suis récemment rendu compte que ce fichier, dont on a oublié la référence par ailleurs, est à 1° de résolution...ce qui peut être embêtant pour ceux qui souhaite faire des zooms
> à haute latitude/altitude.
> Cécile et moi venons de générer un nouveau fichier, en s'inspirant du masque du MAR et en utilisant les données de Schaffer
> (https://essd.copernicus.org/articles/8/543/2016/) pour le Groenland et l'Antarctique. On essaie de voir si on ne peut pas faire encore un peu mieux en utilisant les toutes dernières données de J. Mouginot.
> Pour les curieux, les fichiers sont là:
> https://enacshare.epfl.ch/d9FsbczSYQ43pGhXJCgiW
> et une figure de comparaison est en PJ.
>
> Vous remarquerez quelque chose d'important, l'ancien fichier ne comprenait aucun glacier de montagne (Andes, Himalaya ...) alors que le nouveau oui.
> Si on utilise donc le nouveau fichier, on peut donc s'attendre à ce qu'une partie des processus de surface au dessus des chaînes de montagnes ne soit plus traitée par Orchidée mais par LMDZ (ou qui sait peut-être par LMDZ-SISVAT dans un futur plus ou moins proche).
> Sur un bench en 48x36, ça fait des pourcentages de landice autour de 10-20% sur quelques points de grille (voir PJ) au dessus de l'Himalaya et des Rocheuses mais à haute résolution ça peut évidemment prendre des proportions plus grandes.
>
> Y voyez vous un problème? A priori c'est plutôt plus réaliste mais ça risque de compliquer un peu la tache pour ceux qui souhaitent regarder finement la neige en milieu montagneux (il faudra alors regarder séparément les sous-surfaces landice et land).
>
> Bien à vous,
>
>
> Étienne
>
> -------------------------------------------------------
> Étienne Vignon
> Laboratoire de Météorologie Dynamique
> Sorbonne Université, Tour 45-55, 3è étage, bureau 303
> Case postale 99, 4 place Jussieu, 75252 Paris Cedex 05
> etienne.vignon@lmd.ipsl.fr
> -------------------------------------------------------
