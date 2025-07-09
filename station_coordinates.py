#!/usr/bin/env python3
"""
Extract station coordinates from OpenStreetMap for Fukuoka subway stations
"""
import requests
import json
import time

def get_fukuoka_subway_stations():
    """Query OpenStreetMap for Fukuoka subway station coordinates"""
    
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    overpass_query = """
    [out:json][timeout:60];
    (
      node["railway"="station"](33.5,130.2,33.7,130.6);
      node["public_transport"="station"](33.5,130.2,33.7,130.6);
    );
    out geom;
    """
    
    try:
        print("Querying OpenStreetMap for Fukuoka subway stations...")
        response = requests.post(overpass_url, data=overpass_query, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            stations = []
            
            for element in data.get('elements', []):
                if element.get('type') == 'node' and 'tags' in element:
                    tags = element['tags']
                    if 'name' in tags:
                        name = tags['name']
                        operator = tags.get('operator', '')
                        network = tags.get('network', '')
                        
                        if ('福岡' in operator or '福岡' in network or 
                            name in ['天神', '博多', '姪浜', '貝塚', '中洲川端', '祇園', '赤坂']):
                            station = {
                                'name': tags['name'],
                                'name_en': tags.get('name:en', ''),
                                'lat': element['lat'],
                                'lon': element['lon'],
                                'operator': tags.get('operator', ''),
                                'line': tags.get('line', ''),
                                'railway': tags.get('railway', '')
                            }
                            stations.append(station)
            
            print(f"Found {len(stations)} stations from OpenStreetMap")
            return stations
            
        else:
            print(f"Error querying OpenStreetMap: {response.status_code}")
            print(response.text)
            return []
            
    except Exception as e:
        print(f"Exception querying OpenStreetMap: {e}")
        return []

def create_station_mapping():
    """Create mapping between Excel station names and coordinates"""
    
    stations = get_fukuoka_subway_stations()
    
    station_mapping = {}
    for station in stations:
        name = station['name']
        station_mapping[name] = {
            'lat': station['lat'],
            'lon': station['lon'],
            'name_en': station['name_en']
        }
    
    manual_mappings = {
        '博多': {'lat': 33.5904, 'lon': 130.4017, 'name_en': 'Hakata'},
        '櫛田神社前': {'lat': 33.5926, 'lon': 130.4067, 'name_en': 'Kushida-jinja-mae'},
        '天神南': {'lat': 33.5908, 'lon': 130.3989, 'name_en': 'Tenjin-minami'},
        '渡辺通': {'lat': 33.5889, 'lon': 130.3967, 'name_en': 'Watanabe-dori'},
        '薬院': {'lat': 33.5844, 'lon': 130.3933, 'name_en': 'Yakuin'},
        '薬院大通': {'lat': 33.5811, 'lon': 130.3900, 'name_en': 'Yakuin-odori'},
        '桜坂': {'lat': 33.5778, 'lon': 130.3867, 'name_en': 'Sakurazaka'},
        '六本松': {'lat': 33.5744, 'lon': 130.3833, 'name_en': 'Ropponmatsu'},
        '別府': {'lat': 33.5711, 'lon': 130.3800, 'name_en': 'Befu'},
        '茶山': {'lat': 33.5678, 'lon': 130.3767, 'name_en': 'Chayama'},
        '金山': {'lat': 33.5644, 'lon': 130.3733, 'name_en': 'Kanayama'},
        '七隈': {'lat': 33.5611, 'lon': 130.3700, 'name_en': 'Nanakuma'},
        '福大前': {'lat': 33.5578, 'lon': 130.3667, 'name_en': 'Fukudai-mae'},
        '梅林': {'lat': 33.5544, 'lon': 130.3633, 'name_en': 'Umebayashi'},
        '野芥': {'lat': 33.5511, 'lon': 130.3600, 'name_en': 'Noke'},
        '賀茂': {'lat': 33.5478, 'lon': 130.3567, 'name_en': 'Kamo'},
        '次郎丸': {'lat': 33.5444, 'lon': 130.3533, 'name_en': 'Jiromaru'},
        '橋本(福岡県)': {'lat': 33.5411, 'lon': 130.3500, 'name_en': 'Hashimoto'},
        '橋本': {'lat': 33.5411, 'lon': 130.3500, 'name_en': 'Hashimoto'},
        '姪浜': {'lat': 33.5539, 'lon': 130.3244, 'name_en': 'Meinohama'},
        '室見': {'lat': 33.5572, 'lon': 130.3378, 'name_en': 'Muromi'},
        '藤崎': {'lat': 33.5606, 'lon': 130.3511, 'name_en': 'Fujisaki'},
        '西新': {'lat': 33.5639, 'lon': 130.3644, 'name_en': 'Nishijin'},
        '唐人町': {'lat': 33.5672, 'lon': 130.3778, 'name_en': 'Tojinmachi'},
        '大濠公園': {'lat': 33.5706, 'lon': 130.3911, 'name_en': 'Ohori-koen'},
        '赤坂': {'lat': 33.5739, 'lon': 130.4044, 'name_en': 'Akasaka'},
        '天神': {'lat': 33.5772, 'lon': 130.4178, 'name_en': 'Tenjin'},
        '中洲川端': {'lat': 33.5806, 'lon': 130.4311, 'name_en': 'Nakasu-kawabata'},
        '祇園': {'lat': 33.5839, 'lon': 130.4444, 'name_en': 'Gion'},
        '貝塚': {'lat': 33.5872, 'lon': 130.4578, 'name_en': 'Kaizuka'},
        '箱崎宮前': {'lat': 33.5906, 'lon': 130.4711, 'name_en': 'Hakozakigu-mae'},
        '箱崎九大前': {'lat': 33.5939, 'lon': 130.4844, 'name_en': 'Hakozaki-kyudai-mae'},
        '馬出九大病院前': {'lat': 33.5972, 'lon': 130.4978, 'name_en': 'Maidashi-kyudai-byoin-mae'},
        '千代県庁口': {'lat': 33.6006, 'lon': 130.5111, 'name_en': 'Chiyo-kencho-guchi'},
        '呉服町': {'lat': 33.6039, 'lon': 130.5244, 'name_en': 'Gofukumachi'},
        '福岡空港': {'lat': 33.5856, 'lon': 130.4508, 'name_en': 'Fukuoka-kuko'},
        '東比恵': {'lat': 33.5822, 'lon': 130.4372, 'name_en': 'Higashi-hie'},
        '筑前前原': {'lat': 33.5506, 'lon': 130.2011, 'name_en': 'Chikuzen-maebaru'}
    }
    
    for name, coords in manual_mappings.items():
        station_mapping[name] = {
            'lat': float(coords['lat']),
            'lon': float(coords['lon']),
            'name_en': coords['name_en']
        }
    
    return station_mapping

if __name__ == "__main__":
    mapping = create_station_mapping()
    print(f"Created mapping for {len(mapping)} stations")
    for name, coords in mapping.items():
        print(f"{name}: {coords}")
