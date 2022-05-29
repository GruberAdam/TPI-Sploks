# TPI-Sploks

## Comment faire fonctionner sploks  ?

## Table des matières
1. [Télécharger les fichiers nécessaires en local]()
2. [Installer la base de données]()
3. [Lancer l'application]()
4. [Manuel d'utilisation]()


## Installer le répository en local : 
Pour faire ça, vous avez seulement besoin de télécharger les 2 fichiers à la racine du projet.
Sploks.exe qui va être l'exécutable, et script.sql qui va contenir toutes les données de la base de données

## Installer la base de données
En ce qui concerne la base de données, je vous invite à installer MySQl workbench, et le service qui va avec,
pour pouvoir exéctuer le script que vous avez téléchargé.

Dans mysql il faudra créer un compte qui s'appelle "root" et qui a comme mot de passe "root.1234".
Bien évidemment, ce compte aura besoin d'avoir les droits de modification sur la base de donnée.

## Lancer l'application
Une fois tout cela effectué, il faut lancer le fichier qui s'appelle "Sploks.exe" téléchargé précédemment.
Si toutes les étapes ont bien été effectuées auparavant, vous devriez avoir un menu qui s'ouvre.

## Manuel d'utilisation
Maintenant que vous êtes sur l'application, dans le menu principal, seul le bouton "Inventaire" fonctionnera.
Si il n'y a pas d'erreur avec la base de données, une grande liste qui contient tout le stock doit s'ouvrir.

De là, vous avez 3 possibilités,

1. Filtrer le stock
2. Ajouter des articles
3. Modifier des articles

#### Filtrer le stock
Si vous souhaitez effectuer un filtre, les champs au-dessus des colonnes du stock sont à disposition pour cela.
Veuillez entrer les données souhaitées pour un filtre puis cliquez sur le bouton situé sur la droite "Filtrer"
pour lancer le filtre

#### Ajouter des articles
Si vous souhaitez ajouter des articles, vous devez tout simplement cliquer sur le bouton en haut à droite du stock
qui s'appelle "Ajouter des articles".
Une nouvelle fenêtre s'ouvrira avec différents champs à remplir. Si une erreur est présente sur le remplissage 
des champs l'application vous expliquera votre erreur.

Le bouton "Encore" permet de créer un article, tandis que le bouton "Quitter" permet seulement de quitter la page.

#### Modifier des articles
Si vous souhaitez modifier des articles, vous devez double-cliquer sur la ligne que vous souhaitez modifier dans le stock.
La vue détaillée de cet article s'ouvrir et vous avez maintenant la possibilité de modifier cet article.

Le bouton "Editer" permet de modifier les champs modifiables, oui parce que pas tous les champs sont modifiables, 
le code article par exemple. L'autre bouton, donc "Valider" permet d'effectuer les changements effectués. Bien evidemment,
si une valeur est interdite, l'application vous le fera comprendre.


#### Petites subtilités
Voilà les petites subtilités lorsqu'on souhaite utiliser l'application sans souris.

Dans le menu principal, les touches "a" "s" "d" "f", représente chaque menu dans l'ordre.
Donc "a" = Clients, "s" = Inventaire, "d" = Staff, "f" = Contrats.

Dans le stock, si vous appuyez sur "entrer" en ayant une ligne séléctionnée, cela simule un double clique.

Si vous êtes en train de naviguer avec les flèches directionnelles dans le stock et que vous souhaitez effectuer un filtre,
appuyez sur "echap" ou "escape".
