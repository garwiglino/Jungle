# CRIQUE — Opération Lisière / prototype 0.1

FPS solo autonome pour **UZDoom 5.0.3**, avec ressources propres. Première tranche technique jouable ; **ce n'est pas encore la mission aboutie de 15–20 minutes**. Environ 3–8 minutes de parcours prévu, durée humaine non mesurée. Secteur fictif de Guyane, milice fictive sans identité ethnique ou communautaire attribuée, présence de dinosaures explicitement fantastique.

**Téléchargement :** [Code → Download ZIP](https://github.com/garwiglino/Jungle/archive/refs/heads/main.zip), puis extraire l'archive. Le jeu déjà construit est `dist/crique.ipk3`. Voir le **[guide de test Linux / Windows](docs/TESTER.md)**. Cette version demande un ordinateur : pas de lancement dans le navigateur ni sur téléphone validé. Les essais artistiques de MAT 49 et de bras sont conservés dans `art/`, avec leur état ; ils ne constituent pas les armes définitives intégrées.

## Lancer sous Linux x86_64

Depuis un terminal dans ce dossier :

```sh
chmod +x lancer.sh
./lancer.sh
```

Python 3, accès Internet au premier lancement (33 Mo), session graphique et OpenGL 3.3+ nécessaires. Le lanceur télécharge la version officielle épinglée, vérifie son SHA256 et l'extrait sans FUSE ni privilèges. Le moteur n'est pas inclus dans l'archive distribuable. Le téléchargement ne demande aucun IWAD Doom. Les lancements suivants sont hors ligne. Options audio/vidéo et commandes : Échap → Options.

Pour utiliser une installation existante :

```sh
UZDOOM_BIN=/chemin/vers/uzdoom ./lancer.sh
```

Windows : extraire UZDoom 5.0.3 officiel dans `runtime/uzdoom/`, puis double-cliquer sur `lancer.bat` ; voir [le guide](docs/TESTER.md). macOS : charger ce même IPK3 avec UZDoom officiel. **Ces plateformes n'ont pas été testées.**

## Mission et commandes

Débarquement au sud. Suivre la berge vers le nord ; choisir le chemin ouest ou est autour du massif central. Au camp, trouver la valise jaune sous l'abri, approcher et appuyer sur **E**. Revenir à la balise verte dans la crique du départ, puis **E** pour extraire. Un écran confirme la fin.

| Action | Touche initiale |
|---|---|
| Déplacement | W A S D (configurable pour AZERTY dans Options) |
| Regarder / tirer | Souris / bouton gauche |
| Marche rapide | Maj maintenu (course automatique désactivée au lancement) |
| Accroupissement / saut | Ctrl / Espace |
| Pistolet / fusil | 1 / 2 |
| Rechargement / interaction | R / E |
| Carte / menu | Tab / Échap |
| Sauvegarde rapide / reprise | F6 / F9, choisir d'abord un emplacement |

Les deux armes possèdent des chargeurs distincts (12/30), une réserve commune abstraite dans ce prototype, recul, huit poses de sprites (repos, éclair, recul, abaissement, retrait du chargeur, insertion, manipulation et retour) et sons synthétiques. Les boîtes de munitions et trousses se ramassent au contact. La carte n'impose pas d'éliminer tous les ennemis.

## Ce qui est implémenté

- Carte UDMF avec départ fluvial, deux itinéraires reliés, clairière de camp et abri couvert ; géométrie très simple.
- Deux armes originales, projectiles instantanés, impacts de poussière, chargeurs et rechargement.
- Huit miliciens et quatre raptors : patrouille locale, cône de vision, enquête sur bruit, alerte avec mémoire ; dégâts à distance ou au contact.
- Objectif de récupération, interaction, retour et écran de réussite ; santé et mort.
- HUD propre, menus moteur conservés avec graphismes remplacés, sauvegarde des champs ZScript.
- Textures/sprites/sons procéduraux originaux ; accessoires Blender OBJ intégrés (caisse et embarcation).

## Limites à connaître

Tous les assets sont **provisoires**, pas des concepts présentés comme une production terminée. Les huit directions des sprites existent techniquement mais leurs poses restent insuffisamment différenciées. Animations sommaires. Les armes et toutes leurs animations de vue subjective sont exclusivement en sprites ; un éventuel modèle Blender ne servira qu’au rendu des images. Végétation encore en billboards, sans canopée 3D. Pas de musique originale ni de véritables enregistrements d'ambiance de Guyane. Le bateau est un volume de test, pas une pirogue réaliste finalisée. Pas de bâtiments dégradés détaillés, passerelles, relief naturel abouti ni météo.

La vue des ennemis est arrêtée par la géométrie, **pas par les feuilles en sprites**. Le bruit utilise un rayon sans atténuation par les murs. Pas d'écoute des pas normaux ; la course et le tir signalent une position. L'IA suit une direction avec évitement élémentaire, peut se coincer, ne calcule pas d'itinéraire tactique et ne coopère pas. Les détails et essais sont dans [docs/TECHNIQUE.md](docs/TECHNIQUE.md).

Le parcours géométrique des deux voies a été testé ; **un passage humain complet en conditions normales, sans commandes de test, reste à réaliser**. L'essai de la boucle objectif/sauvegarde/extraction utilise des déplacements console. L'audio a été chargé, mais son mixage n'a pas été écouté sur un périphérique réel. Aucun objectif de performance sur PC de joueur n'est certifié.

## Construire et étendre

```sh
python3 -m pip install -r requirements.txt
# Facultatif, seulement pour régénérer les accessoires 3D :
blender -b -t 2 --python tools/blender_props.py
python3 tools/build.py
```

`src/` contient les définitions et le ZScript ; `tools/build.py` produit les ressources et la carte, puis `dist/crique.ipk3`. Les modèles `.blend` sont inclus comme sources mais exclus de l'IPK3. Pillow testé : 12.3.0 ; Blender testé : 4.3.2. UZDoom construit ses nœuds à l'ouverture de la carte. Extraire `maps/MAP01.wad` de l'IPK3 pour éditer dans Ultimate Doom Builder ou SLADE (non installés/testés ici). Une reconstruction remplace la carte générée : sauvegarder les modifications manuelles ailleurs avant de rebâtir.

Une nouvelle arme hérite de `Fusil` et se déclare dans `Soldat`; un nouvel ennemi hérite de `Milicien` ; les numéros d'éditeur sont dans `MAPINFO`. Une prochaine mission pourra être un autre WAD UDMF, déclaré dans `MAPINFO`, avec son propre état d'objectif.

Voir [docs/PRODUCTION.md](docs/PRODUCTION.md), [docs/CONTEXTE.md](docs/CONTEXTE.md), [docs/LICENCES.md](docs/LICENCES.md), [reports/VALIDATION.md](reports/VALIDATION.md) et [docs/assets.json](docs/assets.json).
