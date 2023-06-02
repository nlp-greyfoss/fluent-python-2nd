from geolib import geohash as gh  # type: ignore # 防止mypy说geolib没有类型提示

PRECISION = 9


def geohash(lat_lon: tuple[float, float]) -> str:  # 以两个float元素的元组注解lat_lon
    return gh.encode(*lat_lon, PRECISION)


"""
$ mypy coordinates.py 
Success: no issues found in 1 source file
"""
