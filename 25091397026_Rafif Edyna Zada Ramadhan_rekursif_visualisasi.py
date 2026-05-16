"""
============================================================
  TUGAS REKURSIF - Visualisasi Interaktif
  Berisi 3 algoritma:
    1. N-Queens (N-Ratu)
    2. Knight's Tour (Tur Kuda)
    3. Knapsack (Masalah Tas)

  Cara menjalankan:
    python rekursif_visualisasi.py

  Output:
    File HTML interaktif akan dibuka otomatis di browser.
============================================================
"""

import webbrowser
import os
import sys

# ─────────────────────────────────────────────────────────
# 1. N-QUEENS ALGORITHM
# ─────────────────────────────────────────────────────────

def is_safe_nqueens(board, row, col, n):
    """Cek apakah posisi (row, col) aman untuk meletakkan ratu."""
    # Cek kolom yang sama di baris sebelumnya
    for i in range(row):
        if board[i] == col:
            return False
        # Cek diagonal
        if abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_nqueens_all(board, row, n, solutions):
    """Rekursif: temukan semua solusi N-Queens menggunakan backtracking."""
    if row == n:
        solutions.append(board[:])  # Simpan salinan solusi
        return
    for col in range(n):
        if is_safe_nqueens(board, row, col, n):
            board[row] = col          # Tempatkan ratu
            solve_nqueens_all(board, row + 1, n, solutions)
            board[row] = -1           # Backtrack: hapus ratu

def get_nqueens_solutions(n):
    """Kembalikan semua solusi N-Queens untuk papan ukuran n."""
    board = [-1] * n
    solutions = []
    solve_nqueens_all(board, 0, n, solutions)
    return solutions


# ─────────────────────────────────────────────────────────
# 2. KNIGHT'S TOUR ALGORITHM (Warnsdorff's Heuristic)
# ─────────────────────────────────────────────────────────

# 8 arah gerak kuda dalam catur
KT_DX = [-2, -1, 1, 2,  2,  1, -1, -2]
KT_DY = [ 1,  2, 2, 1, -1, -2, -2, -1]

def count_exits(x, y, board, n):
    """Hitung berapa langkah valid dari posisi (x, y) — digunakan Warnsdorff."""
    count = 0
    for i in range(8):
        nx, ny = x + KT_DX[i], y + KT_DY[i]
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
            count += 1
    return count

def knight_tour_recursive(board, x, y, move_num, n):
    """
    Rekursif backtracking dengan Warnsdorff's heuristic.
    Mengurutkan langkah berikutnya berdasarkan jumlah exit terkecil.
    """
    if move_num > n * n:
        return True  # Semua petak sudah dikunjungi

    # Kumpulkan semua langkah valid
    next_moves = []
    for i in range(8):
        nx, ny = x + KT_DX[i], y + KT_DY[i]
        if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
            exits = count_exits(nx, ny, board, n)
            next_moves.append((exits, nx, ny))

    # Warnsdorff: prioritaskan petak dengan paling sedikit pilihan keluar
    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = move_num
        if knight_tour_recursive(board, nx, ny, move_num + 1, n):
            return True
        board[nx][ny] = 0  # Backtrack

    return False

def solve_knight_tour(n, start_row, start_col):
    """
    Selesaikan Knight's Tour dari posisi awal (start_row, start_col).
    Kembalikan board 2D jika ditemukan, atau None jika tidak ada solusi.
    """
    board = [[0] * n for _ in range(n)]
    board[start_row][start_col] = 1
    if knight_tour_recursive(board, start_row, start_col, 2, n):
        return board
    return None


# ─────────────────────────────────────────────────────────
# 3. KNAPSACK ALGORITHM (Recursive Backtracking)
# ─────────────────────────────────────────────────────────

def knapsack_recursive(items, target, index=0, chosen=None):
    """
    Rekursif: cari subset dari items yang beratnya tepat sama dengan target.
    - Coba masukkan items[index] → kurangi target
    - Jika gagal, coba tanpa items[index] (backtrack)
    Kembalikan list barang yang dipilih, atau None jika tidak ada solusi.
    """
    if chosen is None:
        chosen = []

    # Base case: berhasil mencapai target tepat
    if target == 0:
        return chosen[:]

    # Base case: tidak mungkin (kelebihan berat atau kehabisan barang)
    if target < 0 or index >= len(items):
        return None

    # Pilihan 1: masukkan items[index]
    chosen.append(items[index])
    result = knapsack_recursive(items, target - items[index], index + 1, chosen)
    if result is not None:
        return result
    chosen.pop()  # Backtrack

    # Pilihan 2: lewati items[index]
    return knapsack_recursive(items, target, index + 1, chosen)


# ─────────────────────────────────────────────────────────
# GENERATE HTML VISUALISASI
# ─────────────────────────────────────────────────────────

def generate_nqueens_data():
    """Siapkan data N-Queens untuk ditanamkan ke HTML."""
    data = {}
    for n in range(4, 11):
        solutions = get_nqueens_solutions(n)
        data[n] = solutions[:50]  # Batasi 50 solusi pertama
    return data

def generate_knight_data():
    """Siapkan beberapa contoh Knight's Tour untuk HTML."""
    examples = []
    for n in [5, 6, 7, 8]:
        board = solve_knight_tour(n, 0, 0)
        if board:
            examples.append({"n": n, "board": board})
    return examples

def generate_knapsack_examples():
    """Siapkan beberapa contoh Knapsack."""
    examples = [
        {"items": [2, 5, 6, 9, 12, 14, 20], "target": 30},
        {"items": [1, 3, 4, 5, 8, 10, 15], "target": 22},
        {"items": [3, 7, 9, 11, 14, 17, 22], "target": 40},
    ]
    results = []
    for ex in examples:
        sol = knapsack_recursive(sorted(ex["items"]), ex["target"])
        results.append({
            "items": sorted(ex["items"]),
            "target": ex["target"],
            "solution": sol or []
        })
    return results

def build_html(nq_data, kt_data, ks_data):
    """Bangun file HTML lengkap dengan visualisasi interaktif."""

    import json
    nq_json = json.dumps(nq_data)
    kt_json = json.dumps(kt_data)
    ks_json = json.dumps(ks_data)

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tugas Rekursif — Visualisasi Interaktif</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg:      #f8f7f4;
    --bg2:     #ffffff;
    --bg3:     #eeede9;
    --text:    #1a1a18;
    --text2:   #6b6a65;
    --border:  #dddcD8;
    --blue:    #3b6fd4;
    --green:   #2e7d32;
    --orange:  #e65100;
    --red:     #c62828;
    --purple:  #6a1b9a;
    --shadow:  0 2px 12px rgba(0,0,0,.08);
  }}

  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }}

  /* ── HEADER ── */
  header {{
    background: var(--text);
    color: #fff;
    padding: 28px 40px;
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  header h1 {{ font-size: 22px; font-weight: 600; letter-spacing: -.3px; }}
  header p  {{ font-size: 13px; opacity: .65; margin-top: 4px; }}
  .header-badge {{
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.2);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .5px;
    text-transform: uppercase;
  }}

  /* ── TABS ── */
  .tab-bar {{
    display: flex;
    gap: 0;
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 0 40px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 0 var(--border);
  }}
  .tab-btn {{
    padding: 14px 22px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text2);
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    transition: all .15s;
    white-space: nowrap;
  }}
  .tab-btn:hover {{ color: var(--text); }}
  .tab-btn.active {{
    color: var(--blue);
    border-bottom-color: var(--blue);
  }}

  /* ── LAYOUT ── */
  .page {{ display: none; padding: 36px 40px; max-width: 1100px; margin: 0 auto; }}
  .page.active {{ display: block; }}

  .page-header {{ margin-bottom: 28px; }}
  .page-header h2 {{ font-size: 20px; font-weight: 600; margin-bottom: 6px; }}
  .page-header p  {{ font-size: 14px; color: var(--text2); line-height: 1.6; max-width: 680px; }}

  .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  @media (max-width: 800px) {{ .two-col {{ grid-template-columns: 1fr; }} }}

  /* ── CARD ── */
  .card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    box-shadow: var(--shadow);
  }}
  .card h3 {{
    font-size: 14px;
    font-weight: 600;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: .6px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }}

  /* ── CONTROLS ── */
  .controls {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    padding: 16px;
    background: var(--bg3);
    border-radius: 10px;
    border: 1px solid var(--border);
  }}
  .controls label {{ font-size: 13px; color: var(--text2); font-weight: 500; }}
  .controls input[type=number], .controls input[type=text] {{
    width: 70px;
    padding: 7px 10px;
    font-size: 13px;
    border-radius: 7px;
    border: 1px solid var(--border);
    background: var(--bg2);
    color: var(--text);
    outline: none;
  }}
  .controls input:focus {{ border-color: var(--blue); box-shadow: 0 0 0 3px rgba(59,111,212,.12); }}

  .btn {{
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 8px;
    border: 1px solid var(--border);
    cursor: pointer;
    background: var(--bg2);
    color: var(--text);
    transition: all .15s;
  }}
  .btn:hover {{ background: var(--bg3); }}
  .btn.primary {{
    background: var(--blue);
    color: #fff;
    border-color: var(--blue);
  }}
  .btn.primary:hover {{ background: #2d5ab8; }}
  .btn.success {{
    background: var(--green);
    color: #fff;
    border-color: var(--green);
  }}

  /* ── STATUS BADGE ── */
  .status {{
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 16px;
    border: 1px solid;
  }}
  .status.info    {{ background: #e8f0fe; color: #1a56db; border-color: #bfcfff; }}
  .status.ok      {{ background: #e8f5e9; color: #1b5e20; border-color: #a5d6a7; }}
  .status.err     {{ background: #ffebee; color: #b71c1c; border-color: #ef9a9a; }}
  .status.running {{ background: #fff8e1; color: #e65100; border-color: #ffe082; }}

  /* ── CHESS BOARD ── */
  .board-wrap {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  .chess-board {{
    display: inline-grid;
    border: 2px solid #8b7355;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,.2);
  }}
  .cell {{
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    position: relative;
    transition: all .2s;
  }}
  .cell.light   {{ background: #f0d9b5; color: #8b7355; }}
  .cell.dark    {{ background: #b58863; color: #f0d9b5; }}
  .cell.queen   {{ background: #4a7fcb !important; color: white; }}
  .cell.kt-start   {{ background: #388e3c !important; color: white; }}
  .cell.kt-visited {{ background: #e3f2fd !important; color: #0d47a1; font-weight: 700; }}
  .cell.kt-current {{ background: #ff8f00 !important; color: white; }}

  /* ── SOLUTION LIST ── */
  .sol-nav {{ display: flex; align-items: center; gap: 10px; }}
  .sol-counter {{ font-size: 13px; color: var(--text2); min-width: 120px; }}
  .move-list {{
    font-size: 12px;
    font-family: 'Courier New', monospace;
    color: var(--text2);
    max-height: 100px;
    overflow-y: auto;
    line-height: 1.8;
    margin-top: 8px;
  }}
  .move-chip {{
    display: inline-block;
    background: #e8f0fe;
    color: #1a56db;
    border-radius: 5px;
    padding: 2px 7px;
    margin: 2px;
    font-size: 11px;
    font-family: monospace;
  }}

  /* ── KNAPSACK ── */
  .item-grid {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }}
  .item-chip {{
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    border: 1.5px solid var(--border);
    background: var(--bg3);
    color: var(--text2);
    cursor: pointer;
    transition: all .15s;
    user-select: none;
  }}
  .item-chip:hover {{ border-color: var(--red); color: var(--red); }}
  .item-chip.chosen {{ background: #e8f5e9; border-color: #66bb6a; color: #1b5e20; }}

  .ks-bar-wrap {{
    width: 100%;
    height: 34px;
    background: var(--bg3);
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    position: relative;
    margin: 12px 0;
  }}
  .ks-bar-seg {{
    position: absolute;
    top: 0; height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: white;
    border-right: 1px solid rgba(255,255,255,.4);
    transition: all .3s;
  }}

  /* ── PROGRESS BAR ── */
  .progress {{ width: 100%; height: 4px; background: var(--bg3); border-radius: 2px; overflow: hidden; margin: 8px 0; }}
  .progress-fill {{ height: 100%; background: var(--blue); border-radius: 2px; transition: width .4s; }}

  /* ── CODE BLOCK ── */
  .code-wrap {{
    background: #1e1e2e;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 20px;
  }}
  .code-header {{
    background: #2a2a3e;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 600;
    color: #888;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #333;
  }}
  .code-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
  pre {{
    padding: 20px;
    font-size: 13px;
    line-height: 1.8;
    font-family: 'Courier New', 'Consolas', monospace;
    color: #cdd6f4;
    overflow-x: auto;
  }}
  .kw  {{ color: #cba6f7; font-weight: 600; }}
  .fn  {{ color: #89b4fa; }}
  .cm  {{ color: #6c7086; font-style: italic; }}
  .st  {{ color: #a6e3a1; }}
  .nm  {{ color: #fab387; }}
  .dc  {{ color: #f38ba8; }}

  /* ── STAT CARDS ── */
  .stat-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; margin-bottom: 20px; }}
  .stat-card {{
    background: var(--bg3);
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
    border: 1px solid var(--border);
  }}
  .stat-num  {{ font-size: 26px; font-weight: 700; color: var(--blue); line-height: 1; }}
  .stat-lbl  {{ font-size: 11px; color: var(--text2); margin-top: 4px; font-weight: 500; text-transform: uppercase; letter-spacing: .4px; }}

  /* ── ANIMATION ── */
  @keyframes fadeIn {{ from {{ opacity:0; transform:translateY(6px); }} to {{ opacity:1; transform:none; }} }}
  .board-wrap {{ animation: fadeIn .3s ease; }}
</style>
</head>
<body>

<header>
  <div>
    <h1>Algoritma Rekursif — Visualisasi Interaktif</h1>
    <p>N-Queens · Knight's Tour · Knapsack Problem</p>
  </div>
  <div style="flex:1"></div>
  <span class="header-badge">Python + HTML</span>
</header>

<nav class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('nq')">♛ &nbsp;N-Queens (N-Ratu)</button>
  <button class="tab-btn" onclick="switchTab('kt')">♞ &nbsp;Knight's Tour (Tur Kuda)</button>
  <button class="tab-btn" onclick="switchTab('ks')">🎒 &nbsp;Knapsack (Masalah Tas)</button>
</nav>

<!-- ══════════════════════════════════════════════════
     PAGE 1 : N-QUEENS
══════════════════════════════════════════════════ -->
<div id="page-nq" class="page active">
  <div class="page-header">
    <h2>♛ N-Queens Problem (N-Ratu)</h2>
    <p>Tempatkan N ratu pada papan N×N sehingga tidak ada dua ratu yang saling menyerang — tidak boleh berada di baris, kolom, maupun diagonal yang sama. Menggunakan <strong>backtracking rekursif</strong>.</p>
  </div>

  <div class="stat-grid" id="nq-stats">
    <div class="stat-card"><div class="stat-num" id="nq-sol-num">—</div><div class="stat-lbl">Total Solusi</div></div>
    <div class="stat-card"><div class="stat-num" id="nq-viewing">—</div><div class="stat-lbl">Ditampilkan</div></div>
    <div class="stat-card"><div class="stat-num" id="nq-nval">8</div><div class="stat-lbl">Ukuran Papan</div></div>
  </div>

  <div class="controls">
    <label>Ukuran papan N :</label>
    <input type="number" id="nq-n" value="8" min="4" max="10">
    <button class="btn primary" onclick="nqSolve()">▶ &nbsp;Cari Semua Solusi</button>
    <button class="btn" onclick="nqPrev()">← Sebelumnya</button>
    <button class="btn" onclick="nqNext()">Berikutnya →</button>
    <button class="btn success" onclick="nqRandom()">🎲 Acak</button>
  </div>

  <div id="nq-status" class="status info">Pilih ukuran papan lalu tekan "Cari Semua Solusi".</div>

  <div class="two-col">
    <div>
      <div class="board-wrap" id="nq-board"></div>
      <div class="move-list" id="nq-placement" style="margin-top:10px;text-align:center"></div>
    </div>
    <div class="card">
      <h3>Kode Python</h3>
      <div class="code-wrap">
        <div class="code-header">
          <span class="code-dot" style="background:#ff5f56"></span>
          <span class="code-dot" style="background:#ffbd2e"></span>
          <span class="code-dot" style="background:#27c93f"></span>
          <span style="margin-left:4px">nqueens.py</span>
        </div>
        <pre><span class="kw">def</span> <span class="fn">is_safe</span>(board, row, col, n):
    <span class="st">&#34;&#34;&#34;Cek keamanan posisi (row, col).&#34;&#34;&#34;</span>
    <span class="kw">for</span> i <span class="kw">in</span> range(row):
        <span class="kw">if</span> board[i] == col:
            <span class="kw">return False</span>
        <span class="kw">if</span> abs(board[i]-col) == abs(i-row):
            <span class="kw">return False</span>
    <span class="kw">return True</span>

<span class="kw">def</span> <span class="fn">solve</span>(board, row, n, solutions):
    <span class="cm"># Base case: semua baris sudah terisi</span>
    <span class="kw">if</span> row == n:
        solutions.append(board[:])
        <span class="kw">return</span>
    <span class="kw">for</span> col <span class="kw">in</span> range(n):
        <span class="kw">if</span> is_safe(board, row, col, n):
            board[row] = col   <span class="cm"># Tempatkan ratu</span>
            solve(board, row+<span class="nm">1</span>, n, solutions)
            board[row] = -<span class="nm">1</span>  <span class="cm"># Backtrack</span>

<span class="cm"># Jalankan:</span>
n = <span class="nm">8</span>
solutions = []
solve([-<span class="nm">1</span>]*n, <span class="nm">0</span>, n, solutions)
<span class="dc">print</span>(f<span class="st">"Ditemukan {{len(solutions)}} solusi"</span>)</pre>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════
     PAGE 2 : KNIGHT'S TOUR
══════════════════════════════════════════════════ -->
<div id="page-kt" class="page">
  <div class="page-header">
    <h2>♞ Knight's Tour (Tur Kuda)</h2>
    <p>Kuda catur harus mengunjungi <strong>setiap petak tepat satu kali</strong>. Menggunakan backtracking rekursif + <strong>Warnsdorff's Heuristic</strong>: selalu pilih petak berikutnya yang memiliki paling sedikit pilihan lanjutan.</p>
  </div>

  <div class="stat-grid">
    <div class="stat-card"><div class="stat-num" id="kt-total">—</div><div class="stat-lbl">Total Petak</div></div>
    <div class="stat-card"><div class="stat-num" id="kt-step-show">—</div><div class="stat-lbl">Langkah Saat Ini</div></div>
    <div class="stat-card"><div class="stat-num" id="kt-nval">6</div><div class="stat-lbl">Ukuran Papan</div></div>
  </div>

  <div class="controls">
    <label>Ukuran papan:</label>
    <input type="number" id="kt-n" value="6" min="5" max="8">
    <label>Baris awal (0-based):</label>
    <input type="number" id="kt-r" value="0" min="0" max="7">
    <label>Kolom awal:</label>
    <input type="number" id="kt-c" value="0" min="0" max="7">
    <button class="btn primary" onclick="ktSolve()">▶ &nbsp;Cari Tur</button>
    <button class="btn success" onclick="ktAnimate()">⏵ &nbsp;Animasi</button>
    <button class="btn" onclick="ktReset()">⏹ Stop</button>
  </div>

  <div id="kt-status" class="status info">Masukkan posisi awal kuda dan tekan "Cari Tur".</div>
  <div class="progress"><div class="progress-fill" id="kt-prog" style="width:0%"></div></div>

  <div class="two-col">
    <div>
      <div class="board-wrap" id="kt-board"></div>
      <div class="move-list" id="kt-movelist" style="margin-top:10px"></div>
    </div>
    <div class="card">
      <h3>Kode Python</h3>
      <div class="code-wrap">
        <div class="code-header">
          <span class="code-dot" style="background:#ff5f56"></span>
          <span class="code-dot" style="background:#ffbd2e"></span>
          <span class="code-dot" style="background:#27c93f"></span>
          <span style="margin-left:4px">knight_tour.py</span>
        </div>
        <pre><span class="cm"># Arah gerak kuda (8 kemungkinan)</span>
DX = [-<span class="nm">2</span>,-<span class="nm">1</span>,<span class="nm">1</span>,<span class="nm">2</span>, <span class="nm">2</span>, <span class="nm">1</span>,-<span class="nm">1</span>,-<span class="nm">2</span>]
DY = [ <span class="nm">1</span>, <span class="nm">2</span>,<span class="nm">2</span>,<span class="nm">1</span>,-<span class="nm">1</span>,-<span class="nm">2</span>,-<span class="nm">2</span>,-<span class="nm">1</span>]

<span class="kw">def</span> <span class="fn">exits</span>(x, y, board, n):
    <span class="cm">&#34;&#34;&#34;Hitung jumlah langkah valid dari (x,y).&#34;&#34;&#34;</span>
    <span class="kw">return</span> sum(<span class="nm">1</span> <span class="kw">for</span> i <span class="kw">in</span> range(<span class="nm">8</span>)
               <span class="kw">if</span> <span class="nm">0</span><=x+DX[i]<n <span class="kw">and</span>
                  <span class="nm">0</span><=y+DY[i]<n <span class="kw">and</span>
                  board[x+DX[i]][y+DY[i]]==<span class="nm">0</span>)

<span class="kw">def</span> <span class="fn">tour</span>(board, x, y, move, n):
    <span class="kw">if</span> move > n*n:
        <span class="kw">return True</span>  <span class="cm"># Selesai!</span>
    nexts = [(exits(x+DX[i],y+DY[i],board,n),
              x+DX[i], y+DY[i])
             <span class="kw">for</span> i <span class="kw">in</span> range(<span class="nm">8</span>)
             <span class="kw">if</span> <span class="nm">0</span><=x+DX[i]<n <span class="kw">and</span>
                <span class="nm">0</span><=y+DY[i]<n <span class="kw">and</span>
                board[x+DX[i]][y+DY[i]]==<span class="nm">0</span>]
    <span class="cm"># Warnsdorff: urutkan dari exit terkecil</span>
    nexts.sort()
    <span class="kw">for</span> _, nx, ny <span class="kw">in</span> nexts:
        board[nx][ny] = move
        <span class="kw">if</span> tour(board, nx, ny, move+<span class="nm">1</span>, n):
            <span class="kw">return True</span>
        board[nx][ny] = <span class="nm">0</span>  <span class="cm"># Backtrack</span>
    <span class="kw">return False</span></pre>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════
     PAGE 3 : KNAPSACK
══════════════════════════════════════════════════ -->
<div id="page-ks" class="page">
  <div class="page-header">
    <h2>🎒 Knapsack Problem (Masalah Tas)</h2>
    <p>Temukan subset dari kumpulan barang yang totalnya <strong>tepat sama</strong> dengan berat target. Algoritma rekursif mencoba memasukkan/melewati setiap barang, dan backtrack jika melebihi target.</p>
  </div>

  <div class="two-col">
    <div>
      <div class="controls">
        <label>Berat target (pon):</label>
        <input type="number" id="ks-target" value="30" min="1" max="300">
        <label>Tambah item:</label>
        <input type="number" id="ks-add" value="7" min="1" max="100">
        <button class="btn" onclick="ksAdd()">+ Tambah</button>
        <button class="btn primary" onclick="ksSolve()">▶ &nbsp;Selesaikan</button>
        <button class="btn" onclick="ksReset()">Reset</button>
      </div>

      <div style="font-size:12px;color:var(--text2);margin-bottom:8px">
        Klik item untuk menghapus &nbsp;·&nbsp; Hijau = masuk solusi
      </div>
      <div class="item-grid" id="ks-chips"></div>

      <div id="ks-status" class="status info">Masukkan berat target dan tekan "Selesaikan".</div>

      <div id="ks-bar-wrap" style="display:none">
        <div style="font-size:13px;font-weight:600;margin-bottom:8px">Visualisasi kapasitas tas:</div>
        <div class="ks-bar-wrap"><div id="ks-bar-inner"></div></div>
        <div style="font-size:12px;color:var(--text2);margin-top:4px" id="ks-bar-label"></div>
      </div>

      <div id="ks-detail" style="margin-top:16px"></div>
    </div>

    <div>
      <div class="card" style="margin-bottom:16px">
        <h3>Contoh Soal</h3>
        <div id="ks-examples"></div>
      </div>
      <div class="card">
        <h3>Kode Python</h3>
        <div class="code-wrap">
          <div class="code-header">
            <span class="code-dot" style="background:#ff5f56"></span>
            <span class="code-dot" style="background:#ffbd2e"></span>
            <span class="code-dot" style="background:#27c93f"></span>
            <span style="margin-left:4px">knapsack.py</span>
          </div>
          <pre><span class="kw">def</span> <span class="fn">knapsack</span>(items, target,
              idx=<span class="nm">0</span>, chosen=None):
    <span class="st">&#34;&#34;&#34;Rekursif: cari subset
    yang totalnya == target.&#34;&#34;&#34;</span>
    <span class="kw">if</span> chosen <span class="kw">is None</span>: chosen = []

    <span class="cm"># Berhasil!</span>
    <span class="kw">if</span> target == <span class="nm">0</span>:
        <span class="kw">return</span> chosen[:]

    <span class="cm"># Gagal (over/habis)</span>
    <span class="kw">if</span> target < <span class="nm">0</span> <span class="kw">or</span> idx >= len(items):
        <span class="kw">return None</span>

    <span class="cm"># Coba masukkan items[idx]</span>
    chosen.append(items[idx])
    res = knapsack(items,
                   target - items[idx],
                   idx+<span class="nm">1</span>, chosen)
    <span class="kw">if</span> res <span class="kw">is not None</span>:
        <span class="kw">return</span> res
    chosen.pop()  <span class="cm"># Backtrack!</span>

    <span class="cm"># Coba tanpa items[idx]</span>
    <span class="kw">return</span> knapsack(items, target,
                    idx+<span class="nm">1</span>, chosen)</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════════
     JAVASCRIPT
══════════════════════════════════════════════════ -->
<script>
// ── EMBEDDED DATA FROM PYTHON ──
const NQ_DATA = {nq_json};
const KT_DATA = {kt_json};
const KS_DATA = {ks_json};

// ════════════════════════════════════
// TAB SWITCHING
// ════════════════════════════════════
function switchTab(name) {{
  const tabs = ['nq','kt','ks'];
  tabs.forEach((t,i) => {{
    document.querySelectorAll('.tab-btn')[i].classList.toggle('active', t===name);
    document.getElementById('page-'+t).classList.toggle('active', t===name);
  }});
}}

// ════════════════════════════════════
// HELPERS
// ════════════════════════════════════
function setStatus(id, msg, type='info') {{
  const el = document.getElementById(id);
  el.className = 'status ' + type;
  el.textContent = msg;
}}

function cellSize(n) {{ return Math.max(32, Math.min(56, Math.floor(440/n))); }}

// ════════════════════════════════════
// N-QUEENS
// ════════════════════════════════════
let nqSolutions = [], nqIdx = 0;

function nqSolve() {{
  const n = parseInt(document.getElementById('nq-n').value);
  if (n < 4 || n > 10) {{ setStatus('nq-status','Ukuran papan harus 4–10.','err'); return; }}
  setStatus('nq-status','Mencari solusi...','running');
  setTimeout(() => {{
    nqSolutions = NQ_DATA[n] || [];
    nqIdx = 0;
    document.getElementById('nq-sol-num').textContent = nqSolutions.length;
    document.getElementById('nq-nval').textContent = n;
    if (nqSolutions.length) {{
      setStatus('nq-status', `✓ ${{nqSolutions.length}} solusi ditemukan untuk papan ${{n}}×${{n}}!`,'ok');
      nqDraw(nqSolutions[0], n);
    }} else {{
      setStatus('nq-status','Tidak ada solusi ditemukan.','err');
    }}
  }}, 10);
}}

function nqDraw(board, n) {{
  const sz = cellSize(n);
  nqIdx = nqSolutions.indexOf(board);
  document.getElementById('nq-viewing').textContent = (nqIdx+1) + ' / ' + nqSolutions.length;
  let html = `<div class="chess-board" style="grid-template-columns:repeat(${{n}},${{sz}}px)">`;
  for (let r=0;r<n;r++) for (let c=0;c<n;c++) {{
    const isQ = board[r]===c;
    const light = (r+c)%2===0;
    html += `<div class="cell ${{isQ?'queen':(light?'light':'dark')}}" style="width:${{sz}}px;height:${{sz}}px;font-size:${{isQ?Math.round(sz*.55):12}}px">`;
    if (isQ) html += '♛';
    html += '</div>';
  }}
  html += '</div>';
  document.getElementById('nq-board').innerHTML = html;
  document.getElementById('nq-placement').innerHTML =
    '<b style="font-size:12px;color:#666">Kolom ratu per baris:</b> ' +
    board.map((c,r)=>`<span class="move-chip">baris ${{r}}→kol ${{c}}</span>`).join('');
}}

function nqNext() {{
  if (!nqSolutions.length) return;
  const n = parseInt(document.getElementById('nq-n').value);
  nqIdx = (nqIdx+1) % nqSolutions.length;
  setStatus('nq-status',`Solusi ${{nqIdx+1}} dari ${{nqSolutions.length}}`,'ok');
  nqDraw(nqSolutions[nqIdx], n);
}}
function nqPrev() {{
  if (!nqSolutions.length) return;
  const n = parseInt(document.getElementById('nq-n').value);
  nqIdx = (nqIdx-1+nqSolutions.length) % nqSolutions.length;
  setStatus('nq-status',`Solusi ${{nqIdx+1}} dari ${{nqSolutions.length}}`,'ok');
  nqDraw(nqSolutions[nqIdx], n);
}}
function nqRandom() {{
  if (!nqSolutions.length) {{ nqSolve(); return; }}
  const n = parseInt(document.getElementById('nq-n').value);
  nqIdx = Math.floor(Math.random()*nqSolutions.length);
  setStatus('nq-status',`Solusi acak: ${{nqIdx+1}} dari ${{nqSolutions.length}}`,'ok');
  nqDraw(nqSolutions[nqIdx], n);
}}

// ════════════════════════════════════
// KNIGHT'S TOUR
// ════════════════════════════════════
let ktBoard = null, ktMoves = [], ktN = 6, ktAnimTimer = null;

// 8 arah gerak kuda
const DX = [-2,-1,1,2,2,1,-1,-2];
const DY = [1,2,2,1,-1,-2,-2,-1];

function ktCountExits(x,y,board,n) {{
  let c=0;
  for(let i=0;i<8;i++){{const nx=x+DX[i],ny=y+DY[i];if(nx>=0&&nx<n&&ny>=0&&ny<n&&board[nx][ny]===0)c++;}}
  return c;
}}
function ktRecurse(board,x,y,move,n) {{
  if(move>n*n)return true;
  let nexts=[];
  for(let i=0;i<8;i++){{const nx=x+DX[i],ny=y+DY[i];if(nx>=0&&nx<n&&ny>=0&&ny<n&&board[nx][ny]===0)nexts.push([ktCountExits(nx,ny,board,n),nx,ny]);}}
  nexts.sort((a,b)=>a[0]-b[0]);
  for(const[,nx,ny]of nexts){{board[nx][ny]=move;if(ktRecurse(board,nx,ny,move+1,n))return true;board[nx][ny]=0;}}
  return false;
}}

function ktSolve() {{
  ktReset();
  ktN = parseInt(document.getElementById('kt-n').value)||6;
  const r0 = parseInt(document.getElementById('kt-r').value)||0;
  const c0 = parseInt(document.getElementById('kt-c').value)||0;
  if(r0<0||r0>=ktN||c0<0||c0>=ktN){{setStatus('kt-status','Posisi awal di luar papan!','err');return;}}
  setStatus('kt-status','Mencari tur dengan Warnsdorff heuristic...','running');
  document.getElementById('kt-prog').style.width='20%';
  document.getElementById('kt-total').textContent = ktN*ktN;
  document.getElementById('kt-nval').textContent = ktN;
  setTimeout(()=>{{
    ktBoard = Array.from({{length:ktN}},()=>new Array(ktN).fill(0));
    ktBoard[r0][c0]=1;
    const found = ktRecurse(ktBoard,r0,c0,2,ktN);
    document.getElementById('kt-prog').style.width='100%';
    if(found){{
      // Bangun urutan langkah
      ktMoves = new Array(ktN*ktN);
      for(let i=0;i<ktN;i++)for(let j=0;j<ktN;j++)ktMoves[ktBoard[i][j]-1]={{r:i,c:j}};
      setStatus('kt-status',`✓ Tur lengkap! ${{ktN*ktN}} langkah berhasil ditemukan.`,'ok');
      document.getElementById('kt-step-show').textContent = ktN*ktN;
      ktDraw(ktBoard, -1);
      let ml = '<b style="font-size:12px;color:#666">Urutan koordinat (baris,kol):</b><br>';
      ktMoves.forEach((m,i)=>ml+=`<span class="move-chip">${{i+1}}:(${{m.r}},${{m.c}})</span>`);
      document.getElementById('kt-movelist').innerHTML = ml;
    }} else {{
      setStatus('kt-status','Tidak ada tur dari posisi ini. Coba posisi lain.','err');
    }}
  }},10);
}}

function ktDraw(board, highlight) {{
  const n = ktN;
  const sz = cellSize(n);
  let html=`<div class="chess-board" style="grid-template-columns:repeat(${{n}},${{sz}}px)">`;
  for(let r=0;r<n;r++) for(let c=0;c<n;c++) {{
    const v=board[r][c];
    const light=(r+c)%2===0;
    let cls=light?'light':'dark';
    if(v===1&&highlight<0) cls='kt-start';
    else if(v===highlight) cls='kt-current';
    else if(v>0) cls='kt-visited';
    const fs = sz<40?9:11;
    html+=`<div class="cell ${{cls}}" style="width:${{sz}}px;height:${{sz}}px;font-size:${{fs}}px">`;
    if(v===highlight||( v===1&&highlight<0)) html+='♞'; else if(v>0) html+=v;
    html+='</div>';
  }}
  html+='</div>';
  document.getElementById('kt-board').innerHTML=html;
}}

function ktAnimate() {{
  if(!ktBoard){{ktSolve();return;}}
  const aBoard=Array.from({{length:ktN}},()=>new Array(ktN).fill(0));
  let step=0;
  ktAnimTimer=setInterval(()=>{{
    if(step>=ktMoves.length){{clearInterval(ktAnimTimer);ktAnimTimer=null;return;}}
    const m=ktMoves[step];
    aBoard[m.r][m.c]=step+1;
    ktDraw(aBoard, step+1);
    document.getElementById('kt-step-show').textContent=step+1;
    document.getElementById('kt-prog').style.width=((step+1)/(ktN*ktN)*100)+'%';
    step++;
  }},100);
}}
function ktReset() {{
  if(ktAnimTimer){{clearInterval(ktAnimTimer);ktAnimTimer=null;}}
  ktBoard=null; ktMoves=[];
  document.getElementById('kt-board').innerHTML='';
  document.getElementById('kt-movelist').innerHTML='';
  document.getElementById('kt-prog').style.width='0%';
  document.getElementById('kt-step-show').textContent='—';
  setStatus('kt-status','Masukkan posisi awal kuda dan tekan "Cari Tur".','info');
}}

// ════════════════════════════════════
// KNAPSACK
// ════════════════════════════════════
let ksItems = [2,5,6,9,12,14,20];
let ksSolution = null;
const BAR_COLORS = ['#388e3c','#2e7d32','#43a047','#66bb6a','#81c784','#4caf50','#a5d6a7'];

function ksRenderChips() {{
  const solSet = new Set(ksSolution||[]);
  document.getElementById('ks-chips').innerHTML = ksItems.map((w,i)=>
    `<span class="item-chip ${{ksSolution&&ksSolution.includes(w)?'chosen':''}}"
      onclick="ksRemove(${{i}})" title="Klik untuk hapus">${{w}} pon</span>`
  ).join('');
}}

function ksAdd() {{
  const v=parseInt(document.getElementById('ks-add').value);
  if(!isNaN(v)&&v>0){{ksItems.push(v);ksItems.sort((a,b)=>a-b);ksSolution=null;ksRenderChips();}}
}}
function ksRemove(i) {{ ksItems.splice(i,1); ksSolution=null; ksRenderChips(); }}
function ksReset() {{
  ksItems=[2,5,6,9,12,14,20]; ksSolution=null; ksRenderChips();
  setStatus('ks-status','Masukkan berat target dan tekan "Selesaikan".','info');
  document.getElementById('ks-bar-wrap').style.display='none';
  document.getElementById('ks-detail').innerHTML='';
}}

function ksRecurse(items,target,idx,chosen) {{
  if(target===0)return chosen.slice();
  if(target<0||idx>=items.length)return null;
  chosen.push(items[idx]);
  let r=ksRecurse(items,target-items[idx],idx+1,chosen);
  if(r!==null)return r;
  chosen.pop();
  return ksRecurse(items,target,idx+1,chosen);
}}

function ksSolve() {{
  const target=parseInt(document.getElementById('ks-target').value);
  if(isNaN(target)||target<=0)return;
  setStatus('ks-status','Mencari kombinasi...','running');
  setTimeout(()=>{{
    ksSolution = ksRecurse(ksItems.slice().sort((a,b)=>a-b), target, 0, []);
    ksRenderChips();
    if(ksSolution){{
      const total=ksSolution.reduce((a,b)=>a+b,0);
      setStatus('ks-status',`✓ Solusi ditemukan! Barang: [${{ksSolution.join(', ')}}] — Total: ${{total}} dari ${{target}} pon.`,'ok');
      // Bar visualisasi
      document.getElementById('ks-bar-wrap').style.display='block';
      let offset=0, barHTML='';
      ksSolution.forEach((w,i)=>{{
        const pct=(w/target)*100;
        barHTML+=`<div class="ks-bar-seg" style="left:${{offset}}%;width:${{pct}}%;background:${{BAR_COLORS[i%BAR_COLORS.length]}}">${{w>2?w:''}}</div>`;
        offset+=pct;
      }});
      document.getElementById('ks-bar-inner').innerHTML=barHTML;
      const unused=ksItems.filter(x=>!ksSolution.includes(x));
      document.getElementById('ks-bar-label').textContent=
        `Terpakai: ${{total}}/${{target}} pon  ·  Tidak dipilih: ${{unused.length?unused.join(', ')+' pon':'(semua dipilih)'}}`;
      // Detail tabel
      let det='<div class="card" style="margin-top:0"><h3>Rincian Solusi</h3><table style="width:100%;font-size:13px;border-collapse:collapse">';
      det+='<tr style="border-bottom:1px solid var(--border)"><th style="text-align:left;padding:6px 4px;color:var(--text2)">Barang</th><th style="text-align:right;padding:6px 4px;color:var(--text2)">Status</th><th style="text-align:right;padding:6px 4px;color:var(--text2)">Berat</th></tr>';
      ksItems.forEach((w,i)=>{{
        const inc=ksSolution.includes(w);
        det+=`<tr style="border-bottom:1px solid var(--bg3)"><td style="padding:6px 4px">Barang #${{i+1}}</td><td style="text-align:right;padding:6px 4px"><span style="color:${{inc?'#2e7d32':'#999'}};font-weight:600">${{inc?'✓ Dipilih':'— Dilewati'}}</span></td><td style="text-align:right;padding:6px 4px;font-family:monospace;font-weight:${{inc?700:400}}">${{w}} pon</td></tr>`;
      }});
      det+=`<tr style="background:var(--bg3)"><td colspan="2" style="padding:8px 4px;font-weight:700">Total Terpilih</td><td style="text-align:right;padding:8px 4px;font-weight:700;font-family:monospace">${{total}} pon</td></tr>`;
      det+='</table></div>';
      document.getElementById('ks-detail').innerHTML=det;
    }} else {{
      setStatus('ks-status',`✗ Tidak ada kombinasi yang tepat = ${{target}} pon. Coba ubah target atau tambah item.`,'err');
      document.getElementById('ks-bar-wrap').style.display='none';
      document.getElementById('ks-detail').innerHTML='';
    }}
  }},10);
}}

// Render contoh soal
(function() {{
  let html='';
  KS_DATA.forEach((ex,i)=>{{
    html+=`<div style="padding:10px 0;border-bottom:1px solid var(--border);${{i===KS_DATA.length-1?'border:none':''}}">
      <div style="font-size:13px;font-weight:600;margin-bottom:4px">Contoh ${{i+1}}: target = ${{ex.target}} pon</div>
      <div style="font-size:12px;color:var(--text2);margin-bottom:4px">Item: [${{ex.items.join(', ')}}]</div>`;
    if(ex.solution.length){{
      html+=`<div style="font-size:12px;color:#2e7d32;font-weight:600">✓ Solusi: [${{ex.solution.join(' + ')}}] = ${{ex.solution.reduce((a,b)=>a+b,0)}}</div>`;
    }} else {{
      html+=`<div style="font-size:12px;color:#b71c1c">✗ Tidak ada solusi tepat</div>`;
    }}
    html+=`<button class="btn" style="margin-top:6px;font-size:12px;padding:4px 12px"
      onclick="loadKsExample(${{i}})">Coba contoh ini →</button>`;
    html+='</div>';
  }});
  document.getElementById('ks-examples').innerHTML=html;
}})();

function loadKsExample(i) {{
  const ex=KS_DATA[i];
  ksItems=ex.items.slice();
  document.getElementById('ks-target').value=ex.target;
  ksSolution=null;
  ksRenderChips();
  ksSolve();
}}

// ── INIT ──
ksRenderChips();
nqSolve();
</script>
</body>
</html>"""
    return html

# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  TUGAS REKURSIF — Membangun Visualisasi")
    print("=" * 60)

    print("\n[1/4] Menghitung solusi N-Queens (N = 4 hingga 10)...")
    nq_data = generate_nqueens_data()
    for n, sols in nq_data.items():
        print(f"      N={n} : {len(sols)} solusi")

    print("\n[2/4] Menyelesaikan Knight's Tour (Warnsdorff)...")
    kt_data = generate_knight_data()
    for ex in kt_data:
        print(f"      Papan {ex['n']}×{ex['n']} dari (0,0) : {'✓ Ditemukan' if ex['board'] else '✗ Tidak ada'}")

    print("\n[3/4] Menyelesaikan Knapsack (contoh soal)...")
    ks_data = generate_knapsack_examples()
    for ex in ks_data:
        sol = ex['solution']
        status = f"✓ [{', '.join(map(str,sol))}] = {sum(sol)}" if sol else "✗ Tidak ada solusi"
        print(f"      Target {ex['target']} dari {ex['items']} → {status}")

    print("\n[4/4] Membuat file HTML visualisasi...")
    html = build_html(nq_data, kt_data, ks_data)

    # Simpan file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rekursif_output.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✓ File berhasil dibuat: {output_path}")
    print("\n  Membuka browser...")
    webbrowser.open(f"file://{output_path}")
    print("\n  Selesai! Visualisasi interaktif siap digunakan.")
    print("=" * 60)

if __name__ == "__main__":
    main()
