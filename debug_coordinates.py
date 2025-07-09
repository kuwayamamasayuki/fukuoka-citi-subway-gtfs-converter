#!/usr/bin/env python3
"""
Debug coordinate issues in Fukuoka GTFS data
"""
import csv
import requests
import json
from station_coordinates import create_station_mapping

def check_coordinate_precision():
    """Check coordinate precision in station mappings vs CSV output"""
    print("=== Coordinate Precision Analysis ===")
    
    mapping = create_station_mapping()
    
    print("\nCoordinates from station_coordinates.py:")
    problem_stations = ['薬院大通', '別府', '七隈', '野芥', '橋本']
    for name in problem_stations:
        if name in mapping:
            coords = mapping[name]
            print(f"{name}: lat={coords['lat']}, lon={coords['lon']}")
    
    print("\nCoordinates from stops.txt:")
    with open('gtfs_output/stops.txt', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['stop_name'] in problem_stations:
                print(f"{row['stop_name']}: lat={row['stop_lat']}, lon={row['stop_lon']}")

def test_overpass_query():
    """Test improved Overpass API query for Fukuoka stations"""
    print("\n=== Testing Overpass API queries ===")
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    query = """
    [out:json][timeout:60];
    (
      node["railway"="station"](33.5,130.2,33.7,130.6);
      node["public_transport"="station"](33.5,130.2,33.7,130.6);
    );
    out geom;
    """
    
    try:
        response = requests.post(overpass_url, data=query, timeout=120)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            print(f"Total stations found in Fukuoka area: {len(elements)}")
            
            fukuoka_stations = []
            for elem in elements:
                if 'tags' in elem and 'name' in elem['tags']:
                    name = elem['tags']['name']
                    operator = elem['tags'].get('operator', '')
                    network = elem['tags'].get('network', '')
                    if '福岡' in operator or '福岡' in network or name in ['天神', '博多', '姪浜', '貝塚']:
                        fukuoka_stations.append(elem)
            
            print(f"Fukuoka subway stations found: {len(fukuoka_stations)}")
            for station in fukuoka_stations[:10]:
                name = station['tags']['name']
                lat = station.get('lat', 'N/A')
                lon = station.get('lon', 'N/A')
                operator = station['tags'].get('operator', 'N/A')
                print(f"  {name}: ({lat}, {lon}) - {operator}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_coordinate_precision()
    test_overpass_query()
