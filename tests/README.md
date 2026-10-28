# Reproduire les essais

Les acteurs de test ne sont pas inclus dans dist/crique.ipk3.

```sh
python3 tools/build_tests.py
./lancer.sh -file build/tests.pk3
```

Dans la console (touche ` ou touche assignée dans Options), saisir :

- `summon CriqueProbe` : journal de santé, objectif, chargeur, réserve et position.
- `summon CriqueRouteTest` : supprime les ennemis, vérifie les deux itinéraires par collision réelle et deux cas de visibilité. À utiliser dans une partie jetable.
- `summon CriqueAITest` : cas contrôlés de détection, dégâts et mort ; tue le joueur à la fin, volontairement.
- `summon CriqueViewBoat` / `summon CriqueViewCrate` : positionne une caméra de vérification des accessoires.

Pour la séquence clavier/souris, installer Xvfb, xdotool et ffmpeg, démarrer Xvfb sur :99 et le jeu avec le PK3 de diagnostic, puis `python3 tools/gui_test.py`. La séquence est destinée à une session de test isolée avec aucune autre fenêtre de jeu ; elle modifie l'état de la partie, utilise god et warp et écrit un checkpoint. Une reprise manuelle normale n'est pas remplacée par cette séquence. Le lanceur du jeu normal ne charge pas ce PK3.

Logs des essais de cette livraison : reports/final-validation.log (boucle), reports/launcher-audio.log (détection, dégâts et mort), reports/benchmarks.txt (rendu statique, si produit). Aucun résultat n'est déduit seulement de la compilation.
