#!/usr/bin/env python3
"""
Generate GTFS files for Fukuoka subway system
"""
import csv
import os
from datetime import datetime, date
from station_coordinates import create_station_mapping
from excel_parser import FukuokaTimetableParser

class GTFSGenerator:
    def __init__(self, output_dir="gtfs_output"):
        self.output_dir = output_dir
        self.station_mapping = create_station_mapping()
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_all_files(self, kukohakozaki_file, nanakuma_file):
        """Generate all GTFS files"""
        
        print("Parsing Excel timetable data...")
        parser = FukuokaTimetableParser()
        timetable_data = parser.parse_excel_files(kukohakozaki_file, nanakuma_file)
        
        print("Generating GTFS files...")
        self.generate_agency()
        self.generate_routes()
        self.generate_stops()
        self.generate_calendar()
        self.generate_trips(timetable_data['trips'])
        self.generate_stop_times(timetable_data['stop_times'])
        
        print(f"GTFS files generated in {self.output_dir}/")
    
    def generate_agency(self):
        """Generate agency.txt"""
        filename = os.path.join(self.output_dir, "agency.txt")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang'])
            writer.writerow([
                'fukuoka_subway',
                '福岡市交通局',
                'https://subway.city.fukuoka.lg.jp/',
                'Asia/Tokyo',
                'ja'
            ])
        
        print("Generated agency.txt")
    
    def generate_routes(self):
        """Generate routes.txt"""
        filename = os.path.join(self.output_dir, "routes.txt")
        
        routes = [
            {
                'route_id': 'airport_line',
                'agency_id': 'fukuoka_subway',
                'route_short_name': '空港線',
                'route_long_name': '福岡市地下鉄空港線',
                'route_type': '1',
                'route_color': '0066CC',
                'route_text_color': 'FFFFFF'
            },
            {
                'route_id': 'hakozaki_line',
                'agency_id': 'fukuoka_subway',
                'route_short_name': '箱崎線',
                'route_long_name': '福岡市地下鉄箱崎線',
                'route_type': '1',
                'route_color': '009639',
                'route_text_color': 'FFFFFF'
            },
            {
                'route_id': 'airport_hakozaki_line',
                'agency_id': 'fukuoka_subway',
                'route_short_name': '空港箱崎線',
                'route_long_name': '福岡市地下鉄空港線・箱崎線直通',
                'route_type': '1',
                'route_color': '0066CC',
                'route_text_color': 'FFFFFF'
            },
            {
                'route_id': 'nanakuma_line',
                'agency_id': 'fukuoka_subway',
                'route_short_name': '七隈線',
                'route_long_name': '福岡市地下鉄七隈線',
                'route_type': '1',
                'route_color': 'FF6600',
                'route_text_color': 'FFFFFF'
            }
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'route_id', 'agency_id', 'route_short_name', 'route_long_name',
                'route_type', 'route_color', 'route_text_color'
            ])
            writer.writeheader()
            writer.writerows(routes)
        
        print("Generated routes.txt")
    
    def generate_stops(self):
        """Generate stops.txt"""
        filename = os.path.join(self.output_dir, "stops.txt")
        
        stops = []
        
        station_id_mapping = {
            '博多': 'hakata',
            '櫛田神社前': 'kushida_jinja_mae',
            '天神南': 'tenjin_minami',
            '渡辺通': 'watanabe_dori',
            '薬院': 'yakuin',
            '薬院大通': 'yakuin_odori',
            '桜坂': 'sakurazaka',
            '六本松': 'ropponmatsu',
            '別府': 'befu',
            '茶山': 'chayama',
            '金山': 'kanayama',
            '七隈': 'nanakuma',
            '福大前': 'fukudai_mae',
            '梅林': 'umebayashi',
            '野芥': 'noke',
            '賀茂': 'kamo',
            '次郎丸': 'jiromaru',
            '橋本': 'hashimoto',
            '姪浜': 'meinohama',
            '室見': 'muromi',
            '藤崎': 'fujisaki',
            '西新': 'nishijin',
            '唐人町': 'tojinmachi',
            '大濠公園': 'ohori_koen',
            '赤坂': 'akasaka',
            '天神': 'tenjin',
            '中洲川端': 'nakasu_kawabata',
            '祇園': 'gion',
            '貝塚': 'kaizuka',
            '箱崎宮前': 'hakozakigu_mae',
            '箱崎九大前': 'hakozaki_kyudai_mae',
            '馬出九大病院前': 'maidashi_kyudai_byoin_mae',
            '千代県庁口': 'chiyo_kencho_guchi',
            '呉服町': 'gofukumachi',
            '福岡空港': 'fukuoka_kuko',
            '東比恵': 'higashi_hie',
            '筑前前原': 'chikuzen_maebaru'
        }
        
        for station_name, stop_id in station_id_mapping.items():
            coords = self.station_mapping.get(station_name, {})
            
            stop = {
                'stop_id': stop_id,
                'stop_name': station_name,
                'stop_lat': f"{coords.get('lat', 33.5904):.4f}",
                'stop_lon': f"{coords.get('lon', 130.4017):.4f}",
                'location_type': '0',
                'parent_station': ''
            }
            stops.append(stop)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'location_type', 'parent_station'
            ])
            writer.writeheader()
            writer.writerows(stops)
        
        print(f"Generated stops.txt with {len(stops)} stops")
    
    def generate_calendar(self):
        """Generate calendar.txt"""
        filename = os.path.join(self.output_dir, "calendar.txt")
        
        start_date = "20250101"
        end_date = "20251231"
        
        services = [
            {
                'service_id': 'weekday',
                'monday': '1',
                'tuesday': '1',
                'wednesday': '1',
                'thursday': '1',
                'friday': '0',
                'saturday': '0',
                'sunday': '0',
                'start_date': start_date,
                'end_date': end_date
            },
            {
                'service_id': 'friday',
                'monday': '0',
                'tuesday': '0',
                'wednesday': '0',
                'thursday': '0',
                'friday': '1',
                'saturday': '0',
                'sunday': '0',
                'start_date': start_date,
                'end_date': end_date
            },
            {
                'service_id': 'weekend',
                'monday': '0',
                'tuesday': '0',
                'wednesday': '0',
                'thursday': '0',
                'friday': '0',
                'saturday': '1',
                'sunday': '1',
                'start_date': start_date,
                'end_date': end_date
            }
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'service_id', 'monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday', 'start_date', 'end_date'
            ])
            writer.writeheader()
            writer.writerows(services)
        
        print("Generated calendar.txt")
    
    def generate_trips(self, trips_data):
        """Generate trips.txt"""
        filename = os.path.join(self.output_dir, "trips.txt")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id'
            ])
            writer.writeheader()
            
            for trip in trips_data:
                writer.writerow({
                    'route_id': trip['route_id'],
                    'service_id': trip['service_id'],
                    'trip_id': trip['trip_id'],
                    'trip_headsign': trip['trip_headsign'],
                    'direction_id': trip['direction_id']
                })
        
        print(f"Generated trips.txt with {len(trips_data)} trips")
    
    def generate_stop_times(self, stop_times_data):
        """Generate stop_times.txt"""
        filename = os.path.join(self.output_dir, "stop_times.txt")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'
            ])
            writer.writeheader()
            
            for stop_time in stop_times_data:
                writer.writerow(stop_time)
        
        print(f"Generated stop_times.txt with {len(stop_times_data)} stop times")

if __name__ == "__main__":
    generator = GTFSGenerator()
    generator.generate_all_files("kukohakozaki_timetable.xlsx", "nanakuma_timetable.xlsx")
