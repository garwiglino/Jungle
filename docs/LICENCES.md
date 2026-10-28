# Distribution autonome

Le jeu est un IPK3 avec IWADINFO et ses propres classes PlayerPawn, armes, ennemis, niveau, palette, textures, sons et interface. Aucun doom.wad, doom2.wad ou Freedoom n'est requis. Hériter des classes de base du moteur n'intègre pas les assets commerciaux de Doom.

UZDoom 5.0.3 est annoncé GPL-3.0-or-later par le README officiel. Les sources précisent des licences distinctes pour bibliothèques, marque et certains paquets de ressources. En particulier `docs/licenses/README.TXT` indique que `brightmaps.pk3`, `game_support.pk3` et `game_widescreen_gfx.pk3` dérivent de ressources de jeux sous copyright, et préconise `-DBUILD_NONFREE=no` pour une construction qui les exclut. Nos essais ont donc été refaits sans ces paquets. Le bootstrap les retire de son installation extraite, ainsi que lights.pk3, inutilisé.

**L'archive du projet ne redistribue pas le binaire moteur** : le lanceur télécharge la publication officielle 5.0.3, avec hash SHA256 fixé. Le code du jeu et ses outils sont distribués avec les sources sous GPL-3.0-or-later. Les ressources originales sont dédiées CC0-1.0, hors rendu typographique DejaVu (notice incluse dans LICENSES/DejaVu.txt) et ressources internes du moteur.

Pour une future édition avec moteur préinstallé : produire UZDoom avec BUILD_NONFREE=no, conserver mentions et licences du moteur et des bibliothèques, fournir le code source correspondant et les instructions de compilation requises par GPL, examiner les conditions de marque/branding et inclure les avis des polices et ressources. Ne pas supposer qu'un lien générique vers le dépôt remplit toutes les obligations d'une redistribution binaire. Cette édition n'est pas fabriquée ici.

Liens vérifiés : https://github.com/UZDoom/UZDoom/releases/tag/5.0.3 et https://github.com/UZDoom/UZDoom/tree/5.0.3 . Capture de la réponse API dans docs/uzdoom-release-5.0.3.json. Binaire officiel téléchargé SHA256 : 9c5166febc09cbf80c24612a78829037c953f38c4d986e36f8475ddd507e0228.

Aucune dépense ni acquisition de licence externe. Les textes de licence et ce registre doivent accompagner toute version partagée. Le code interne hérité d'UZDoom reste sous sa propre licence ; la dédicace CC0 ne s'y applique pas.
