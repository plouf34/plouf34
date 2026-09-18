---
name: transcription-pcsi
description: Transforme les photos/PDF de cours manuscrits PCSI de Clarisse (Maths, Physique, Chimie, SI - Lycée Louis Barthou) en pages HTML de référence autonomes, vérifiées scientifiquement, avec quiz final, puis les commit/push sur github.com/plouf34/prepabarthou. Utiliser dès que l'utilisateur envoie des photos de cours manuscrits ou un PDF de prof à transcrire, ou invoque /transcription-pcsi.
---

# Transcription des cours PCSI de Clarisse

Charge et applique intégralement le prompt maître stocké dans
`Prepa_barthou/PROMPT_TRANSCRIPTION.md` à la racine de ce dépôt — lis ce
fichier en premier avec l'outil Read avant de commencer toute transcription.

Ce fichier définit : le rôle, les règles de fidélité aux notations du prof,
la vérification scientifique des formules et des schémas (SVG, relecture en
plusieurs passes), le rendu LaTeX/MathJax, la gestion des passages
illisibles, le quiz obligatoire de 10 questions en fin de chapitre, le
gabarit HTML (`ch01-bases-optique-geometrique.html`), la convention de
nommage des fichiers, et le workflow de publication.

## Rappel du workflow de publication (à la fin de chaque transcription)

1. Nommer le fichier `NN-Date_Matière_Type_NomDuLienSourceSansAccents.html`
   (NN = prochain numéro disponible dans le sous-dossier concerné).
   Si le cours transcrit est une prise de notes manuscrite de Clarisse
   (pas un document du professeur), inclure le mot `Clarisse` dans le nom
   de fichier (ex. `..._Cours_Clarisse_...`) — l'index le classe
   automatiquement dans « 1. Cours Clarisse » ; tout fichier sans ce mot est
   classé dans « 2. Cours Profs » (documents récupérés sur le site du prof
   ou de Louis Barthou).
2. Le placer dans `Prepa_barthou/1ere_annee/<01_MATHS|02_PHYSIQUE|03_CHIMIE|04_SI>/`
   du dépôt `plouf34/prepabarthou`, branche `claude/pcsi-henri-iv-math-exercises-pubkis`.
3. Régénérer `Prepa_barthou/1ere_annee/index.html` avec le script
   `.claude/skills/transcription-pcsi/regen_index.py <repo_root>`, qui scanne
   le contenu réel des 4 sous-dossiers et répartit chaque matière en 2
   sous-parties « Cours Clarisse » / « Cours Profs » (ne pas régénérer
   l'index à la main ni se fier à une liste mémorisée — d'autres sessions
   peuvent avoir ajouté des fichiers entre-temps).
4. Commit puis push sur la branche ci-dessus.
5. Fournir une copie du fichier à l'utilisateur (pièce jointe/téléchargement)
   pour récupération locale.

Avant de committer : vérifier que les balises HTML/SVG sont équilibrées,
que le nombre de `$$` est pair, et que le quiz contient bien 10 questions.
