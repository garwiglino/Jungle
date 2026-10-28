> **Pose non validée** : le bloc poignée-chargeur avant reste dessiné sur le flanc gauche. La correction demandée consiste à le placer sous le boîtier, dans son plan central, avec la main gauche déplacée sous ce bloc. La tentative de retouche a été refusée par le service d’image ; aucune nouvelle image corrigée n’a été produite. Ne pas décliner les animations à partir de cette silhouette.

# MAT 49 — retour au sprite peint, prise abaissée

Cette proposition remplace visuellement le rendu Blender rejeté. L'image peinte précédemment approuvée sert de référence ; image_gen en a retouché la prise, avec main droite abaissée sous l'arrière du boîtier. Source RGBA : mat49-ready-source.png. Sprite d'inspection : preview/sprites/M49PA0.png, 320×200, origine grAb (0,22). Le réticule reste un élément indépendant du HUD, centré à la fenêtre.

**Une seule pose de repos est produite.** Le PK3 d'inspection n'utilise aucune frame Blender et désactive le tir. Il ne faut pas confondre ce nouvel aperçu avec l'ancienne arme de prototype animée. Les animations de tir et de rechargement peintes restent à produire ; le détail historique de la silhouette n'est pas certifié.

Depuis le projet :

```
python3 art/mat49/painted/export.py
./lancer.sh -file dist/mat49-painted-preview.pk3
```

Console : `give MAT49Preview`, puis `use MAT49Preview`. Charger uniquement ce PK3 MAT 49 : la version Blender définit la même classe et ne doit pas être chargée simultanément.

Contrôle effectué : PNG RGBA avec alpha, import dans UZDoom 5.0.3, chargement de la classe et inspection visuelle de la pose avec HUD. Capture réelle : reports/mat49-peint-corrige.png. Pas de nouvelle validation complète de mission, ni d'animation revendiquée.
