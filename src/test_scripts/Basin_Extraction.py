"""
Strahler order-N basin delineation from a DEM (set ORDER).

WhiteboxTools is used only for DEM conditioning and the D8 pointer.
Everything else (accumulation, streams, Strahler order, link IDs, link
catchments) is computed from that single pointer in one consistent pass,
so the network topology cannot disagree with itself.

Requires: whitebox, numpy, numba, rasterio, geopandas, shapely
"""
import os
import numpy as np
import rasterio
import geopandas as gpd
from rasterio.features import shapes
from shapely.geometry import shape
from numba import njit
import whitebox

# ---------------------------------------------------------------- settings
WORK_DIR = os.path.abspath("Oregon_Coast_Range_Files")
DEM = "Umpqua_10m_2.tif"
BREACH_DIST = 50          # cells
THRESHOLD = 500           # contributing cells for channel initiation
ORDER = 5                 # Strahler order of basins to extract
OUT_SHP = f"Umpqua_Order{ORDER}_Basins.shp"

# WhiteboxTools D8 encoding: 1=NE 2=E 4=SE 8=S 16=SW 32=W 64=NW 128=N
CODES = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.int64)
DR = np.array([-1, 0, 1, 1, 1, 0, -1, -1], dtype=np.int64)
DC = np.array([1, 1, 1, 0, -1, -1, -1, 0], dtype=np.int64)


@njit
def downstream_index(pntr, valid):
    """Flat index of the downstream cell, -1 if none/off-grid/invalid."""
    nr, nc = pntr.shape
    ds = -np.ones(nr * nc, dtype=np.int64)
    for r in range(nr):
        for c in range(nc):
            i = r * nc + c
            if not valid[i]:
                continue
            p = pntr[r, c]
            for k in range(8):
                if p == CODES[k]:
                    rr = r + DR[k]
                    cc = c + DC[k]
                    if 0 <= rr < nr and 0 <= cc < nc:
                        j = rr * nc + cc
                        if valid[j]:
                            ds[i] = j
                    break
    return ds


@njit
def topological_order(ds, valid):
    """Upstream-to-downstream ordering (Kahn's algorithm)."""
    n = ds.size
    indeg = np.zeros(n, dtype=np.int32)
    for i in range(n):
        if valid[i] and ds[i] >= 0:
            indeg[ds[i]] += 1
    order = np.empty(n, dtype=np.int64)
    head = 0
    tail = 0
    for i in range(n):
        if valid[i] and indeg[i] == 0:
            order[tail] = i
            tail += 1
    while head < tail:
        i = order[head]
        head += 1
        j = ds[i]
        if j >= 0:
            indeg[j] -= 1
            if indeg[j] == 0:
                order[tail] = j
                tail += 1
    return order[:tail]


@njit
def network(ds, order, threshold):
    """Accumulation, stream mask, Strahler order, link IDs, link catchments."""
    n = ds.size
    acc = np.ones(n, dtype=np.int64)
    for i in order:
        if ds[i] >= 0:
            acc[ds[i]] += acc[i]
    stream = acc >= threshold

    so = np.zeros(n, dtype=np.int32)        # Strahler order (stream cells)
    link = np.zeros(n, dtype=np.int64)      # link ID (stream cells)
    nin = np.zeros(n, dtype=np.int32)       # number of stream inflows
    maxin = np.zeros(n, dtype=np.int32)     # max inflow order
    nmax = np.zeros(n, dtype=np.int32)      # inflows sharing max order
    inlink = np.zeros(n, dtype=np.int64)    # link of the single inflow
    link_order = np.zeros(n + 1, dtype=np.int32)
    nlinks = 0

    for i in order:                          # upstream -> downstream
        if not stream[i]:
            continue
        if nin[i] == 0:
            so[i] = 1
        elif nmax[i] >= 2:
            so[i] = maxin[i] + 1
        else:
            so[i] = maxin[i]
        if nin[i] == 1:
            link[i] = inlink[i]              # continue existing link
        else:
            nlinks += 1                      # channel head or junction
            link[i] = nlinks
            link_order[nlinks] = so[i]
        j = ds[i]
        if j >= 0 and stream[j]:
            nin[j] += 1
            if so[i] > maxin[j]:
                maxin[j] = so[i]
                nmax[j] = 1
            elif so[i] == maxin[j]:
                nmax[j] += 1
            inlink[j] = link[i]

    # Catchment of each link: label inherited from downstream cell
    lab = np.zeros(n, dtype=np.int64)
    for k in range(order.size - 1, -1, -1):  # downstream -> upstream
        i = order[k]
        if stream[i]:
            lab[i] = link[i]
        elif ds[i] >= 0:
            lab[i] = lab[ds[i]]
    return acc, stream, so, lab, link_order[: nlinks + 1]


@njit
def order_n_basins(ds, order, stream, so, n_target):
    """Full drainage basins of Strahler order-N streams.

    The outlet of an order-N stream is its last order-N cell (the next cell
    downstream is higher order, or there is none). Each outlet gets an ID,
    and every cell upstream of it inherits that ID. Basins of the same order
    cannot nest, because everything downstream of an outlet is order > N.
    """
    n = ds.size
    lab = np.zeros(n, dtype=np.int64)
    nb = 0
    for k in range(order.size - 1, -1, -1):  # downstream -> upstream
        i = order[k]
        j = ds[i]
        if stream[i] and so[i] == n_target and (j < 0 or so[j] > n_target):
            nb += 1
            lab[i] = nb
        elif j >= 0:
            lab[i] = lab[j]
    return lab, nb


def main():
    wbt = whitebox.WhiteboxTools()
    wbt.set_working_dir(WORK_DIR)
    if not os.path.isfile(os.path.join(WORK_DIR, DEM)):
        raise FileNotFoundError(os.path.join(WORK_DIR, DEM))

    if wbt.breach_depressions_least_cost(dem=DEM, output="dem_breached.tif",
                                         dist=BREACH_DIST, fill=True) != 0:
        raise RuntimeError("breach_depressions_least_cost failed")
    if wbt.d8_pointer(dem="dem_breached.tif", output="d8_pntr.tif") != 0:
        raise RuntimeError("d8_pointer failed")

    with rasterio.open(os.path.join(WORK_DIR, "dem_breached.tif")) as src:
        dem = src.read(1, masked=True)
    with rasterio.open(os.path.join(WORK_DIR, "d8_pntr.tif")) as src:
        pntr = src.read(1).astype(np.int64)
        profile, transform, crs = src.profile, src.transform, src.crs
    nr, nc = pntr.shape
    valid = ~np.ma.getmaskarray(dem).ravel()

    ds = downstream_index(pntr, valid)
    order = topological_order(ds, valid)
    acc, stream, so, lab, link_order = network(ds, order, THRESHOLD)

    # Full basins of order-N streams
    basin, nb = order_n_basins(ds, order, stream, so, ORDER)
    lab2 = basin.reshape(nr, nc)

    # Exclude basins touching the DEM edge or nodata (possibly truncated,
    # so their order is unreliable)
    vmask = valid.reshape(nr, nc)
    edge = np.zeros((nr, nc), bool)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    pad = np.pad(~vmask, 1, constant_values=True)
    edge |= (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    bad = np.unique(lab2[edge & vmask])
    bad = bad[bad > 0]

    o1 = np.where((lab2 > 0) & ~np.isin(lab2, bad), lab2, 0).astype(np.int32)

    # QA rasters
    prof = profile.copy()
    prof.update(dtype="int32", nodata=0, count=1)
    with rasterio.open(os.path.join(WORK_DIR, "strahler_check.tif"), "w", **prof) as dst:
        dst.write(np.where(stream, so, 0).reshape(nr, nc).astype(np.int32), 1)
    with rasterio.open(os.path.join(WORK_DIR, f"order{ORDER}_basins.tif"), "w", **prof) as dst:
        dst.write(o1, 1)

    recs = [{"geometry": shape(g), "basin_id": int(v)}
            for g, v in shapes(o1, mask=o1 > 0, transform=transform)]
    gdf = gpd.GeoDataFrame(recs, geometry="geometry", crs=crs)
    gdf = gdf.dissolve(by="basin_id").reset_index()
    gdf["area_km2"] = gdf.geometry.area / 1e6
    gdf.to_file(os.path.join(WORK_DIR, OUT_SHP))
    print(f"{len(gdf)} order-{ORDER} basins written; "
          f"{nb} found, {len(bad)} edge-truncated basins excluded")


if __name__ == "__main__":
    main()