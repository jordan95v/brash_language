<h1>Brash - Projet de théorie des langages</h1>

Ce projet a pour but de créer un interpréteur pour un langage de programmation fictif, le Brash. Ce langage est un langage de programmation impératif, avec des variables, des boucles, des conditions et des fonctions.

Ce dernier prend inspiration du langage Bash et du python.

<h1>Table des matières</h1>

- [Exemple de code Brash](#exemple-de-code-brash)
  - [Hello world](#hello-world)
  - [Déclaration et affichage de variable](#déclaration-et-affichage-de-variable)
  - [Variables globales et locales](#variables-globales-et-locales)
  - [Opérateurs et sucre syntaxique](#opérateurs-et-sucre-syntaxique)
    - [Opérateurs de comparaison](#opérateurs-de-comparaison)
  - [Tableaux](#tableaux)
    - [Méthodes de tableaux](#méthodes-de-tableaux)
  - [Conditions](#conditions)
  - [Boucles](#boucles)
    - [Boucle while](#boucle-while)
    - [Boucle for](#boucle-for)
  - [Scope des variables](#scope-des-variables)
  - [Fonctions](#fonctions)
  - [Commentaires](#commentaires)
  - [Exemple de code complet](#exemple-de-code-complet)


# Exemple de code Brash

## Hello world

```
print("Hello world");
```

Première chose à faire quand on apprend un nouveau langage, afficher "Hello world".

## Déclaration et affichage de variable

```
my_first_var = 5;
print(my_first_var);
```

Code basique qui permet d'initialiser une variable et de l'afficher.

```
my_first_var, my_second_var = 5, 10;
```

Il est possible d'initialiser plusieurs variables en même temps.

## Variables globales et locales

Les variables sont locales par défaut, il faut utiliser le mot clé `global` pour les rendre globales.

```
my_first_var = 5;
global my_first_var;
```

Dans cet exemple, la variable `my_first_var` est devenue globale après être instanciée.

```
global my_first_var = 5;
```

Dans cet exemple, la variable `my_first_var` est globale dès sa déclaration.

## Opérateurs et sucre syntaxique

```
my_first_var = 5;
my_first_var += 5; // my_first_var = 10
my_first_var -= 5; // my_first_var = 5
my_first_var *= 5; // my_first_var = 25
my_first_var /= 5; // my_first_var = 5
my_first_var++; // my_first_var = 6
my_first_var--; // my_first_var = 5
```

Les opérateurs `+=`, `-=`, `*=`, `/=` permettent de faire une opération et d'affecter le résultat à la variable.
On appelle ça du sucre syntaxique.
Les opérateurs `++` et `--` permettent d'incrémenter ou de décrémenter une variable.

### Opérateurs de comparaison

```
my_first_var = 5;
my_second_var = 10;

my_first_var == my_second_var; // false
my_first_var != my_second_var; // true
my_first_var < my_second_var; // true
my_first_var > my_second_var; // false
my_first_var <= my_second_var; // true
my_first_var >= my_second_var; // false
```

Les opérateurs de comparaison permettent de comparer deux variables.
Il est possible d'enchaîner les opérateurs de comparaison.

## Tableaux

```
my_first_array = [1, 2, 3, 4, "hello", "you"];
print(my_first_array[0]); // Affiche 1
```

Les tableaux sont déclarés avec des crochets `[]`. Ils peuvent contenir des nombres, des chaînes de caractères ou la valeur de variables.
Pour accéder à une valeur, on utilise des crochets `[]` après le nom du tableau et on met l'index de la valeur à l'intérieur.
Les index commencent à 0.

### Méthodes de tableaux

Certains méthodes sont disponibles pour les tableaux.

```
my_first_array = [1, 2, 3, 4, "hello", "you"];
my_first_array.append(5); // Ajoute 5 à la fin du tableau
my_first_array.remove(2); // Supprime la première occurence de 2
```

On peut ajouter n'importe quel type de valeur à un tableau. Même un autre tableau.

## Conditions

```
if my_first_var == 5
then
    print("my_first_var is equal to 5");
else
    print("my_first_var is not equal to 5");
endif;
```

La construction d'une condition utilise les mots clés `if`, `then` et `else`.
Il est possible d'imbriquer des conditions, et de ne pas mettre de `else`.

## Boucles

### Boucle while

```
while my_first_var < 10
do
    print(my_first_var);
    my_first_var++;
endwhile;
```

Tant que la condition est vraie, on exécute le code dans la boucle.

### Boucle for

```
for i=0; i<10; i++
do
    print(i);
endfor;
```

Le premier paramètre est le bloc d'initialisation, le deuxième est la condition et le troisième est le bloc d'incrémentation.
Bloc fait référence au code entre les `;`.

## Scope des variables

Les variables qui sont instanciées dans une boucle ou une condition sont locales à cette boucle ou cette condition.

```
for i=0; i<10; i++
do
    my_var = 5;
endfor;
print(my_var); // Erreur, my_var n'existe pas
```

## Fonctions

```
// Fonction sans paramètres
function my_function()
    print("Hello world");
endfunction;


// Fonction avec paramètres
function calculate(a, b)
    return a + b;
endfunction;
```

Les fonctions sont déclarées avec le mot clé `function` et se termine avec le mot clé `endfunction`.
Les paramètres sont séparés par des virgules.
Le mot clé `return` permet de retourner une valeur, et est coupe-circuit, c'est à dire que le code après le `return` ne sera pas exécuté.

## Commentaires

```
// Ceci est un commentaire sur une ligne
```

Les commentaires sur une ligne sont précédés par `//`.

## Exemple de code complet

Voici un code qui permet de calculer la somme des nombres de 1 à 10.

```
sum = 0;

for i = 1; i < 20; i++
do
    if i < 10
    then
        sum += i;
    endif;
endfor;
print(sum);
```
