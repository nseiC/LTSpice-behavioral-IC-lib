"""Leitor minimo do formato .raw binario do ngspice (dados reais)."""
import numpy as np


def read_raw(path):
    """ngspice binary rawfile (real transient data) -> {name: array}"""
    with open(path, "rb") as f:
        data = f.read()
    k = data.index(b"Binary:\n")
    head = data[:k].decode("latin-1").splitlines()
    nvar = int(next(l for l in head if l.startswith("No. Variables")).split(":")[1])
    npt = int(next(l for l in head if l.startswith("No. Points")).split(":")[1])
    i = head.index("Variables:")
    names = [head[i + 1 + j].split()[1].lower() for j in range(nvar)]
    arr = np.frombuffer(data[k + 8:], dtype="<f8", count=nvar * npt).reshape(npt, nvar)
    return {n: arr[:, j].copy() for j, n in enumerate(names)}
