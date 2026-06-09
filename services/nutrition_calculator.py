def kalori_hesapla(besinler: list[dict], veritabani: dict) -> dict:
    """
    Girilen besin listesini veritabanıyla eşleştirip toplam makro hesaplar.
    besinler: [{"ad": "tavuk", "gram": 300}, ...]
    """
    toplam = {"toplam_kalori": 0.0, "toplam_protein": 0.0, "toplam_karb": 0.0, "toplam_yag": 0.0}
    bulunamayanlar = []

    for besin in besinler:
        ad = besin.get("ad", "").lower()
        gram = besin.get("gram", 100)

        if ad not in veritabani:
            bulunamayanlar.append(ad)
            continue

        veri = veritabani[ad]
        oran = gram / 100

        toplam["toplam_kalori"] += veri["kalori"] * oran
        toplam["toplam_protein"] += veri["protein"] * oran
        toplam["toplam_karb"] += veri["karb"] * oran
        toplam["toplam_yag"] += veri["yag"] * oran

    return {
        **{k: round(v, 1) for k, v in toplam.items()},
        "bulunamayanlar": bulunamayanlar,
    }
