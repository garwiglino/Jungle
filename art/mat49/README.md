# Version active : sprite peint

La proposition active est désormais [painted/README.md](painted/README.md), avec le rendu peint initial et une prise abaissée. Elle contient une seule pose de repos. Les rendus Blender ci-dessous ont été rejetés par l’utilisateur pour leur style et ne constituent plus la direction artistique retenue.

---

# MAT 49 — pose reconstruite et sprites A–H

La prise de l'image peinte précédente était incorrecte : le sprite faisait lire une main saisissant le flanc du boîtier. Cette révision utilise une scène Blender originale, puis des rendus PNG. Dans la scène, la poignée est sous l'arrière du boîtier et la main droite entoure cette poignée ; la main gauche soutient le logement de chargeur par-dessous. Le modèle est un accessoire de jeu stylisé, pas une réplique historique certifiée.

## Résultat et limites

- Huit poses de sprites : A repos, B tir, C recul, D abaissement, E retrait du chargeur, F insertion, G redressement, H retour.
- MAT49Preview devient une arme de prototype utilisable : chargeur 32, tir automatique, rechargement, réserve abstraite commune au prototype. Sons précédents réutilisés provisoirement.
- Toutes les images en jeu sont des **sprites PNG 320×200 RGBA**, origine grAb (0,22). Aucun modèle 3D d'arme dans UZDoom. Blender ne sert qu'à la production des images.
- Axe de l'arme x=160 ; réticule dessiné séparément au centre de l'écran par le HUD.
- Manches avec camouflage Tiger Stripe procédural, tenu de coupe inspirée TAP-47. Motif, tissus et mains encore simplifiés. Le rendu est plus simple et plus géométrique que la précédente image peinte ; il ne reprend pas sa finition.
- Les gestes de rechargement restent des poses de prototype ; absence de verrouillage/déverrouillage détaillé, d'animation spécifique de culasse et de vrais sons MAT 49.

L'ancienne image est archivée dans `legacy/previous-side-grip.png`, jamais chargée par le nouveau PK3. Elle ne doit pas être confondue avec la correction.

## Reproduire

```
blender -b -t 4 --python art/mat49/blender/build_pose.py
python3 art/mat49/export_sprite.py
./lancer.sh -file dist/mat49-preview.pk3
```

Console du jeu : `give MAT49Preview`, puis `use MAT49Preview`. Tir et rechargement : souris gauche et R. Les armes précédentes restent disponibles avec 1 et 2. Le PK3 MAT 49 n'est pas chargé par défaut.

Sources : `blender/build_pose.py`, `blender/mat49-pose.blend` ; rendus haute résolution `blender/MAT4[A-H]0-source.png` ; export technique `blender/export_sprites.py` ; états ZScript `preview/ZSCRIPT`. Tous les matériaux de ce modèle sont procéduraux ; aucune texture photographique ou image générée précédente n'est projetée dessus.

## Vérifications réelles

Blender 4.3.2 / Cycles CPU, 64 échantillons, 640×400 avec alpha ; import nearest-neighbor en 320×200. UZDoom 5.0.3 charge l'add-on sans erreur. Journal `reports/mat49-corrected.log` : chargeur 32 au départ, 26 après une rafale réelle, retour à 32 et réserve 150→144 après R. Capture réelle `reports/mat49-pose-corrigee.png` et vidéo `reports/mat49-tir-recharge.mp4`.

Cette révision a reçu un contrôle de chargement, de rendu, de tir et de rechargement. Elle ne certifie pas une nouvelle traversée complète de la mission, les sauvegardes avec cet add-on, ni les performances sur machine cible.
