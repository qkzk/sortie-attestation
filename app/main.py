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
from flask import Flask, render_template, request, send_file
import pypandoc


def get_text(text_path) -> str:
    '''retourne le contenu du fichier texte'''
    with open(text_path) as attestation:
        return attestation.read()


def fill_text(text: str, parsed_form: list, motifs=None) -> str:
    '''rempli le texte avec les données reçues depuis le formulaire'''
    # TODO améliorer cette merde
    parsed_form[-3] = date.today()
    return text.format(*parsed_form, **motifs)


def parse_form(form: dict) -> list:
    '''récupère les données du formulaire et les ordonne dans une liste'''
    return [form.get(key) for key in LISTE_CHAMPS]


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
                          outputfile=OUTPUT_PDF)


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


TEXT_PATH = "/app/app/text/attestation-de-deplacement-derogatoire.md"
TEXT = get_text(TEXT_PATH)
LISTE_CHAMPS = ['nom',
                'prenom',
                'date_naissance',
                'adresse',
                'ville',
                'jour',
                'horaire',
                'nom']
MOTIFS = ['travail',
          'courses',
          'consultation',
          'familial',
          'handicap',
          'sport',
          'justice',
          'autorite',
          'enfants']
OUTPUT_PDF = "/app/app/pdf/attestation.pdf"

# Flask
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    '''vue de la page d'accueil'''
    return render_template("index.html")


@app.route("/generer", methods=["POST"])
def generer():
    '''génère et envoie un PDF'''

    create_pdf(request.form)
    return_data = read_pdf_file(OUTPUT_PDF)
    os.remove(OUTPUT_PDF)

    return send_file(return_data,
                     mimetype='application/pdf',
                     attachment_filename="attestation.pdf")
