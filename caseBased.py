import math
import random

# Menghitung nilai fungsi objektif f(x1, x2) berdasarkan soal
def fungsi_objektif(x1, x2):
    bagian1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
    bagian2 = 0.5 * math.exp(1 - math.sqrt(x2**2))
    return -(bagian1 + bagian2)

# Mengubah kromosom representasi biner menjadi nilai x1 dan x2
def dekode(kromosom):
    panjang = len(kromosom) // 2
    # Membagi kromosom menjadi dua gen (masing-masing untuk x1 dan x2)
    gen1 = kromosom[:panjang]
    gen2 = kromosom[panjang:]
    
    # Mengkonversi nilai biner ke desimal
    des1 = sum([val * (2**idx) for idx, val in enumerate(reversed(gen1))])
    des2 = sum([val * (2**idx) for idx, val in enumerate(reversed(gen2))])
    
    maksimum = (2**panjang) - 1
    # Memetakan nilai desimal ke dalam range [-10, 10]
    x1 = -10 + (20 / maksimum) * des1
    x2 = -10 + (20 / maksimum) * des2
    
    return x1, x2

# Perhitungan fitness. Karena mencari nilai minimum, semakin kecil nilai fungsi, semakin besar fitness
def hitung_fitness_positif(kromosom):
    x1, x2 = dekode(kromosom)
    # Menambah konstanta agar fitness tidak bernilai negatif
    # Asumsi 100 nilai yang besar untuk mengimbangi output fungsi
    return 100 - fungsi_objektif(x1, x2)

# Menginisialisasi populasi awal secara acak berisi 0 dan 1
def buat_populasi(ukuran, panjang):
    return [[random.randint(0, 1) for _ in range(panjang)] for _ in range(ukuran)]

# Roulette Wheel Selection, semakin tinggi fitness maka semakin besar peluang terpilih
def seleksi_roulette(populasi):
    # Hitung total fitness seluruh populasi
    total_fitness = sum(hitung_fitness_positif(ind) for ind in populasi)
    # Tentukan titik acak pada roda
    titik_henti = random.uniform(0, total_fitness)
    
    arus_fitness = 0
    for individu in populasi:
        arus_fitness += hitung_fitness_positif(individu)
        if arus_fitness >= titik_henti:
            return individu
    return populasi[-1]

# Two-point Crossover, dua titik potong memberikan variasi genetik yang lebih dinamis dibandingkan hanya satu titik.
def pindah_silang_dua_titik(induk1, induk2, pc):
    if random.random() < pc:
        # Tentukan dua titik potong secara acak
        titik1 = random.randint(1, len(induk1) - 2)
        titik2 = random.randint(titik1 + 1, len(induk1) - 1)
        
        # Tukar bagian tengah antara dua titik tersebut
        anak1 = induk1[:titik1] + induk2[titik1:titik2] + induk1[titik2:]
        anak2 = induk2[:titik1] + induk1[titik1:titik2] + induk2[titik2:]
        return anak1, anak2
    return induk1, induk2

# Metode mutasi pembalikan bit (Bit-flip Mutation)
def mutasi(kromosom, pm):
    # Membalik bit (0 jadi 1, 1 jadi 0) jika probabilitas Pm terpenuhi
    return [1 - gen if random.random() < pm else gen for gen in kromosom]

# Proses Utama Algoritma Genetika
def algoritma_genetika():
    # Menentukan parameter GA
    ukuran_populasi = 50
    panjang_kromosom = 20
    maks_generasi = 100
    pc = 0.8
    pm = 0.1
    
    # 1. Inisialisasi populasi
    populasi = buat_populasi(ukuran_populasi, panjang_kromosom)
    
    # 5. Kriteria Penghentian Evolusi (Loop berulang hingga batas maksimum)
    for generasi in range(maks_generasi):
        # Evaluasi kecocokan seluruh populasi dan urutkan
        populasi.sort(key=hitung_fitness_positif, reverse=True)
        
        # 4. Pergantian Generasi: Elitisme (Simpan 2 kromosom terbaik)
        populasi_baru = populasi[:2]
        
        # Buat keturunan baru sampai memenuhi batas ukuran populasi
        while len(populasi_baru) < ukuran_populasi:
            # 2. Pemilihan Orangtua
            induk1 = seleksi_roulette(populasi)
            induk2 = seleksi_roulette(populasi)
    
            # 3. Operasi Genetik: Pindah Silang (Crossover)
            anak1, anak2 = pindah_silang_dua_titik(induk1, induk2, pc)
            
            # 3. Operasi Genetik: Mutasi dan simpan ke populasi baru
            populasi_baru.append(mutasi(anak1, pm))
            if len(populasi_baru) < ukuran_populasi:
                populasi_baru.append(mutasi(anak2, pm))
                
        # Mengganti generasi lama dengan generasi yang baru
        populasi = populasi_baru
        
    # Mengambil dan mengevaluasi hasil terbaik setelah loop selesai
    populasi.sort(key=hitung_fitness_positif, reverse=True)
    kromosom_terbaik = populasi[0]
    x1, x2 = dekode(kromosom_terbaik)
    
    # Output program
    print("Kromosom Terbaik:", kromosom_terbaik)
    print("Nilai x1:", x1)
    print("Nilai x2:", x2)

# Eksekusi fungsi GA
if __name__ == "__main__":
    algoritma_genetika()