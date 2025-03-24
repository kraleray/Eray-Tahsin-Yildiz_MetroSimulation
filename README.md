# Metro Rota Optimizasyon Simülasyonu 

Bu proje, bir metro ağında en az aktarmalı ve en hızlı rotayı bulmak için BFS ve A* algoritmalarını kullanır. Kullanıcılar, başlangıç ve hedef istasyonlarını seçerek en uygun rotayı belirleyebilir ve görselleştirebilir.

##  Kullanılan Teknolojiler ve Kütüphaneler

- **Python 3.11**
- Kütüphaneler:
  - collections.deque: BFS algoritmasında kuyruk yapısı için.
  - heapq: A* algoritmasında öncelik kuyruğu için.
  - matplotlib: Metro ağının görselleştirilmesi için.
  - typing: Tip ipuçları (type hints) için.

## Algoritmaların Çalışma Mantığı

### 1. BFS (Breadth-First Search)
- **Amacı**: En az aktarmalı rotayı bulmak.
- **Nasıl Çalışır?**:
  - Başlangıç istasyonundan başlayarak tüm komşuları tek tek gezer.
  - Hedefe ulaşana kadar her seviyedeki istasyonları inceler.
  - Önce aynı hat üzerindeki istasyonları, sonra aktarma noktalarını kontrol eder.
- **Neden Kullandık?**: Aktarma sayısını minimize etmek için ideal.

### 2. A* (A-Star) Algoritması
- **Amacı**: En hızlı rotayı bulmak.
- **Nasıl Çalışır?**:
  - Toplam süreyi minimize etmek için ağırlıklı bir arama yapar.
  - Gidilen yolun süresini ve tahmini kalan mesafeyi dikkate alır.
  - Öncelik kuyruğu (heapq) kullanarak en düşük maliyetli rotayı seçer.
- **Neden Kullandık?**: Hız açısından en verimli güzergahı belirlemek için uygundur.

### 3. Metro Ağı Görselleştirme Sistemi
- **Amacı**: Metro ağını grafiksel olarak göstermek.
- **Nasıl Çalışır?**:
  - plt.scatter() ile istasyonları noktalar halinde çizer.
  - plt.plot() ile hatları birbirine bağlar.
  - Başlangıç, hedef ve aktarma noktalarını farklı renklerle vurgular.
- **Neden Kullandık?**: Kullanıcıların rotayı daha iyi anlamasını sağlamak için.

  
## Örnek Kullanım ve Test Sonuçları
=== Test Senaryoları ===

1. AŞTİ'den OSB'ye:
En az aktarmalı rota: AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB  
En hızlı rota (25 dakika): AŞTİ -> Kızılay -> Kızılay -> Ulus -> Demetevler -> OSB

2. Kullanıcı Girişi ile:  
=== Durak Listesi ===  
  K1: Kızılay  
  K2: Ulus  
  K3: Demetevler  
  K4: OSB  
  M1: AŞTİ  
  M2: Kızılay  
  M3: Sıhhiye  
  M4: Gar  
  T1: Batıkent  
  T2: Demetevler  
  T3: Gar  
  T4: Keçiören  
Başlangıç istasyonunun ID'sini girin (örneğin, M1, K4): m1  
Hedef istasyonunun ID'sini girin (örneğin, M1, K4): t4  

En az aktarmalı rota: AŞTİ -> Kızılay -> Sıhhiye -> Gar -> Gar -> Keçiören  
En hızlı rota (19 dakika): AŞTİ -> Kızılay -> Sıhhiye -> Gar -> Gar -> Keçiören  
  
![image](https://github.com/user-attachments/assets/94c301df-5230-4940-a3c4-9cf2a2bc59e7)  

##  Projeyi Geliştirme Fikirleri

### Gerçek Dünya Verileri
- İstanbul, Londra gibi metro ağlarının gerçek istasyonlarını ve sürelerini ekleyerek simülasyonu gerçekçi hale getirebilirsiniz.
- Belediyelerinin açık verileri entegre edilebilir.

### Web Arayüzü ve Mobil Uygulama
- Kullanıcı dostu bir web arayüzü geliştirilebilir.
- Mobil uygulamaya dönüştürülebilir.
- Kullanıcıların istasyon seçimi için interaktif harita entegrasyonu yapılabilir.

### Trafik Verileri
- Gerçek zamanlı tren sıklığı verileriyle süre hesaplaması yapılabilir.
- Yoğun saatlerde aktarma sürelerini otomatik artıran bir algoritma eklenebilir.
