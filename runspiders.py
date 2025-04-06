import os
import subprocess
import argparse


# Liste des spiders disponibles
ALL_SPIDERS = [
    'guardian_picture',
    'smh_picture',
    'cnn_week_pics',
    'atlantic_pictures',
    'theweek_pictures'
]


def prompt_spider_choice():
    # Environnement CI/CD : on lance automatiquement tous les spiders
    if os.getenv("CI") == "true":
        print("Mode CI détecté. Tous les spiders seront lancés sans prompt.")
        return ALL_SPIDERS

    # Sinon, prompt utilisateur
    choice = input("Lancer tous les spiders ? [Y/N]: ").strip().lower()
    if choice == 'y' or choice == '':
        return ALL_SPIDERS
    else:
        print("Liste des spiders disponibles :")
        for idx, spider in enumerate(ALL_SPIDERS, start=1):
            print(f"{idx}. {spider}")
        selected = input("Entrez le numéro du spider à lancer: ").strip()
        try:
            idx = int(selected) - 1
            if 0 <= idx < len(ALL_SPIDERS):
                return [ALL_SPIDERS[idx]]
            else:
                print("Numéro invalide. Lancement de tous les spiders par défaut.")
                return ALL_SPIDERS
        except ValueError:
            print("Entrée invalide. Lancement de tous les spiders par défaut.")
            return ALL_SPIDERS


def main():
    parser = argparse.ArgumentParser(
        description="Lance les spiders Scrapy avec option de sélection interactive."
    )
    parser.add_argument(
        "--spider",
        help="Nom du spider à lancer (si omis, le script demande via un prompt interactif)",
        default=None
    )
    args = parser.parse_args()

    # Définir le dossier de sortie fixe
    output_dir = "json_datas"
    os.makedirs(output_dir, exist_ok=True)

    # Déterminer quels spiders lancer
    if args.spider:
        if args.spider not in ALL_SPIDERS:
            print(f"Spider '{args.spider}' non trouvé. Lancement de tous les spiders.")
            spiders_to_run = ALL_SPIDERS
        else:
            spiders_to_run = [args.spider]
    else:
        spiders_to_run = prompt_spider_choice()

    # Lancer chaque spider et exporter dans json_datas/ avec écrasement
    for spider in spiders_to_run:
        outfile = os.path.join(output_dir, f"{spider}.json")
        cmd = [
            "scrapy",
            "crawl",
            spider,
            "-O", f"{outfile}:json"  # Force l'écrasement et indique le format JSON
        ]
        print(f"Lancement du spider '{spider}' (fichier: {outfile})")
        subprocess.run(cmd, check=True)

    if len(spiders_to_run) == len(ALL_SPIDERS):
        print("Tous les spiders ont été lancés.")
    else:
        print(f"le spider {spiders_to_run} a été lancé.")


if __name__ == "__main__":
    main()
