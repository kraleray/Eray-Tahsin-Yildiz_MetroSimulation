import matplotlib.pyplot as plt
from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))


class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
        self.hatlar[hat].append(self.istasyonlar[idx])

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set()
        while kuyruk:
            mevcut_istasyon, yol = kuyruk.popleft()

            if mevcut_istasyon == hedef:
                return yol
            ziyaret_edildi.add(mevcut_istasyon)
            for komsu, _ in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [komsu]))
        return None

    def heuristic(self, istasyon: Istasyon, hedef: Istasyon) -> int:
        if istasyon.hat == hedef.hat:
            return abs(int(istasyon.idx[1:]) - int(hedef.idx[1:]))
        return 5

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        pq = [(self.heuristic(baslangic, hedef), 0, id(baslangic), baslangic, [baslangic])]
        while pq:
            _, toplam_sure, _, mevcut_istasyon, yol = heapq.heappop(pq)
            if mevcut_istasyon in ziyaret_edildi:
                continue
            ziyaret_edildi.add(mevcut_istasyon)
            if mevcut_istasyon == hedef:
                return yol, toplam_sure
            for komsu, sure in mevcut_istasyon.komsular:
                g_yeni = toplam_sure + sure
                f_yeni = g_yeni + self.heuristic(komsu, hedef)
                heapq.heappush(pq, (f_yeni, g_yeni, id(komsu), komsu, yol + [komsu]))
        return None

    def ciz(self, baslangic_id: str, hedef_id: str, rota: Optional[List[Istasyon]] = None):
        plt.figure(figsize=(12, 8))

        hat_renkleri = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Turuncu Hat": "orange"
        }

        istasyon_koordinatlar = {
            "K1": (1, 2),
            "K2": (2, 2),
            "K3": (3, 2),
            "K4": (4, 2),
            "M1": (1, 1),
            "M2": (1, 2),
            "M3": (2, 1),
            "M4": (3, 1),
            "T1": (1, 0),
            "T2": (3, 2),
            "T3": (3, 1),
            "T4": (4, 0)
        }

        for hat, istasyonlar in self.hatlar.items():
            x = []
            y = []
            for istasyon in istasyonlar:
                x.append(istasyon_koordinatlar[istasyon.idx][0])
                y.append(istasyon_koordinatlar[istasyon.idx][1])

            plt.scatter(x, y, color=hat_renkleri[hat], label=hat, s=100)

            for i, istasyon in enumerate(istasyonlar):
                plt.text(x[i], y[i] + 0.1, istasyon.ad, fontsize=9, ha='center', va='bottom', color=hat_renkleri[hat])

            for i in range(len(x) - 1):
                plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color=hat_renkleri[hat], linewidth=2)

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        x_baslangic, y_baslangic = istasyon_koordinatlar[baslangic.idx]
        plt.scatter(x_baslangic, y_baslangic, color="green", s=100, edgecolors="black", zorder=5, label="Başlangıç")
        plt.text(x_baslangic, y_baslangic + 0.2, "Başlangıç", fontsize=10, ha='center', va='bottom', color="green")

        x_hedef, y_hedef = istasyon_koordinatlar[hedef.idx]
        plt.scatter(x_hedef, y_hedef, color="red", s=100, edgecolors="black", zorder=5, label="Hedef")
        plt.text(x_hedef, y_hedef + 0.2, "Hedef", fontsize=10, ha='center', va='bottom', color="red")

        if rota:
            x_rota = [istasyon_koordinatlar[istasyon.idx][0] for istasyon in rota]
            y_rota = [istasyon_koordinatlar[istasyon.idx][1] for istasyon in rota]
            plt.plot(x_rota, y_rota, color="purple", linewidth=5, label="Rota")

        for istasyon in self.istasyonlar.values():
            if len([hat for hat, istasyon_listesi in self.hatlar.items() if istasyon in istasyon_listesi]) > 1:
                x, y = istasyon_koordinatlar[istasyon.idx]
                plt.scatter(x, y, color="yellow", s=300, edgecolors="black", zorder=5, label="Aktarma Noktası")

        plt.title("Metro Ağı")
        plt.xticks([])
        plt.yticks([])
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    metro = MetroAgi()

    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")

    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)

    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)

    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)
    print("\n=== Test Senaryoları ===")
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    print("\n=== Durak Listesi ===")
    for idx, istasyon in metro.istasyonlar.items():
        print(f"{idx}: {istasyon.ad}")

    baslangic_id = input("\nBaşlangıç istasyonu için ID girin (örneğin, M1, K4): ").strip().upper()
    while baslangic_id not in metro.istasyonlar:
        print("Geçersiz bir ID girdiniz lütfen aşağıdaki listeden bir ID seçin:")
        for idx, istasyon in metro.istasyonlar.items():
            print(f"  {idx}: {istasyon.ad}")
        baslangic_id = input("Başlangıç istasyonunun ID'sini girin (örneğin, M1, K4): ").strip().upper()

    hedef_id = input("Hedef istasyonunun ID'sini girin (örneğin, M1, K4): ").strip().upper()
    while hedef_id not in metro.istasyonlar:
        print("Geçersiz bir ID girdiniz lütfen aşağıdaki listeden bir ID seçin:")
        for idx, istasyon in metro.istasyonlar.items():
            print(f"  {idx}: {istasyon.ad}")
        hedef_id = input("Hedef istasyonunun ID'sini girin (örneğin, M1, K4): ").strip().upper()

    rota = metro.en_az_aktarma_bul(baslangic_id, hedef_id)
    if rota:
        print("\nEn az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul(baslangic_id, hedef_id)
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    metro.ciz(baslangic_id, hedef_id, rota)