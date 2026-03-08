from visualization import DataVisualizer
from pathlib import Path

def main():
    """Run Phase 2: Generate all visualizations"""
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / 'outputs' / 'processed_data' / 'processed_data_full.json'
    output_dir = base_dir / 'outputs' / 'charts'
    
    # Check if data file exists
    if not data_file.exists():
        print(f"❌ Error: Data file not found at {data_file}")
        print("Please run Phase 1 first (main.py)")
        return
    
    print("Starting visualization generation...")
    print(f"Data source: {data_file}")
    print(f"Output directory: {output_dir}\n")
    
    # Create visualizer and generate charts
    visualizer = DataVisualizer(str(data_file), str(output_dir))
    charts = visualizer.generate_all_charts()
    
    print(f"\n✓ Successfully generated {len(charts)} visualizations!")
    print(f"✓ Charts saved to: {output_dir}")
    
    # List all generated files
    print("\nGenerated files:")
    for chart in charts:
        print(f"  - {chart}")

if __name__ == "__main__":
    main()