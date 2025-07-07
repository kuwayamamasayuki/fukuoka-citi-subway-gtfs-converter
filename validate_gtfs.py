#!/usr/bin/env python3
"""
Validate generated GTFS files
"""
import os
import csv
import sys

def validate_gtfs_files(gtfs_dir):
    """Validate GTFS files for basic compliance"""
    
    required_files = ['agency.txt', 'routes.txt', 'stops.txt', 'calendar.txt', 'trips.txt', 'stop_times.txt']
    
    print(f"Validating GTFS files in {gtfs_dir}...")
    
    for filename in required_files:
        filepath = os.path.join(gtfs_dir, filename)
        if not os.path.exists(filepath):
            print(f"ERROR: Required file missing: {filename}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                row_count = sum(1 for row in reader)
                print(f"✓ {filename}: {row_count} rows")
        except Exception as e:
            print(f"ERROR reading {filename}: {e}")
            return False
    
    print("Basic GTFS validation completed successfully!")
    return True

def check_data_consistency(gtfs_dir):
    """Check data consistency across GTFS files"""
    
    print("\nChecking data consistency...")
    
    try:
        trips = {}
        with open(os.path.join(gtfs_dir, 'trips.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trips[row['trip_id']] = row
        
        stops = {}
        with open(os.path.join(gtfs_dir, 'stops.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stops[row['stop_id']] = row
        
        routes = {}
        with open(os.path.join(gtfs_dir, 'routes.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                routes[row['route_id']] = row
        
        stop_times_count = 0
        orphaned_trips = set()
        orphaned_stops = set()
        
        with open(os.path.join(gtfs_dir, 'stop_times.txt'), 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stop_times_count += 1
                
                if row['trip_id'] not in trips:
                    orphaned_trips.add(row['trip_id'])
                
                if row['stop_id'] not in stops:
                    orphaned_stops.add(row['stop_id'])
        
        print(f"✓ Found {len(trips)} trips")
        print(f"✓ Found {len(stops)} stops")
        print(f"✓ Found {len(routes)} routes")
        print(f"✓ Found {stop_times_count} stop times")
        
        if orphaned_trips:
            print(f"WARNING: {len(orphaned_trips)} orphaned trip references in stop_times.txt")
        
        if orphaned_stops:
            print(f"WARNING: {len(orphaned_stops)} orphaned stop references in stop_times.txt")
        
        if not orphaned_trips and not orphaned_stops:
            print("✓ Data consistency check passed!")
        
        return len(orphaned_trips) == 0 and len(orphaned_stops) == 0
        
    except Exception as e:
        print(f"ERROR during consistency check: {e}")
        return False

if __name__ == "__main__":
    gtfs_dir = sys.argv[1] if len(sys.argv) > 1 else "gtfs_output"
    
    if not os.path.exists(gtfs_dir):
        print(f"Error: GTFS directory not found: {gtfs_dir}")
        sys.exit(1)
    
    valid = validate_gtfs_files(gtfs_dir)
    consistent = check_data_consistency(gtfs_dir)
    
    if valid and consistent:
        print("\n✓ GTFS validation completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ GTFS validation failed!")
        sys.exit(1)
