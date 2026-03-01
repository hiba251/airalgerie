# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 16:42:54 2026

@author: User
"""

import os

print("CWD =", os.getcwd())

# écrit DIRECTEMENT sur le Bureau (Windows)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
path = os.path.join(desktop, "spyder_test_write.txt")

with open(path, "w", encoding="utf-8") as f:
    f.write("OK - Spyder can write files.\n")

print("Wrote:", path)