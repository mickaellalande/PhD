Bonjour Cécile, Mickael, Martin

Je mets aussi Fred, Frédérique et Laurent en copie pour qu'ils puissent suivre nos échanges.

Suite au dernier poihl, j'ai généré un nouveau fichier relief à partir du fichier high résolution (0.0625°) du GMTED utilisé par Mickael corrigé pour l'Antarctique et le Groenland. J'ai également généré de nouveaux fichiers landiceref (very High Resolution (1min) and High resolution(0.0625°)), avec ou sans les glaciers de montagnes (voir figure en pièce jointe). Références et détails sont donnés dans les attributs des netcdfs. Pour info, Cécile est même en train de voir si on ne peut pas faire encore mieux pour les masques landice en utilisant le must du must des données (celles de J. Mouginot).

Les anciens et nouveaux fichiers sont ici:

https://enacshare.epfl.ch/djfBtAZzDr28sMdRPQ5Eg

Je suis preneur de tout commentaire/remarque sur ces fichiers. Si vous avez 5 min pour jeter un coup d'oeil ce serait super.

Pour info, suite à la formation d'Orchidée aujourd'hui j'ai contacté Catherine Ottlé concernant le traitement de la neige sur les glaciers et les histoires de bio/nobio. J'ai copié mon mail et la réponse en dessous du mail. En gros: plus de nobio dans la nouvelle version d'Orchidée.

Merci d'avance pour vos retours, 
Bien à vous,
Étienne



Compte tenu des problèmes de codage de la variable frac-nobio et
d'erreurs dans les bilans d'eau recensé par Nicolas Vuichard, Jan
Polcher et Agnès Ducharne sur le wiki d'ORCHIDEE:

https://forge.ipsl.jussieu.fr/orchidee/wiki/Documentation/Frac_Nobio

nous ne travaillons maintenant qu'avec des cartes de land cover sans
NOBIO. Les zones de glaciers, de villes, de lacs, etc.. (bien
identifiées dans les cartes initiales de l'ESA à 300m de résolution) ont
toutes été regroupées avec le sol nu et sont traitées comme du sol nu
par ORCHIDEE. Je ne sais pas bien ce qui se passe quand on couple avec
LMDZ: j'imagine que le Landice mask prend le dessus? et que cela peut
peut être entrainer des soucis de fermeture des bilans d'eau comme ceux
documentés par Nicolas sur le wiki?

Avec Sylvie Charbit, Christophe Dumas et Fabienne Maignan, nous avons
travaillé à adapter le modèle de neige 3 couches sur le Groenland et
avons vérifié la fermeture des bilans, mais j'avoue qu'il faudrait qu'on
refasse un point à ce sujet. Et le travail est un peu en standby depuis
l'année dernière.

-------------------------------------------------------
Étienne Vignon
Laboratoire de Météorologie Dynamique  	
Sorbonne Université, Tour 45-55, 3è étage, bureau 303
Case postale 99, 4 place Jussieu, 75252 Paris Cedex 05
etienne.vignon@lmd.ipsl.fr
-------------------------------------------------------