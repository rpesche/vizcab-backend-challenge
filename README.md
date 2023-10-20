# Exercice Vizcab : estimation de l'impact carbone d'un projet

## Contexte

L'objectif est de développer des fonctions d'API permettant de mettre en oeuvre une analyse de cycle de vie simplifiée d'un projet de construction.

Pour cela on considère un projet de trois bâtiments :

- un bâtiment de logement
- un bâtiment de bureaux
- un complexe sportif

### Données d'entrée

Un **bâtiment** `data/batiments.json` est défini par les caractéristiques suivantes :

- `id` (int) : un index unique identifiant le bâtiment
- `nom` (str) : le nom du bâtiment
- `surface` (float) : la surface du bâtiment
- `zoneIds` (List[int]) : la liste des identifiants uniques des zones constituant le bâtiment
- `usage` (int) : identifiant de l'usage du bâtiment défini dans le fichier de données `data/usages.json`
- `periodeDeReference` (int) : la période en années sur laquelle l'analyse de cycle de vie est effectuée


Les bâtiments sont découpés en **zones** `data/zones.json` pouvant avoir des usages différents. Les caractéristiques des zones sont les suivantes :

- `id` (int) : un index unique identifiant la zone
- `nom` (str) : le nom de la zone
- `surface` (float) : la surface de la zone
- `usage` (int) : identifiant de l'usage de la zone défini dans le fichier de données `data/usages.json`
- `constructionElements` (List[Dict[int, float]]) : liste des éléments de construction contenant leur identifiant unique ainsi que leur quantité (dont l'unité est définie dans le produit de construction). Cette liste se présente sous la forme `[{id: 0, quantite: 12.34}, ...]` et la quantité est par la suite utilisée pour calculer les impacts de chaque élément de construction d'une zone.

Les **produits de construction** `data/construction_elements.json` contiennent les impacts carbone unitaires pour chaque phase de la vie du produit. Les phases considérées sont :

- la production du produit
- la construction du bâtiment
- l'exploitation du bâtiment
- la fin de vie.

Les champs du produit de construction sont les suivants :

- `id` (int) : un index unique identifiant le produit
- `nom` (str) : le nom du produit
- `unite` (str) : l'unité de mesure du produit de construction
- `impactUnitaireRechauffementClimatique` (Dict[str, float]) : impact carbone unitaire en kg éq. CO₂/unité du produit de construction pour chaque phase du cycle de vie du produit. Cet objet se présente sous la forme `{production: 1.2, construction: 3.4, exploitation: 5.6, finDeVie: 7.8}` et les impacts unitaires sont par la suite multipliés par les quantités des produits présents dans les zones pour évaluer l'impact carbone.
- `dureeVieTypique` (int) : la durée de vie du produit considérée dans l'analyse en années


## Comment démarrer

Cloner le dépot afin de récupérer les données du projet :

- `data/batiments.json`
- `data/zones.json`
- `data/construction_elements.json`
- `data/usages.json`

## Instructions de l'exercice

L'objectif est de créer des fonctions d'API RESTful retournant les informations demandées.

Le langage de programmation choisi peut être du python ou du javascript/typescript. Le choix des outils, framework, bibliothèques utilisées pour vous aider dans l'implémentation est libre.

### Niveau 1 : calcul de la surface et de l'usage des bâtiments

1. Créer une fonction d'API qui calcule la surface d'un bâtiment donné {i} qui est la somme des surfaces des zones le composant.
2. Créer la fonction calculant l'usage d'un bâtiment donné {i} et retournant le label de l'usage corespondant. Dans le cas d'un bâtiment contenant des zones d'usage différent, l'usage d'un bâtiment est l'usage représentant la plus grande surface dans ce bâtiment.

### Niveau 2 : calcul de l'impact carbone d'un bâtiment

Implémenter une fonction d'API calculant l'impact sur le réchauffement climatique d'un **bâtiment** {i} sur **tout son cycle de vie** à partir des instructions de calculs suivantes (il n'est pas nécessaire de faire des fonction d'API pour les calculs intermédiaires).

#### Calcul d'impact d'un produit de construction

L'impact carbone
<a href="https://render.githubusercontent.com/render/math?math=I" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I" title="I"/></a>
 d'un produit de construction pour une phase de cycle de vie donnée est calculé à partir des impacts unitaires
<a href="https://render.githubusercontent.com/render/math?math=I_U" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I_U" title="I_U"/></a>
des produits de construction et de la quantité
<a href="https://render.githubusercontent.com/render/math?math=Q_j" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=Q_j" title="Q_j"/></a>
présente dans la zone {j}.

##### Production

L'impact carbone d'un produit de construction de la zone {j} pour la phase de production :

<a href="https://render.githubusercontent.com/render/math?math=I_{production\,j} = I_{Uproduction} \times Q_{j}" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I_{production\,j} = I_{Uproduction} \times Q_{j}" title="I_{production\,j} = I_{Uproduction} \times Q_{j}"/></a>

##### Construction

L'impact carbone d'un produit de construction de la zone {j} pour la phase de construction :

<a href="https://render.githubusercontent.com/render/math?math=I_{construction\,j} = I_{Uconstruction} \times Q_{j}" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I_{construction\,j} = I_{Uconstruction} \times Q_{j}" title="I_{construction\,j} = I_{Uconstruction} \times Q_{j}"/></a>

##### Exploitation

L'impact carbone d'un produit de construction de la zone {j} pour la phase d'exploitation :

<a href="https://render.githubusercontent.com/render/math?math=I_{exploitation\,j} = \left(R_p \times I_{Uexploitation} %2B (R_p - 1) \times (I_{Uproduction} %2B I_{Uconstruction} %2B I_{Ufindevie})\right) \times Q_{j}" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I_{exploitation\,j} = \left(R_p \times I_{Uexploitation} %2B (R_p - 1) \times (I_{Uproduction} %2B I_{Uconstruction} %2B I_{Ufindevie})\right) \times Q_{j}" title="I_{exploitation\,j} = \left(R_p \times I_{Uexploitation} %2B (R_p - 1) \times (I_{Uproduction} %2B I_{Uconstruction} %2B I_{Ufindevie})\right) \times Q_{j}"/></a>

avec
<a href="https://render.githubusercontent.com/render/math?math=R_p"  target="_blank"><img src="https://render.githubusercontent.com/render/math?math=R_p" title="R_p"/></a>
le facteur de renouvellement dépendant du produit de construction {p} et du bâtiment {i} par :
<a href="https://render.githubusercontent.com/render/math?math=R_p%20\doteq%20R_{p\,i}%20=%20\text{Max}\left(1,%20\frac{\text{periodeDeReference}_i}{\text{dureeVieTypique}_p}\right)"  target="_blank"><img src="https://render.githubusercontent.com/render/math?math=R_p%20\doteq%20R_{p\,i}%20=%20\text{Max}\left(1,%20\frac{\text{periodeDeReference}_i}{\text{dureeVieTypique}_p}\right)" title="=R_p%20\doteq%20R_{p\,i}%20=%20\text{Max}\left(1,%20\frac{\text{periodeDeReference}_i}{\text{dureeVieTypique}_p}\right)"/></a>

##### Fin de vie

L'impact carbone d'un produit de construction de la zone {j} pour la phase de fin de vie :

<a href="https://render.githubusercontent.com/render/math?math=I_{findevie\,j} = I_{Ufindevie} \times Q_{j}" target="_blank"><img src="https://render.githubusercontent.com/render/math?math=I_{findevie\,j} = I_{Ufindevie} \times Q_{j}" title="I_{findevie\,j} = I_{Ufindevie} \times Q_{j}"/></a>

##### Total cycle de vie

L'impact carbone sur le cycle de vie total d'un produit de construction est la somme des impacts des différentes phases : production, construction, exploitation et fin de vie.

#### Calcul d'impact d'une zone

L'impact carbone sur le cycle de vie total d'une zone est la somme des impacts de ses éléments de construction.

#### Calcul d'impact d'un bâtiment

L'impact carbone sur le cycle de vie total d'un bâtiment est la somme des impacts de ses zones.

### Questions BONUS

1. Mettre en place les urls d'API correspondant aux endpoints implémentés
2. Quel serait l'outil que vous utiliseriez pour documenter l'API
3. Ecrire un fichier de configuration Docker pour déployer cette API

## Ce qu'on attend de vous

- Ce test sert de base à une discussion, les méthodes employées sont plus importantes que le résultat.
- Ce test pouvant être un peu long l'objectif n'est pas de finir tous les niveaux mais de mettre l'accent sur la structure du code, la qualité de l'implémentation et la clarté des messages de commits.
- En cas de questions, n'hésitez pas à envoyer un message pour demander des précisions ou des explications.
