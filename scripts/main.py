from data_loader import DataLoader
from data_processor import DataProcessor
from pathlib import Path

def main():
    """Main execution script for Phase 1"""
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / 'data' / 'power-bi-export-2026-01-14T15-28-16-178Z.csv'
    output_dir = base_dir / 'outputs' / 'processed_data'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load data
    print("=" * 60)
    print("PHASE 1: DATA PIPELINE SETUP")
    print("=" * 60)
    
    loader = DataLoader(str(data_file))
    df = loader.load_excel()
    inspection_results = loader.inspect_data()
    
    # Step 2: Process data
    processor = DataProcessor(df)
    cleaned_df = processor.clean_data()
    
    # Step 3: Generate summary statistics
    summary = processor.generate_summary_stats()
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Total Records: {summary['total_records']}")
    print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Total Revenue (EGP): {summary['total_revenue_egp']:.2f}")
    print(f"Total Revenue (USD): {summary['total_revenue_usd']:.2f}")
    print(f"Drop-off Rate: {summary['drop_off_rate']:.2f}%")
    
    # Step 4: Export to JSON
    output_file = output_dir / 'processed_data.json'
    export_paths = processor.export_to_json(str(output_file))
    
    print("\n" + "=" * 60)
    print("PHASE 1 COMPLETE!")
    print("=" * 60)
    print(f"\nProcessed files saved to:")
    for key, path in export_paths.items():
        print(f"  {key}: {path}")

if __name__ == "__main__":
    main()