"""
Tugas Rekursif — tiga algoritma backtracking rekursif
1. N-Queens  (n-ratu)
2. Knight's Tour (Tur Kuda) — dengan heuristik Warnsdorff
3. Knapsack  (masalah karung)
"""

# ─────────────────────────────────────────────────────────────
# 1.  N-QUEENS
# ─────────────────────────────────────────────────────────────

def n_queens_all(n):
    """Kembalikan semua solusi N-Queens sebagai list posisi kolom per baris."""
    solusi = []
    cols   = [False] * n
    diag1  = [False] * (2 * n)   # row - col + n  (diagonal /)
    diag2  = [False] * (2 * n)   # row + col       (diagonal \)
    ratu   = [-1] * n

    def backtrack(row):
        if row == n:
            solusi.append(ratu[:])
            return
        for col in range(n):
            if cols[col] or diag1[row - col + n] or diag2[row + col]:
                continue
            ratu[row] = col
            cols[col] = diag1[row - col + n] = diag2[row + col] = True
            backtrack(row + 1)
            ratu[row] = -1
            cols[col] = diag1[row - col + n] = diag2[row + col] = False

    backtrack(0)
    return solusi


def cetak_papan_queens(n, ratu):
    """Cetak papan N-Queens ke konsol."""
    garis = "+" + ("---+" * n)
    print(garis)
    for row in range(n):
        baris = "|"
        for col in range(n):
            baris += " Q |" if ratu[row] == col else "   |"
        print(baris)
        print(garis)
    print()


def main_queens():
    print("=" * 50)
    print("        MASALAH N-QUEENS (N-RATU)")
    print("=" * 50)
    n = int(input("Masukkan ukuran papan (n): "))
    if n < 1:
        print("Ukuran papan harus minimal 1.")
        return

    semua = n_queens_all(n)
    if not semua:
        print(f"Tidak ada solusi untuk papan {n}x{n}.")
        return

    print(f"\nDitemukan {len(semua)} solusi untuk papan {n}x{n}.")
    tampil = input("Tampilkan semua solusi? (y/n): ").strip().lower()

    if tampil == "y":
        for i, sol in enumerate(semua, 1):
            print(f"\n--- Solusi {i} ---")
            print("Posisi ratu (kolom per baris):", [c + 1 for c in sol])
            cetak_papan_queens(n, sol)
    else:
        print("\n--- Solusi pertama ---")
        print("Posisi ratu (kolom per baris):", [c + 1 for c in semua[0]])
        cetak_papan_queens(n, semua[0])


# ─────────────────────────────────────────────────────────────
# 2.  KNIGHT'S TOUR (Tur Kuda) — Warnsdorff + backtracking
# ─────────────────────────────────────────────────────────────

GERAK_KUDA = [(2, 1), (1, 2), (-1, 2), (-2, 1),
              (-2, -1), (-1, -2), (1, -2), (2, -1)]


def derajat_warnsdorff(papan, r, c, n):
    """Hitung jumlah langkah valid dari (r, c) — digunakan heuristik Warnsdorff."""
    return sum(
        1
        for dr, dc in GERAK_KUDA
        if 0 <= r + dr < n and 0 <= c + dc < n and papan[r + dr][c + dc] < 0
    )


def knight_tour(n, baris_awal, kolom_awal):
    """
    Selesaikan Tur Kuda dengan heuristik Warnsdorff.
    Kembalikan papan jika berhasil, None jika gagal.
    """
    papan = [[-1] * n for _ in range(n)]
    papan[baris_awal][kolom_awal] = 1
    r, c = baris_awal, kolom_awal

    for langkah in range(2, n * n + 1):
        kandidat = []
        for dr, dc in GERAK_KUDA:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and papan[nr][nc] < 0:
                deg = derajat_warnsdorff(papan, nr, nc, n)
                kandidat.append((deg, nr, nc))

        if not kandidat:
            return None   # macet sebelum selesai

        kandidat.sort()           # pilih yang derajatnya paling kecil
        _, nr, nc = kandidat[0]
        papan[nr][nc] = langkah
        r, c = nr, nc

    return papan


def cetak_papan_kuda(papan, n):
    """Cetak papan Tur Kuda ke konsol."""
    lebar = len(str(n * n)) + 1
    garis = "+" + (("-" * lebar + "+") * n)
    print(garis)
    for row in range(n):
        baris = "|"
        for col in range(n):
            v = papan[row][col]
            baris += str(v).center(lebar) + "|"
        print(baris)
        print(garis)
    print()


def main_knight_tour():
    print("=" * 50)
    print("       MASALAH TUR KUDA (KNIGHT'S TOUR)")
    print("=" * 50)
    n = int(input("Ukuran papan n×n (disarankan 8): "))
    br = int(input(f"Baris awal  (0–{n-1}): "))
    kl = int(input(f"Kolom awal  (0–{n-1}): "))

    if not (0 <= br < n and 0 <= kl < n):
        print("Posisi di luar papan.")
        return

    papan = knight_tour(n, br, kl)
    if papan is None:
        print(f"\nTidak ditemukan solusi dari ({br}, {kl}) pada papan {n}×{n}.")
        return

    print(f"\nTur Kuda berhasil! Papan {n}×{n} mulai dari ({br}, {kl}):\n")
    cetak_papan_kuda(papan, n)

    # Cetak urutan langkah sebagai list koordinat
    total = n * n
    urutan = [None] * (total + 1)
    for r in range(n):
        for c in range(n):
            if papan[r][c] > 0:
                urutan[papan[r][c]] = (r, c)
    print("Urutan langkah (baris, kolom):")
    for i in range(1, total + 1):
        sep = "\n" if i % 8 == 0 else "  "
        print(f"{i:3}:({urutan[i][0]},{urutan[i][1]})", end=sep)
    print()


# ─────────────────────────────────────────────────────────────
# 3.  KNAPSACK (masalah karung) — rekursif
# ─────────────────────────────────────────────────────────────

def knapsack_semua_solusi(barang, target):
    """
    Temukan SEMUA subset barang yang totalnya tepat = target.
    Kembalikan list of list (indeks barang terpilih).
    """
    solusi = []

    def backtrack(idx, sisa, dipilih):
        if sisa == 0:
            solusi.append(dipilih[:])
            return
        if idx == len(barang) or sisa < 0:
            return
        # ambil barang[idx]
        dipilih.append(idx)
        backtrack(idx + 1, sisa - barang[idx], dipilih)
        dipilih.pop()
        # lewati barang[idx]
        backtrack(idx + 1, sisa, dipilih)

    backtrack(0, target, [])
    return solusi


def knapsack_satu_solusi(barang, target):
    """
    Temukan SATU solusi (lebih cepat, berhenti di solusi pertama).
    Kembalikan list indeks atau None.
    """
    def backtrack(idx, sisa, dipilih):
        if sisa == 0:
            return dipilih[:]
        if idx == len(barang) or sisa < 0:
            return None
        # coba ambil
        dipilih.append(idx)
        hasil = backtrack(idx + 1, sisa - barang[idx], dipilih)
        if hasil is not None:
            return hasil
        dipilih.pop()
        # lewati
        return backtrack(idx + 1, sisa, dipilih)

    return backtrack(0, target, [])


def main_knapsack():
    print("=" * 50)
    print("          MASALAH KNAPSACK (KARUNG)")
    print("=" * 50)
    raw = input("Masukkan berat barang (pisahkan koma), contoh: 2,5,6,9,12,14,20\n> ")
    try:
        barang = [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        print("Format input tidak valid.")
        return
    if not barang:
        print("Tidak ada barang.")
        return

    target = int(input("Masukkan berat target: "))

    print(f"\nBarang : {barang}")
    print(f"Target : {target}\n")

    mode = input("Cari satu solusi (1) atau semua solusi (2)? ").strip()

    if mode == "2":
        semua = knapsack_semua_solusi(barang, target)
        if not semua:
            print("Tidak ada kombinasi yang memenuhi target.")
        else:
            print(f"Ditemukan {len(semua)} solusi:\n")
            for i, sol in enumerate(semua, 1):
                berat_terpilih = [barang[j] for j in sol]
                total = sum(berat_terpilih)
                print(f"  Solusi {i:3}: {berat_terpilih}  → total = {total}")
    else:
        sol = knapsack_satu_solusi(barang, target)
        if sol is None:
            print("Tidak ada kombinasi yang memenuhi target.")
        else:
            berat_terpilih = [barang[j] for j in sol]
            print(f"Solusi ditemukan: {berat_terpilih}")
            print(f"Total berat     : {sum(berat_terpilih)}")


# ─────────────────────────────────────────────────────────────
# MENU UTAMA
# ─────────────────────────────────────────────────────────────

def main():
    menu = {
        "1": ("N-Queens (N-Ratu)", main_queens),
        "2": ("Tur Kuda (Knight's Tour)", main_knight_tour),
        "3": ("Knapsack (Masalah Karung)", main_knapsack),
        "0": ("Keluar", None),
    }

    while True:
        print("\n" + "=" * 50)
        print("    PROGRAM ALGORITMA REKURSIF & BACKTRACKING")
        print("=" * 50)
        for k, (nama, _) in menu.items():
            print(f"  [{k}] {nama}")
        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "0":
            print("Sampai jumpa!")
            break
        elif pilihan in menu:
            print()
            menu[pilihan][1]()
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()