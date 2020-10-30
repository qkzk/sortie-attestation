'''
titre:  Générateur d'attestation de déplacement dérogatoire
auteur: qkzk
date:   2020/10/30

Sert une page web avec un formulaire permettant de remplir rapidement
une attestation dérogatoire.

L'attestation est générée au format pdf puis envoyée à l'utilisateur.
'''
import io
import os
from datetime import date
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
import pypandoc


def get_text(text_path: str) -> str:
    '''retourne le contenu du fichier texte'''
    with open(text_path) as attestation:
        return attestation.read()


def fill_text(text: str, parsed_form: list, motifs : dict) -> str:
    '''rempli le texte avec les données reçues depuis le formulaire'''
    # TODO améliorer cette merde
    parsed_form[-3] = date.today()
    return text.format(*parsed_form, **motifs)


def parse_form(form: dict) -> list:
    '''récupère les données du formulaire et les ordonne dans une liste'''
    # TODO encore de la merde
    return [form.get(key) for key in LISTE_CHAMPS] + [form.get("nom")]


def parse_motif(form: dict) -> dict:
    '''crée un dictionnaire des cases à cocher depuis le formulaire'''
    motifs = {motif_possible: ' ' for motif_possible in MOTIFS}
    if 'motif' in form:
        motifs[form['motif']] = 'x'
    return motifs


def create_pdf(form: dict):
    '''crée le fichier pdf et écrase le précédent'''
    text = fill_text(TEXT, parse_form(form), parse_motif(form))
    pypandoc.convert_text(text,
                          'pdf',
                          format='md',
                          outputfile=OUTPUT_PATH)


def read_pdf_file(filepath):
    '''
    stackoverflow magic
    lit le contenu d'un fichier et le renvoie
    Permet d'effacer le fichier source ensuite et d'envoyer proprement
    le contenu.
    '''
    return_data = io.BytesIO()
    with open(filepath, 'rb') as binary_file:
        return_data.write(binary_file.read())
    return_data.seek(0)
    return return_data


TEXT_PATH = "app/text/attestation-de-deplacement-derogatoire.md"
TEXT = get_text(TEXT_PATH)
LISTE_CHAMPS = {
    "nom" : "Nom",
    "prenom" : "Prénom",
    "date_naissance": "Date de naissance",
    "adresse": "Adresse",
    "ville": "Ville actuelle",
    "jour": "jour",
    "horaire": "Horaire",
}

MOTIFS = {
    "travail": "Travail",
    "courses": "Courses",
    "consultation": "Consultation médicale",
    "familial": "Motif familial impérieux",
    "handicap": "Personne en situation de handicap",
    "sport": "Sport, ballade, promenade des animaux",
    "justice": "Convocation judiciaire ou administrative",
    "autorite": "Mission d'intérêt général",
    "enfants": "Enfants"
}

OUTPUT_PATH = "app/pdf/attestation.pdf"

# Flask
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    '''vue de la page d'accueil'''
    return render_template("index.html", champs=LISTE_CHAMPS, boutons=MOTIFS)


@app.route("/attestation", methods=["POST"])
def attestation():
    '''génère et envoie un PDF'''

    create_pdf(request.form)
    return_data = read_pdf_file(OUTPUT_PATH)
    os.remove(OUTPUT_PATH)

    return send_file(return_data,
                     mimetype='application/pdf',
                     attachment_filename="attestation.pdf")
