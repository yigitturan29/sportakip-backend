"""
Hareket fotoğrafı çekme servisi.
İleride ExerciseDB veya Unsplash API ile entegre edilecek.
"""
import httpx


async def fotograf_getir(hareket_adi: str) -> str | None:
    """Hareket adına göre fotoğraf URL'i döner. Şimdilik mock."""
    # TODO: Gerçek API entegrasyonu (ExerciseDB, Wger, vb.)
    mock_urls = {
        "bench press": "https://example.com/images/benchpress.jpg",
        "squat": "https://example.com/images/squat.jpg",
        "deadlift": "https://example.com/images/deadlift.jpg",
    }
    return mock_urls.get(hareket_adi.lower())


async def toplu_fotograf_guncelle(hareketler: list[str]) -> dict:
    """Birden fazla hareket için fotoğraf URL'lerini günceller."""
    sonuclar = {}
    for hareket in hareketler:
        url = await fotograf_getir(hareket)
        sonuclar[hareket] = url or "bulunamadi"
    return sonuclar
