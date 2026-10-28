# Tester CRIQUE

Le fichier jouable est `dist/crique.ipk3`. Il contient les ressources du jeu et ne demande aucun fichier commercial Doom. Le moteur requis est **UZDoom 5.0.3**. Les références d'armes et de bras dans `art/` ne remplacent pas les sprites provisoires du prototype.

## Télécharger

Sur [le dépôt](https://github.com/garwiglino/Jungle), choisir **Code → Download ZIP**, puis extraire complètement l'archive. On peut aussi cloner :

```sh
git clone https://github.com/garwiglino/Jungle.git
cd Jungle
```

Il n'est pas nécessaire de reconstruire le projet pour jouer.

## Linux x86_64 — plateforme testée

Python 3, une session graphique et un pilote OpenGL 3.3 ou supérieur sont nécessaires. Dans le dossier extrait :

```sh
chmod +x lancer.sh
./lancer.sh
```

Le premier lancement télécharge le moteur officiel (environ 33 Mo) et vérifie son SHA256. Les suivants peuvent se faire hors ligne. Aucune installation de Blender ou Pillow n'est nécessaire pour jouer.

## Windows — lanceur fourni, plateforme non testée ici

1. Télécharger l'archive Windows sur [la publication officielle UZDoom 5.0.3](https://github.com/UZDoom/UZDoom/releases/tag/5.0.3).
2. Extraire **tout son contenu** dans `runtime/uzdoom/` du projet : le fichier doit être `runtime/uzdoom/uzdoom.exe`, avec ses bibliothèques et ressources voisines.
3. Double-cliquer sur **lancer.bat**.

Une installation existante peut être sélectionnée depuis `cmd` :

```bat
set "UZDOOM_BIN=C:\Jeux\UZDoom\uzdoom.exe"
lancer.bat
```

## Téléphone et navigateur

Cette livraison n'a pas de version navigateur, Android ou iOS. Elle ne peut pas être jouée directement dans cette conversation ni sur la page GitHub. Le téléchargement peut être consulté depuis un téléphone, mais le lancement fourni demande un ordinateur compatible. Aucun port mobile n'a été validé.

## Premier parcours

1. Se déplacer avec **W A S D**, regarder avec la souris. Sur AZERTY, configurer **Z Q S D** dans **Échap → Options → Customize Controls**. Le moteur fournit aussi les réglages audio/vidéo.
2. Tester le tir au clic gauche, **R** pour recharger, **1 / 2** pour changer d'arme. **Maj** accélère, **Ctrl** accroupit, **Espace** saute.
3. Depuis le débarquement au sud, suivre la berge vers le camp au nord. Deux passages contournent le massif central. **Tab** affiche la carte.
4. Au camp, approcher la **valise jaune sous l'abri**, puis appuyer sur **E**. L'objectif affiché doit changer.
5. Utiliser **Échap → Save Game** pour créer une sauvegarde, s'éloigner, puis **Load Game** pour vérifier la reprise. **F6 / F9** servent ensuite aux sauvegardes/reprises rapides, avec les confirmations du moteur. Les fichiers restent dans `saves/`.
6. Revenir à la **balise verte au débarquement** et appuyer sur **E**. L'écran doit afficher **EXTRACTION REUSSIE**. Avant de récupérer la valise, la balise doit refuser l'extraction.

Le parcours visé du prototype est de 3–8 minutes, sans chronométrage humain validé. Les collisions des deux voies et les systèmes d'armes, d'objectif et de sauvegarde ont été vérifiés séparément ; une traversée humaine complète en conditions normales reste à faire. Les ennemis peuvent encore se coincer et leur audition traverse les murs dans un rayon fixe. Les feuilles en sprites ne bloquent pas leur vision.

## Signaler un problème

Noter le système, la version d'UZDoom, l'action, le résultat attendu et le résultat observé. Joindre une capture et, pour un problème de reprise, la sauvegarde concernée. Les limites et résultats techniques sont dans [VALIDATION.md](../reports/VALIDATION.md).
