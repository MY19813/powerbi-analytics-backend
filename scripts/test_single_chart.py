from visualization import DataVisualizer
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

def test_single_chart():
    """Test generating a single chart"""
    print("TEST: Single Chart Generation")
    print("-" * 40)
    
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / 'outputs' / 'processed_data' / 'processed_data_full.json'
    output_dir = base_dir / 'outputs' / 'charts' / 'test'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        visualizer = DataVisualizer(str(data_file), str(output_dir))
        
        # Test one chart
        visualizer.plot_status_distribution()
        
        # Check if file was created
        chart_file = output_dir / 'status_distribution.png'
        assert chart_file.exists(), "Chart file should exist"
        assert chart_file.stat().st_size > 0, "Chart file should not be empty"
        
        print(f"✓ Chart generated successfully")
        print(f"✓ File size: {chart_file.stat().st_size} bytes")
        print(f"✓ Location: {chart_file}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_single_chart()