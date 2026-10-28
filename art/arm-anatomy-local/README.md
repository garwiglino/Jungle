# Contrôle anatomique 3D — pas une version artistique finale

Cette scène sert à sortir de l'incohérence des profils générés séparément. Une seule géométrie de bras droit est utilisée pour toutes les caméras. La base anatomique est MakeHuman `base.obj`, explicitement CC0 dans l'en-tête de l'asset ; licence et provenance dans source/. Le bras droit est extrait, l'avant-bras et la main sont redressés ensemble par rotation, sans miroir ni permutation des doigts.

Les cinq vues sont de véritables rendus orthographiques Blender d'une même scène. Caméras à 0°, 90°, 180°, 270° et 45°, même cadrage et même échelle. Le côté du pouce définit une fois l'orientation du modèle. Le bouton de manchette est un seul objet 3D, pas un détail recréé dans chaque image.

**Limites** : maquette de contrôle uniquement. La manche, le motif procédural et la matière de peau ne reproduisent pas encore la finition réaliste des images approuvées. Les vues photo générées précédemment restent non validées comme turnaround cohérent. Ne pas présenter ce modèle comme une ressource de production terminée. Pas de rig, de poids d'animation ni d'intégration UZDoom.

Source de la géométrie : https://github.com/makehumancommunity/makehuman/blob/master/makehuman/data/3dobjs/base.obj
La licence CC0 et les auteurs figurent dans source/base.obj et source/LICENSE.ASSETS.md.

Reproduire :
```
blender -b -t 4 --python tools/build_anatomical_arm.py
```

Les scripts, données source et rendus sont conservés pour inspection. Les dimensions et proportions restent à vérifier avant production d'une manche finale. Aucun crédit Tripo n'a été utilisé.
