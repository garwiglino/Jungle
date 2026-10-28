# Architecture et limites

Version stable vérifiée le 26 octobre 2026 via l'API GitHub officielle : tag 5.0.3, commit 7910df7102033fd7754a317f3254f24101135926. Capture de la réponse dans `uzdoom-release-5.0.3.json`. Les notes annoncent notamment une correction de chargement des sauvegardes.

Documentation consultée dans les sources officielles au tag : README, LICENSE, docs/licenses/README.TXT, specs/udmf.txt, specs/udmf_zdoom.txt, wadsrc/static/zscript (Actor, PlayerPawn, Weapon, EventHandler, Screen), wadsrc/static/mapinfo/mindefaults.txt, wadsrc_extra/static/iwadinfo.txt, src/common/models/models_obj.cpp et src/r_data/models.cpp. Le wiki zdoom.org est inaccessible par le proxy (403) ; aucune consultation réussie de son contenu n'est revendiquée.

| Fourni par UZDoom | Spécifique au projet |
|---|---|
| Déplacement FPS, souris libre, saut, accroupissement, touche de vitesse | Proportions et équipement du Soldat, génération du niveau |
| Collisions secteurs/acteurs, hitscan, dégâts et état de mort | Armes originales, chargeurs, recul, rechargement et sons |
| Visibilité géométrique CheckSight | Cône, seuils de distance, patrouilles et états d'alerte |
| Sérialisation ZScript et menus de sauvegarde | Champs recovered, complete, chargeurs, position de bruit, mémoire ennemie |
| Options vidéo/audio, configuration des touches, automap | HUD, objectif, extraction et écran de réussite |
| Rendu OpenGL, modèles OBJ, sprites et textures PNG | Textures/sprites synthétiques, modèles Blender et sélection des budgets |

## Détection

Les ennemis évaluent le joueur toutes les 5 tics (35 tics/seconde). Vision : distance strictement inférieure à 850 unités debout, 420 accroupi, demi-angle 55 degrés ; vision à très courte distance sous 110 unités indépendamment de l'orientation. CheckSight doit réussir. La lumière et les feuilles ne modifient pas ces seuils. Le tir annonce la dernière position pendant 70 tics au fusil et 45 au pistolet. La course annonce pendant 5 tics. L'écoute atteint 1100 unités, sans occlusion ni propagation acoustique. Un ennemi entend une position et s'en approche ; il ne connaît pas ensuite automatiquement les déplacements silencieux.

Alerte visuelle conservée 210 tics après perte de vue ; puis investigation de la dernière position et retour à la patrouille. Patrouille dans un rayon d'environ 120 unités autour du point initial. Évitement par essai de déplacement puis rotation de 90 degrés, sans navigation globale. Raptors : attaque au contact, pas de tir. Miliciens : dispersion et cadence simples, aucune tactique de groupe. Le champ `mode` est observable avec un outil de test.

## Carte et performances

Échelle conventionnelle : 56 unités pour un humain (~1,75 m). Grille de construction 256 unités, couloirs de trois cellules et clairière ouverte. Les couloirs sont plus larges que leurs trajectoires de test ; végétation solide écartée des raccords. GrandArbre possède une collision cylindrique de rayon 22, le feuillage n'en possède pas. Caisse : rayon 34, hauteur 44 ; bateau : cylindre rayon 78, hauteur 30, approximation volontaire, pas de marche sur coque détaillée.

Pas de lumières dynamiques ni de particules météo. La végétation est opaque/découpée par alpha, nombre limité d'acteurs (voir build.json). Les modèles Blender ont 108 et 96 triangles. L'absence d'occlusion des billboards constitue une limite de l'infiltration, pas une propriété cachée. Pour la suite : troncs 3D et cartes de feuilles limitées, imposteurs de canopée, secteurs occultants et instrumentation de densité.

Cible de conception à valider : Linux/Windows x86_64, Ryzen 5 5600, 16 Go, GTX 1660 6 Go, 1920×1080, OpenGL, objectif 60 images/s. Cette machine n'est pas disponible ici. Machine d'essai : CPU virtuel AMD EPYC 9V74, Mesa llvmpipe OpenGL 4.5, Xvfb ; aucune comparaison avec une vraie carte graphique n'est valable. Avant extension : mesurer médiane et p95 des temps d'image sur un trajet fixe, trois exécutions, même configuration, dans la clairière et sous canopée ; ne pas extrapoler depuis le taux de tics 35 Hz.

## Tests

`tests/ZSCRIPT` ajoute des acteurs de diagnostic dans un PK3 séparé, exclu du jeu livré. `CriqueRouteTest` enlève les ennemis pour isoler les collisions du décor, puis fait progresser le joueur par TryMove de 8 unités dans chaque voie, sans noclip. Il vérifie aussi visibilité et occlusion par le massif. `CriqueAITest` examine cône, accroupissement, bruit, mêlée et mort dans des cas contrôlés. Ces essais ne certifient pas le comportement émergent d'une rencontre complète.

`tools/gui_test.py` pilote clavier/souris via xdotool sur DISPLAY=:99 et capture le rendu via ffmpeg. Il teste le tir réel, le rechargement, l'interaction, puis sauvegarde/reprise/extraction avec warps console. Il nécessite Xvfb, xdotool, ffmpeg et le PK3 de diagnostic. Ses captures sont des images du jeu, pas des images de concept. Les résultats et les limitations sont explicités dans reports/VALIDATION.md.
