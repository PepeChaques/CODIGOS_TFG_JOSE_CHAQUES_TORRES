import sys
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

if len(sys.argv) != 2:
    print("Para usar el script: python3 DBSCAN.py archivo.pcd")
    sys.exit(1)