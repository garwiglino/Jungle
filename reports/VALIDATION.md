# Livraison 0.1 — état vérifié le 26/10/2026

## Vérification avant publication GitHub — 28/10/2026

Le jeu a été reconstruit et relancé avec le binaire officiel UZDoom 5.0.3 sous Linux/Xvfb/llvmpipe. Le réticule du HUD est désormais dessiné au centre de l'écran. Les contrôles de ressources passent pour 128 fichiers ; SHA256 du jeu publié : `99e630d00142d235b182f0d3bfc8baf9c772bed0c1b0d37fe19c92d778431c55`.

Le journal [github-validation.log](github-validation.log) vérifie le tir du fusil, son rechargement, le refus d'extraction avant la valise, la récupération, la sauvegarde/reprise, l'extraction et quatre assertions de parcours/vision. Dans cette séquence, le clic trop bref du pistolet n'a pas été enregistré. Le contrôle complémentaire [github-pistol-ai.log](github-pistol-ai.log), avec un appui tenu, confirme sa consommation de munition et les sept assertions d'IA/dégâts/mort. Le pilote GUI a été corrigé pour maintenir ce clic. Le résultat synthétique est dans [github-validation.json](github-validation.json).

Les mêmes limites s'appliquent : boucle d'objectif testée avec god/warp, absence de parcours humain complet en difficulté normale et d'écoute audio réelle. Aucun nouveau relevé de performance n'est revendiqué. Le lanceur Windows est fourni mais n'a pas été exécuté ici. Les armes restent les deux sprites procéduraux du prototype ; les références MAT 49 et bras conservées dans `art/` ne sont pas les ressources définitives intégrées.

**Prototype jouable, pas une mission finale de 15–20 minutes.** Les ressources graphiques et sonores restent provisoires. Aucun test humain complet en difficulté normale n'a été effectué.

## Exécution réelle

UZDoom officiel 5.0.3 exécuté sous Debian 13 x86_64, CPU virtuel AMD EPYC 9V74, Xvfb, Mesa llvmpipe OpenGL 4.5. Le lanceur fourni a été utilisé après extraction du binaire officiel et vérification de son SHA256. Les paquets optionnels de ressources dérivées de jeux commerciaux ont été retirés. L'IPK3 est le seul jeu chargé, sans IWAD Doom ni Freedoom. Le PK3 de diagnostic est ajouté uniquement pendant les essais.

Le journal `final-validation.log` est celui de la séquence finale avec les huit poses de sprites par arme. Le journal `launcher-audio.log` couvre les assertions d'IA/dégâts/mort et le chargement audio. Pas d'erreur de compilation ZScript, de texture ou de modèle manquant dans ces journaux. OpenAL ouvre **No Output** : les sons se chargent sans périphérique matériel ; aucune écoute ou validation de mixage n'est revendiquée. Absence de GENMIDI et séquenceur ALSA disponible : pas de musique OPL utilisée par le projet.

## Résultats

| Vérification | Méthode / résultat |
|---|---|
| Tir du fusil | Bouton de souris réel : chargeur réduit ; voir états CRIQUE_PROBE dans le journal |
| Rechargement du fusil | R réel : retour à 30 et réserve diminuée de la quantité transférée |
| Tir du pistolet | Changement par 1, clic réel : chargeur 12 → 11 |
| Animations d'armes | Sprites PNG exclusivement ; A–H pour chaque arme ; retrait/insertion/manipulation dans les états ZScript ; planche docs/armes-sprites.png |
| Extraction sans valise | Warp à la balise, E : complete reste 0 |
| Récupération | Warp au camp, E : recovered passe à 1 |
| Sauvegarde et reprise | save checkpoint, déplacement, load checkpoint : position, chargeur, réserve et recovered restaurés |
| Fin de mission | Retour à la balise et E : complete passe à 1, écran final affiché |
| Route ouest | PASS WEST_ROUTE : TryMove par pas de 8 avec collisions, ennemis retirés |
| Route est | PASS EAST_ROUTE, même méthode |
| Vue dans un couloir | PASS VISIBLE_SAME_CORRIDOR |
| Massif occultant | PASS CENTRAL_MASSIF_OCCLUDES |
| Cône visuel | PASS OUTSIDE_VISION_CONE |
| Accroupissement à 600 unités | PASS CROUCH_BEYOND_420 |
| Debout à 600 unités | PASS STANDING_WITHIN_850_ALERTS |
| Bruit à travers obstacle | PASS RADIAL_NOISE_INVESTIGATION_THROUGH_WALL : limite actuelle volontairement explicitée |
| Mêlée raptor | PASS RAPTOR_MELEE_DAMAGE : 12 points |
| Dégâts joueur / mort | PASS PLAYER_DAMAGE et PASS PLAYER_DEATH |
| Accessoires Blender | OBJ/UV/textures chargés sans erreur, caisse et bateau inspectés dans UZDoom ; captures crate.png et boat.png |
| Fichiers | CRC ZIP, décodage PNG, offsets de sprites, formats WAV et références UDMF vérifiés par tools/validate_build.py |

La séquence de récupération emploie **god et warp** pour isoler les systèmes. Ce n'est pas une traversée humaine de la mission. Le test d'IA place les acteurs de façon contrôlée et appelle leurs ticks ; il ne valide pas des tactiques de groupe. Les routes isolent les collisions des décors, pas les collisions d'une foule ennemie. La sauvegarde de diagnostic peut contenir l'invulnérabilité ; elle n'est pas une partie de départ distribuée.

## Mesures de rendu

Trois captures natives `bench`, après stabilisation, sur le moteur exécuté avec rendu logiciel llvmpipe ; fenêtre 1024×576 sur écran Xvfb 1280×720. Les informations brutes sont dans benchmarks.txt. Acteurs actifs, joueur invulnérable pour préserver la scène. Mesures ponctuelles, pas une médiane ni un p95 de trajet.

| Vue | Images/s rapportées | Sprites visibles | Éclairages dynamiques |
|---|---:|---:|---:|
| Départ vers jungle | 47 | 90 | 0 |
| Embarcation dans la crique | 50 | 2 | 0 |
| Camp depuis la caisse | 49 | 52 | 0 |

Ces relevés précèdent l'ajout des poses D–H d'armes ; la géométrie et les poses de repos sont identiques. Ils ne certifient pas la cadence des nouvelles animations. Les modèles Blender comptent 108 triangles (caisse) et 96 (bateau). Les comptes de carte et le hash du paquet actuel sont dans build.json. La configuration cible 1080p n'a pas été disponible ; aucune promesse de 60 images/s sur celle-ci.

## Problèmes corrigés pendant ce jalon

Ressources d'interface manquantes dans un lancement sans Doom ; faux murs visuels dus aux textures médianes des lignes internes ; arbres solides coupant les raccords entre chemins ; chemin de texture des modèles OBJ ; temporisation du pilote GUI lors d'un chargement de carte. Les rapports finaux font foi, les essais préliminaires ne sont pas distribués.

## Restant avant la première mission finale

Parcours humains complets sans commandes de test ; mesure des durées et équilibre ; collision/lecture de chaque rencontre ; recherche géographique approfondie ; remplacement des sprites et sons provisoires ; vraie végétation hybride ; relief, abris et passerelles détaillés ; briefing et arc de recherche de l'équipe disparue ; audio écouté et réglé ; performance sur PC cible ; tests des plateformes et résolutions ; contrôle de redistribution d'une éventuelle édition avec binaire moteur préinstallé. Ne pas étendre la campagne avant ces validations.
