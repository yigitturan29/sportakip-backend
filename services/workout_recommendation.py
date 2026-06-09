"""
RPE tabanlı antrenman öneri servisi.
İleride OpenAI API ile değiştirilebilir modüler yapı.
"""
from typing import List


def oneri_uret(performans: dict) -> dict:
    rpe            = int(performans.get("rpe", 7))
    mevcut_agirlik = float(performans.get("agirlik", 0) or performans.get("weight", 0) or 0)
    mevcut_set     = int(performans.get("set_sayisi", 0) or performans.get("sets", 0) or 3)

    if rpe <= 6:
        return {
            "eylem":         "agirlik_artir",
            "mesaj":         f"RPE {rpe} — Gelecek hafta ağırlığı 2.5–5 kg artır.",
            "oneri_agirlik": round(mevcut_agirlik + 2.5, 1),
            "oneri_set":     mevcut_set,
        }
    elif rpe <= 8:
        return {
            "eylem":         "tekrar_artir",
            "mesaj":         f"RPE {rpe} — Aynı ağırlıkla 1–2 tekrar daha ekle.",
            "oneri_agirlik": mevcut_agirlik,
            "oneri_set":     mevcut_set,
        }
    elif rpe == 9:
        return {
            "eylem":         "koru",
            "mesaj":         f"RPE {rpe} — Ağırlığı koru, seti 1 azaltmayı düşün.",
            "oneri_agirlik": mevcut_agirlik,
            "oneri_set":     max(mevcut_set - 1, 1),
        }
    else:  # rpe == 10
        return {
            "eylem":         "deload",
            "mesaj":         f"RPE {rpe} — Deload yap, ağırlığı %10 düşür.",
            "oneri_agirlik": round(mevcut_agirlik * 0.9, 1),
            "oneri_set":     max(mevcut_set - 1, 1),
        }


def oneri_uret_batch(exercises: List) -> list:
    """Birden fazla egzersiz için toplu öneri üretir."""
    result = []
    for ex in exercises:
        data = ex if isinstance(ex, dict) else ex.model_dump()
        oneri = oneri_uret(data)
        result.append({
            "hareket":       data.get("ad", ""),
            "kas":           data.get("kas", ""),
            "mevcut_agirlik": float(data.get("weight", 0) or 0),
            "oneri":         oneri,
        })
    return result
