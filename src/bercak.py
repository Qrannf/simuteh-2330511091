"""bercak.py: analisis bercak SIMUTEH (dipakai ulang mulai P7)."""

import json
import cv2
import numpy as np
from utils_tepi import mask_daun_awal, bercak_awal

PARAM_BERCAK = {
    "kanal": 2,
    "k": 4.0,
    "se_bentuk": "elips",
    "se_open": 5,
    "se_close": 5,
    "luas_min": 20,
    "bulat_min": 0.5,
    "rasio_maks": 1.8,
    "batas_ringan": 0.1,
    "batas_berat": 2.0,
    "mm_per_px": 0.4375,
}

_BENTUK = {
    "elips": cv2.MORPH_ELLIPSE,
    "persegi": cv2.MORPH_RECT,
    "silang": cv2.MORPH_CROSS
}


def _se(p, uk):
    return cv2.getStructuringElement(
        _BENTUK[p["se_bentuk"]], (uk, uk)
    )


def bersihkan(biner, p):
    """Opening membuang derau dan closing menutup celah."""
    hasil = biner.copy()

    # TODO 1: Opening
    if p["se_open"] > 0:
        hasil = cv2.morphologyEx(
            hasil, cv2.MORPH_OPEN, _se(p, p["se_open"])
        )

    # TODO 2: Closing
    if p["se_close"] > 0:
        hasil = cv2.morphologyEx(
            hasil, cv2.MORPH_CLOSE, _se(p, p["se_close"])
        )

    return hasil


def ukur_dan_saring(biner, p):
    """Mengukur dan menyaring setiap komponen bercak."""

    # TODO 3: Label komponen dengan konektivitas 8
    jumlah, label, stats, pusat = cv2.connectedComponentsWithStats(
        (biner > 0).astype(np.uint8),
        connectivity=8
    )

    keluar = np.zeros_like(biner)
    daftar = []

    for i in range(1, jumlah):
        mask = (label == i).astype(np.uint8)

        # Kontur komponen
        kontur, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        if not kontur:
            continue

        kontur = kontur[0]

        # TODO 4: Menghitung karakteristik komponen
        luas = int(stats[i, cv2.CC_STAT_AREA])
        keliling = cv2.arcLength(kontur, True)

        kebulatan = (
            0.0 if keliling == 0
            else 4 * np.pi * luas / (keliling ** 2)
        )

        w, h = cv2.minAreaRect(kontur)[1]
        rasio = max(w, h) / max(min(w, h), 1)

        # TODO 5: Penyaringan komponen
        if (
            luas >= p["luas_min"]
            and kebulatan >= p["bulat_min"]
            and rasio <= p["rasio_maks"]
        ):
            keluar[mask > 0] = 255

            daftar.append({
                "label": int(i),
                "luas_px": luas,
                "luas_mm2": round(
                    luas * p["mm_per_px"] ** 2, 2
                ),
                "keliling_px": round(float(keliling), 2),
                "kebulatan": round(float(kebulatan), 3),
                "rasio_aspek": round(float(rasio), 3),
                "cx": int(pusat[i][0]),
                "cy": int(pusat[i][1])
            })

    return keluar, daftar


def analisis_daun(img_praproses, p=None):
    """Menganalisis bercak pada citra BGR hasil praproses."""

    p = {**PARAM_BERCAK, **(p or {})}

    m_daun = mask_daun_awal(img_praproses)

    biner = bercak_awal(
        img_praproses,
        m_daun,
        kanal=p["kanal"],
        k=p["k"]
    )

    m_bercak, daftar = ukur_dan_saring(
        bersihkan(biner, p), p
    )

    # TODO 6: Menghitung persentase luas bercak
    luas_daun = np.count_nonzero(m_daun > 0)
    luas_bercak = np.count_nonzero(m_bercak > 0)

    persen = (
        0.0 if luas_daun == 0
        else luas_bercak / luas_daun * 100
    )

    # TODO 7: Menentukan kelas mutu
    if persen >= p["batas_berat"]:
        kelas = "Bercak Berat"
    elif persen >= p["batas_ringan"]:
        kelas = "Bercak Ringan"
    else:
        kelas = "Sehat"

    return {
        "mask_daun": m_daun,
        "mask_bercak": m_bercak,
        "jumlah_bercak": len(daftar),
        "persen_bercak": round(float(persen), 3),
        "kelas": kelas,
        "bercak": daftar
    }


def simpan_param(p, path="../hasil/param_bercak.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BERCAK, **p}, f, indent=2)
