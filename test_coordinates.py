#!/usr/bin/env python3
"""
Test coordinate accuracy for Fukuoka subway stations
"""
from station_coordinates import create_station_mapping

def test_coordinate_accuracy():
    """Test that coordinates are accurate and properly formatted"""
    mapping = create_station_mapping()
    
    print("Testing coordinate accuracy and precision:")
    
    key_stations = {
        '博多': (33.5904, 130.4017),
        '天神': (33.5772, 130.4178),
        '薬院大通': (33.5811, 130.3900),
        '別府': (33.5711, 130.3800),
        '七隈': (33.5611, 130.3700),
        '野芥': (33.5511, 130.3600),
        '橋本': (33.5411, 130.3500),
        '姪浜': (33.5539, 130.3244),
        '福岡空港': (33.5856, 130.4508)
    }
    
    for station_name, expected_coords in key_stations.items():
        if station_name in mapping:
            actual = mapping[station_name]
            lat_diff = abs(actual['lat'] - expected_coords[0])
            lon_diff = abs(actual['lon'] - expected_coords[1])
            
            print(f"{station_name}:")
            print(f"  Expected: {expected_coords[0]:.4f}, {expected_coords[1]:.4f}")
            print(f"  Actual:   {actual['lat']:.4f}, {actual['lon']:.4f}")
            print(f"  Diff:     {lat_diff:.6f}, {lon_diff:.6f}")
            
            if lat_diff > 0.001 or lon_diff > 0.001:
                print(f"  WARNING: Large coordinate difference!")
            print()

if __name__ == "__main__":
    test_coordinate_accuracy()
