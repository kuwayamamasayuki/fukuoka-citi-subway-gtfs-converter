#!/usr/bin/env python3
"""
Main script to convert Fukuoka subway timetables to GTFS format
"""
import argparse
import os
import sys
from gtfs_generator import GTFSGenerator

def main():
    parser = argparse.ArgumentParser(description='Convert Fukuoka subway timetables to GTFS format')
    parser.add_argument('--kuko-hakozaki', 
                       default='kukohakozaki_timetable.xlsx',
                       help='Path to Kuko-Hakozaki line Excel file')
    parser.add_argument('--nanakuma',
                       default='nanakuma_timetable.xlsx', 
                       help='Path to Nanakuma line Excel file')
    parser.add_argument('--output-dir',
                       default='gtfs_output',
                       help='Output directory for GTFS files')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.kuko_hakozaki):
        print(f"Error: Kuko-Hakozaki file not found: {args.kuko_hakozaki}")
        sys.exit(1)
    
    if not os.path.exists(args.nanakuma):
        print(f"Error: Nanakuma file not found: {args.nanakuma}")
        sys.exit(1)
    
    print("Starting Fukuoka subway GTFS conversion...")
    print(f"Kuko-Hakozaki file: {args.kuko_hakozaki}")
    print(f"Nanakuma file: {args.nanakuma}")
    print(f"Output directory: {args.output_dir}")
    
    try:
        generator = GTFSGenerator(args.output_dir)
        generator.generate_all_files(args.kuko_hakozaki, args.nanakuma)
        
        print("\nGTFS conversion completed successfully!")
        print(f"Generated files in {args.output_dir}/:")
        
        for filename in ['agency.txt', 'routes.txt', 'stops.txt', 'calendar.txt', 'trips.txt', 'stop_times.txt']:
            filepath = os.path.join(args.output_dir, filename)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  {filename}: {size} bytes")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
