#!/usr/bin/env python3
"""
migrate-images.py

Télécharge les images du carrousel (actuellement hébergées sur le CDN
de Cargo, freight.cargo.site) vers un dossier local du dépôt, pour
rendre le site indépendant de Cargo.

Usage :
    python3 migrate-images.py

Prérequis : aucun (n'utilise que la bibliothèque standard de Python).
À lancer depuis la racine de ton dépôt (là où se trouve ton dossier
"img/").
"""

import os
import urllib.request
import urllib.error

# Dossier de destination (sera créé s'il n'existe pas)
OUTPUT_DIR = "img/portfolio"

# (URL source sur le CDN Cargo, nom de fichier local)
IMAGES = [
    ("https://freight.cargo.site/t/original/i/bd7fb072b8440cbd1c1d61b0081c1c85e63b254d76252bffd39e931a9920267a/Mockup.jpg", "01_Mockup.jpg"),
    ("https://freight.cargo.site/t/original/i/3686c7db76490a1b78dab0ec18f707175d69cd41ef3f4f39cc2cb4e880b28ff0/VS.03.jpg", "02_VS.03.jpg"),
    ("https://freight.cargo.site/t/original/i/c4d507d95aabd1f678b6328c6e0cb5854ea670c48a282376fe64b01b4eadf3b3/Promotion.Brochure.Friedberg.00.jpg", "03_Promotion.Brochure.Friedberg.00.jpg"),
    ("https://freight.cargo.site/t/original/i/5ab381cfb94a83b75417dbc3612a006c26e486d00d6ce3a35b2d97912c9a3b17/CARNET_01.jpg", "04_CARNET_01.jpg"),
    ("https://freight.cargo.site/t/original/i/17bf816961a8cbfed9ddf775d725ecd20fc147b3970ee21196cf9aeb869e93db/PO2.jpg", "05_PO2.jpg"),
    ("https://freight.cargo.site/t/original/i/9dce73d0232583e955fa5c4aac847c9fce923ddf122602c89b3231a2eaae5e99/Capture-decran-2023-09-06-a-09.59.42.png", "06_Capture-decran-2023-09-06-a-09.59.42.png"),
    ("https://freight.cargo.site/t/original/i/fcfee53180b65fc138b2d398185182cc812ff69e171c1975c56671d2834f7eb6/RQ0A8897.jpg", "07_RQ0A8897.jpg"),
    ("https://freight.cargo.site/t/original/i/52559d9c424f5cbad22c78723aa35e3a3b8006023141b1303bd38882d7f9d6ca/RQ0A2487.jpg", "08_RQ0A2487.jpg"),
    ("https://freight.cargo.site/t/original/i/2541fdb6820eb1a554850a3e8e8f436fcd29506a39e4bbe7eda4a69fa3fad7fb/Studio.Cards2.jpg", "09_Studio.Cards2.jpg"),
    ("https://freight.cargo.site/t/original/i/e3719bbe785e9858d722b64fd3d5d5bad9fef9080d186030bdd686e89565fe10/11.png", "10_11.png"),
    ("https://freight.cargo.site/t/original/i/6ac1d2831d688d45142bb2086c1cf75e7e04b08c6f4c99448392c79efabf66ad/IMG_4547.jpg", "11_IMG_4547.jpg"),
    ("https://freight.cargo.site/t/original/i/0bc4034e9070398391d1564b2c27147768b08d0b402dc7bd0244ff9aac095c7f/MANO.Cards.jpg", "12_MANO.Cards.jpg"),
    ("https://freight.cargo.site/t/original/i/ee9a9a225fc3cb191fd123859fdb5bf3053396627935e42639655ca82df89f52/CS-01.jpg", "13_CS-01.jpg"),
    ("https://freight.cargo.site/t/original/i/c9fde73f77ac042f574746df2101b68708189c6974dab6d46f570af8ae380044/3.jpg", "14_3.jpg"),
    ("https://freight.cargo.site/t/original/i/59d76d0b12bf15ce3be210dc19fd41aa50356d227a77c9c643cf88f69b3e143f/IMG_0071.jpg", "15_IMG_0071.jpg"),
    ("https://freight.cargo.site/t/original/i/de0dd080a2d487d77828ef465850ce905b267c36b37e3e77e0e7d9951f4fb80f/PP110x2.jpg", "16_PP110x2.jpg"),
    ("https://freight.cargo.site/t/original/i/c4cf11b46ba6121a9519fd14d384f32cdf2619fcc40052ba7420ede7ff796fc5/FP01.jpg", "17_FP01.jpg"),
    ("https://freight.cargo.site/t/original/i/75d2ecee9d9d5d0a2686ffcefd2475e9868678d20332b5deff9a284f07451c9a/O1.jpg", "18_O1.jpg"),
    ("https://freight.cargo.site/t/original/i/e4f721674cebfa9e097e6bb406d004c3c30c941945730182e83cdd21239428b5/Promotion.Brochure.Friedberg.07.jpg", "19_Promotion.Brochure.Friedberg.07.jpg"),
    ("https://freight.cargo.site/t/original/i/7a8133826ffa4d62f8d9e98b9e556bb0c5a8dbd2f2a4b027c84b2c900c32e63c/IMG_0445.JPG", "20_IMG_0445.JPG"),
    ("https://freight.cargo.site/t/original/i/9119c9934a663a0d96eb0218ec1f86711f6a7b1ed4f2771f55595f5b14a65fc7/IMG_0460-copie.jpg", "21_IMG_0460-copie.jpg"),
    ("https://freight.cargo.site/t/original/i/ab8c967067aa3b109d24caa72a5ddd6a59a22d6c91d123edd35d91ceb17af42d/RQ0A8748.jpg", "22_RQ0A8748.jpg"),
    ("https://freight.cargo.site/t/original/i/9d7b9d8a2abcdc7c89530d0702990097395aa8bf1670a440c6c5ad8746b09084/Mano.Editorial-Mockup.Mushkino.jpg", "23_Mano.Editorial-Mockup.Mushkino.jpg"),
    ("https://freight.cargo.site/t/original/i/4be8eee31fad1692bcf0f49acce5471b48ae43412c4ea0634d246ab2445f8b3c/Numeriser-5.jpeg", "24_Numeriser-5.jpeg"),
    ("https://freight.cargo.site/t/original/i/f676d922c89cb092cf650dac6acb1bf884958c2f3a59645f04f8a2ffbfe474b6/PO6.jpg", "25_PO6.jpg"),
    ("https://freight.cargo.site/t/original/i/fac2b933f90ef50d0634aa67ee304d72dd408ee54ba1a5fa3488c299d4c61453/design-5.png", "26_design-5.png"),
    ("https://freight.cargo.site/t/original/i/19c031acab45437452ac16de17510d8a9158fea76b0f46cdc3fbb2a868f61304/PPF-LYRS-004.002.jpg", "27_PPF-LYRS-004.002.jpg"),
    ("https://freight.cargo.site/t/original/i/0cdf985c4035f782fb8ab68a5b04d5c2434df288c3edd22ac6c1646993401174/Prmotion.Barbey.Poire.Bottle_Mockup.jpg", "28_Prmotion.Barbey.Poire.Bottle_Mockup.jpg"),
    ("https://freight.cargo.site/t/original/i/8462d93c0fbc68948130a539b9d08f87cf777f3fcb7dc8f95da361d0a7d09fbf/Friedber.UP-G-170-5x.jpg", "29_Friedber.UP-G-170-5x.jpg"),
    ("https://freight.cargo.site/t/original/i/14b1094e892a0d8d5ac4ff1a246ab5f926cff245ae073a19460877d24ee810b5/CLTR_UrbanPoster_UP-AMS-02.jpg", "30_CLTR_UrbanPoster_UP-AMS-02.jpg"),
    ("https://freight.cargo.site/t/original/i/9d696bb049f30388a492d6a7960c3d839923a18024fb7b6eae65f5e3952e7402/EB.Promo.Theatre.jpg", "31_EB.Promo.Theatre.jpg"),
    ("https://freight.cargo.site/t/original/i/541530822878cfa69bfd1e18ae400cde395a53f28fd7546fc55aec4fae6a76f8/PPF-LYRS-001.jpg", "32_PPF-LYRS-001.jpg"),
    ("https://freight.cargo.site/t/original/i/9dcc1f64ac0a2003c91db354f41757a82a1bd7edaa5d16fe951e1f19d023b9da/EB.Promo.Poesie.jpg", "33_EB.Promo.Poesie.jpg"),
    ("https://freight.cargo.site/t/original/i/7bc8634b08650b00eaff825470917fcb1f9eace2e0d8ce7a52f611fa651bfc42/P5130680.jpg", "34_P5130680.jpg"),
    ("https://freight.cargo.site/t/original/i/8f87bf4e4d54f361e9d88208fadc85b396da7fb1105125e55394364feb6b5b1a/ARTD-C05-Device-049.jpg", "35_ARTD-C05-Device-049.jpg"),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ok, skipped, failed = 0, 0, 0

    for url, filename in IMAGES:
        dest = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(dest):
            print(f"↷ déjà présent : {filename}")
            skipped += 1
            continue

        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            with open(dest, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"✓ téléchargé : {filename} ({size_kb:.0f} Ko)")
            ok += 1
        except urllib.error.URLError as e:
            print(f"✗ échec : {filename} — {e}")
            failed += 1
        except Exception as e:
            print(f"✗ erreur inattendue : {filename} — {e}")
            failed += 1

    print()
    print(f"Terminé : {ok} téléchargée(s), {skipped} déjà présente(s), {failed} échec(s).")
    if failed:
        print("Relance le script pour réessayer les fichiers en échec (ceux déjà présents seront ignorés).")


if __name__ == "__main__":
    main()
