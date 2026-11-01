"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""

import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,         # sampling: lebar citra kerja (piksel)
    "gamma": 1.0,         # < 1 mencerahkan, > 1 menggelapkan
    "clahe_clip": 2.0,    # 0 berarti CLAHE tidak dipakai
    "clahe_tile": 8,
    "penapis": "median",  # "none", "rerata", "gaussian", "median"
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,       # 0 berarti tanpa penajaman
}


def praproses(img_bgr, p=None):
    """
    Urutan praproses:
    1. Ubah ukuran
    2. Koreksi gamma
    3. CLAHE pada kanal V
    4. Redam derau
    5. Penajaman (unsharp masking)
    """

    p = {**PARAM_BAWAAN, **(p or {})}

    # TODO 1: Ubah ukuran dengan rasio aspek tetap
    h, w = img_bgr.shape[:2]
    lebar = int(p["lebar"])
    tinggi = int(round(h * lebar / w))

    img = cv2.resize(
        img_bgr,
        (lebar, tinggi),
        interpolation=cv2.INTER_AREA
    )

    # TODO 2: Koreksi gamma menggunakan cv2.LUT
    if p["gamma"] != 1.0:
        gamma = float(p["gamma"])

        if gamma <= 0:
            raise ValueError("Gamma harus lebih besar dari 0")

        lut = np.array([
            255 * (i / 255.0) ** gamma
            for i in range(256)
        ]).clip(0, 255).astype(np.uint8)

        img = cv2.LUT(img, lut)

    # TODO 3: CLAHE pada kanal V di ruang warna HSV
    if p["clahe_clip"] > 0:
        ubin = int(p["clahe_tile"])

        clahe = cv2.createCLAHE(
            clipLimit=float(p["clahe_clip"]),
            tileGridSize=(ubin, ubin)
        )

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # TODO 4: Redam derau sesuai jenis penapis
    k = int(p["kernel"])

    if p["penapis"] == "median" and k < 3:
        raise ValueError("Kernel median minimal 3")

    if k % 2 == 0:
        k += 1

    if p["penapis"] == "rerata":
        img = cv2.blur(img, (k, k))

    elif p["penapis"] == "gaussian":
        img = cv2.GaussianBlur(
            img,
            (k, k),
            float(p["sigma"])
        )

    elif p["penapis"] == "median":
        img = cv2.medianBlur(img, k)

    elif p["penapis"] == "none":
        pass

    else:
        raise ValueError(
            "Jenis penapis harus none, rerata, gaussian, atau median"
        )

    # TODO 5: Penajaman menggunakan unsharp masking
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)

        img = cv2.addWeighted(
            img,
            1.0 + p["tajam_k"],
            blur,
            -p["tajam_k"],
            0
        )

    return img


def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump(
            {**PARAM_BAWAAN, **p},
            f,
            indent=2
        )
