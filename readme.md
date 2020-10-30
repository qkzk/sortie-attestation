---
title: "Generateur d'attestation dérogatoire"
author: "qkzk"
date: "2020/10/30"

---

## Le générateur : [sortie-attestation.herokuapp.com/](https://sortie-attestation.herokuapp.com/)

# Générateur d'attestation dérogatoire

Pour éviter d'en imprimer une, génère une attestation format PDF

# ÉTAPES

- [x] Page avec formulaire
- [x] Remplir une page avec flask
- [x] Générer un pdf avec pandoc
- [x] Générer un pdf depuis Python
- [x] Intégrer le tout
- [x] Héberger sur Heroku

# Heroku

Difficile d'installer texlive... mais ça va finit par marcher

# Précisions diverses 

1. rien n'est conservé. Ni le contenu du formulaire, ni le fichiers pdf,
2. n'ayant pas installé "tous anti covid", je n'ai aucune idée de ce à
    quoi l'attestation qu'il génère ressemble.
3. J'ai utilisé l'attestation disponible [ici](https://www.interieur.gouv.fr/Actualites/L-actu-du-Ministere/Attestations-de-deplacement), 
    plus précisemment [celle là](https://www.interieur.gouv.fr/content/download/124829/999546/file/30-10-2020-attestation-de-deplacement-derogatoire.txt?#xtor=AD-322).
4. Pensez à compléter la ville et le code postal dans le champ adresse...

