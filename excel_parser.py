#!/usr/bin/env python3
"""
Parse Excel timetable data for Fukuoka subway
"""
import pandas as pd
import re
from datetime import datetime, time

class FukuokaTimetableParser:
    def __init__(self):
        self.station_mapping = {}
        self.routes = {}
        self.trips = []
        self.stop_times = []
        
    def parse_excel_files(self, kukohakozaki_file, nanakuma_file):
        """Parse both Excel files and extract timetable data"""
        
        print("Parsing Kuko-Hakozaki line timetable...")
        self._parse_kuko_hakozaki(kukohakozaki_file)
        
        print("Parsing Nanakuma line timetable...")
        self._parse_nanakuma(nanakuma_file)
        
        return {
            'routes': self.routes,
            'trips': self.trips,
            'stop_times': self.stop_times
        }
    
    def _parse_kuko_hakozaki(self, filename):
        """Parse Kuko-Hakozaki line Excel file"""
        
        wb = pd.ExcelFile(filename)
        
        for sheet_name in wb.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            
            service_type = self._extract_service_type(sheet_name)
            direction = self._extract_direction(sheet_name)
            
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            if direction == "姪浜方面":
                route_id = "airport_line"
                self._process_sheet_data(df, route_id, service_type, direction)
            elif direction == "空港貝塚方面":
                route_id = "airport_hakozaki_line"
                self._process_sheet_data(df, route_id, service_type, direction)
    
    def _parse_nanakuma(self, filename):
        """Parse Nanakuma line Excel file"""
        
        wb = pd.ExcelFile(filename)
        
        for sheet_name in wb.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            
            service_type = self._extract_service_type(sheet_name)
            direction = self._extract_direction(sheet_name)
            
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            route_id = "nanakuma_line"
            self._process_sheet_data(df, route_id, service_type, direction)
    
    def _extract_service_type(self, sheet_name):
        """Extract service type from sheet name"""
        if "平日" in sheet_name:
            return "weekday"
        elif "金曜" in sheet_name:
            return "friday"
        elif "土休" in sheet_name:
            return "weekend"
        return "weekday"
    
    def _extract_direction(self, sheet_name):
        """Extract direction from sheet name"""
        if "姪浜方面" in sheet_name:
            return "姪浜方面"
        elif "空港貝塚方面" in sheet_name:
            return "空港貝塚方面"
        elif "橋本方面" in sheet_name:
            return "橋本方面"
        elif "博多方面" in sheet_name:
            return "博多方面"
        return "unknown"
    
    def _process_sheet_data(self, df, route_id, service_type, direction):
        """Process individual sheet data"""
        
        if df.empty or len(df) < 3:
            return
        
        destination_row = df.iloc[0]
        through_service_row = df.iloc[1] if len(df) > 1 else None
        
        station_names = []
        for idx, row in df.iterrows():
            if idx >= 2:
                station_name = row.iloc[0]
                if pd.notna(station_name) and station_name != "始発":
                    if not (str(station_name).startswith('(') and str(station_name).endswith(')')):
                        station_names.append(station_name)
        
        for col_idx in range(2, len(df.columns)):
            if col_idx >= len(destination_row):
                continue
                
            destination = destination_row.iloc[col_idx]
            if pd.isna(destination):
                continue
            
            through_service = ""
            if through_service_row is not None and col_idx < len(through_service_row):
                through_service = str(through_service_row.iloc[col_idx]) if pd.notna(through_service_row.iloc[col_idx]) else ""
            
            trip_id = f"{route_id}_{service_type}_{direction}_{col_idx}"
            
            trip = {
                'trip_id': trip_id,
                'route_id': route_id,
                'service_id': service_type,
                'trip_headsign': destination,
                'direction_id': 0 if "方面" in direction else 1,
                'through_service': through_service
            }
            self.trips.append(trip)
            
            stop_sequence = 1
            for station_idx, station_name in enumerate(station_names):
                row_idx = station_idx + 2
                if row_idx < len(df):
                    time_cell = df.iloc[row_idx, col_idx]
                    if pd.notna(time_cell) and str(time_cell) != "nan":
                        time_str = str(time_cell)
                        
                        if self._is_valid_time(time_str):
                            stop_time = {
                                'trip_id': trip_id,
                                'arrival_time': time_str,
                                'departure_time': time_str,
                                'stop_id': self._normalize_station_name(station_name),
                                'stop_sequence': stop_sequence
                            }
                            self.stop_times.append(stop_time)
                            stop_sequence += 1
    
    def _is_valid_time(self, time_str):
        """Check if time string is valid"""
        if not time_str or time_str == "nan":
            return False
        
        time_pattern = r'^\d{1,2}:\d{2}:\d{2}$'
        return bool(re.match(time_pattern, str(time_str)))
    
    def _normalize_station_name(self, station_name):
        """Normalize station name for stop_id"""
        if not station_name:
            return ""
        
        station_name = str(station_name).strip()
        
        if station_name.endswith("(福岡県)"):
            station_name = station_name.replace("(福岡県)", "")
        
        if station_name == "橋本":
            return "hashimoto"
        
        name_mapping = {
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
        
        return name_mapping.get(station_name, station_name.lower().replace(' ', '_'))

if __name__ == "__main__":
    parser = FukuokaTimetableParser()
    data = parser.parse_excel_files("kukohakozaki_timetable.xlsx", "nanakuma_timetable.xlsx")
    
    print(f"Parsed {len(data['trips'])} trips")
    print(f"Parsed {len(data['stop_times'])} stop times")
