# Inventaire et étapes suivantes

Le registre détaillé des fichiers générés est `assets.json`. Tous sont des ressources de prototype, sauf textes légaux. Aucun asset à acheter n'est intégré. Les achats éventuels ne sont pas autorisés implicitement par ce document.

| Catégorie | Présent | Production définitive prévue | Contrôle requis |
|---|---|---|---|
| Terrain / architecture | Grille UDMF, 8 matériaux synthétiques, abri | Modules manuels : berges, crique secondaire, roches, passerelle, camp, tôles et ruines utilitaires ; variantes procédurales contrôlées | Proportions, raccords, collision et lignes de vue |
| Accessoires | Caisse 108 triangles, bateau 96 triangles, fichiers Blender/OBJ | Refaire bateau crédible, radio, antenne, caisses variées ; Blender et génération 3D assistée si utile après revue des droits et coûts | Origine au sol, axe avant, UV, matériau, silhouette, volume de collision |
| Milice | Sprites provisoires à 8 orientations, trois frames | Modèle humain original animé, rendu 8 directions : repos, marche, tir, douleur, mort | Directions réellement distinctes, pieds fixes, silhouette et contraste |
| Raptors | Sprites provisoires | Modèle de fiction simple animé puis rendu multidirectionnel | Mêlée lisible, appuis, dimensions, corps au sol |
| Armes | Huit poses de sprites dessinées par arme | Animation Blender rendue exclusivement en sprites PNG de vue FPS : attente, tir, retour, retrait/entrée chargeur, verrou, changement, vide ; aucun modèle 3D d’arme affiché en jeu | Cadrage 4:3/16:9/21:9, cadence, synchronisation son/dégâts |
| Végétation | Deux billboards, tronc avec collision | Gros volumes 3D, cartes de feuillage alpha, variantes par zone ; canopée légère | Overdraw, nombre de cartes, pivots, occlusion, lecture des ennemis |
| Effets | Impact poussière et éclair dessiné sur arme | Impacts bois/boue/métal, éclat de bouche, eau et pluie limitée | Durée, lisibilité, nombre simultané |
| Interface | HUD et écran final simples, menus moteur | Briefing, direction, inventaire mission, transitions et options harmonisées | Résolutions, taille lisible, AZERTY, manette à tester |
| Audio | 7 WAV synthétiques mono | Foley, tirs crédibles, faune identifiée, ambiance spatialisée, musique discrète originale | Boucles, saturation, niveaux, distances et licence |

## Portes de validation

1. **Prototype actuel** : boucle mécanique, collisions des deux routes, sauvegarde et assertions élémentaires. Corriger les bugs révélés ; garder les rapports.
2. **Mission jouée normalement** : faire au moins trois parcours humains (ouest, est, infiltration), sans invulnérabilité/warp. Vérifier dégâts, blocages, reprises et munitions. Cette porte reste ouverte.
3. **Art vertical** : finir une berge, un segment de jungle et un poste du camp avant de multiplier les variantes. Comparer sprites et modèle 3D sur le même ennemi. Pas de concepts comptés comme ressources intégrées.
4. **Mission 15–20 minutes** : créer reconnaissance, indices de l'équipe disparue, risque dinosaurien, récupération puis retour/extraction ; ajouter du contenu utile, pas une vitesse artificiellement réduite. Tester la durée auprès de joueurs découvrant le niveau. Le prototype actuel n'atteint pas ce jalon.
5. **Optimisation et diffusion** : mesures 1080p sur configuration cible, inspection des licences et tests hors ligne sur une machine vierge. Pas d'extension de campagne avant réussite de ces portes.

## Fiche de contrôle asset

Pour chaque import : identifiant/version, source/auteur/licence, unité et hauteur, avant/haut/origine, transformation appliquée, normales, UV et résolution, texture/PBR converti au moteur, alpha propre, sprite offsets, collisions, états d'animation, nombre de triangles/acteurs/cartes alpha, coût sur scène de référence, capture UZDoom, statut et défauts. Les générateurs garantissent dimensions, origine et UV des accessoires ; leur collision est une approximation cylindrique. Le registre ne constitue pas une certification visuelle complète de chaque orientation.
