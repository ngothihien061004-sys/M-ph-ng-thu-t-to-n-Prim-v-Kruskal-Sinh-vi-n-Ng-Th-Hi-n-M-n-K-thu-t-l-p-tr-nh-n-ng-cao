import tkinter as tk
from tkinter import messagebox
import heapq

# ======================
# Thuật toán Prim
# ======================
def prim(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * n
    heap = [(0, 0, -1)]
    mst = []
    total = 0

    while heap:
        w, u, parent = heapq.heappop(heap)
        if visited[u]:
            continue

        visited[u] = True
        total += w

        if parent != -1:
            mst.append((parent, u, w))

        for v, weight in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (weight, v, u))

    return mst, total


# ======================
# Kruskal
# ======================
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, x, y):
    rx = find(parent, x)
    ry = find(parent, y)

    if rx != ry:
        if rank[rx] > rank[ry]:
            parent[ry] = rx
        elif rank[rx] < rank[ry]:
            parent[rx] = ry
        else:
            parent[ry] = rx
            rank[rx] += 1

def kruskal(n, edges):
    edges = sorted(edges, key=lambda x: x[2])
    parent = list(range(n))
    rank = [0] * n
    mst = []
    total = 0

    for u, v, w in edges:
        if find(parent, u) != find(parent, v):
            union(parent, rank, u, v)
            mst.append((u, v, w))
            total += w

    return mst, total


# ======================
# Chạy thuật toán
# ======================
def run_algorithm():
    try:
        n = int(entry_vertices.get())
        lines = text_edges.get("1.0", tk.END).strip().split("\n")

        edges = []
        for line in lines:
            u, v, w = map(int, line.split())
            edges.append((u, v, w))

        if algo_var.get() == "Prim":
            mst, total = prim(n, edges)
        else:
            mst, total = kruskal(n, edges)

        result_text.config(state="normal")
        result_text.delete("1.0", tk.END)

        result_text.insert(tk.END, "CÂY KHUNG NHỎ NHẤT\n\n")
        for u, v, w in mst:
            result_text.insert(tk.END, f"{u} — {v}  |  Trọng số = {w}\n")

        result_text.insert(tk.END, f"\nTỔNG TRỌNG SỐ = {total}")
        result_text.config(state="disabled")

    except:
        messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng!")


# ======================
# GIAO DIỆN
# ======================
root = tk.Tk()
root.title("Mô phỏng thuật toán Prim và Kruskal")
root.geometry("600x650")
root.resizable(False, False)

title = tk.Label(root, text="MÔ PHỎNG THUẬT TOÁN PRIM & KRUSKAL",
                 font=("Arial", 14, "bold"))
title.pack(pady=10)

frame_top = tk.Frame(root)
frame_top.pack(pady=5)

tk.Label(frame_top, text="Số đỉnh:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
entry_vertices = tk.Entry(frame_top, width=10)
entry_vertices.grid(row=0, column=1)

tk.Label(root, text="Nhập cạnh (u v w):", font=("Arial", 11)).pack()

text_edges = tk.Text(root, height=10, width=60)
text_edges.pack(pady=5)

algo_var = tk.StringVar(value="Prim")

frame_algo = tk.Frame(root)
frame_algo.pack(pady=5)

tk.Radiobutton(frame_algo, text="Prim", variable=algo_var,
               value="Prim", font=("Arial", 11)).grid(row=0, column=0, padx=10)

tk.Radiobutton(frame_algo, text="Kruskal", variable=algo_var,
               value="Kruskal", font=("Arial", 11)).grid(row=0, column=1, padx=10)

tk.Button(root, text="Chạy thuật toán",
          command=run_algorithm,
          bg="#4CAF50", fg="white",
          font=("Arial", 11, "bold"),
          width=20).pack(pady=10)

tk.Label(root, text="Kết quả:", font=("Arial", 12, "bold")).pack()

result_text = tk.Text(root, height=12, width=60, state="disabled")
result_text.pack(pady=5)

root.mainloop()