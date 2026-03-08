from data_loader import DataLoader
from pathlib import Path

def test_data_loading():
    print("TEST: Data Loading")
    print("-" * 40)
    
    data_file = Path(__file__).parent.parent / 'data' / 'power-bi-export-2026-01-14T15-28-16-178Z.csv'
    
    try:
        loader = DataLoader(str(data_file))
        df = loader.load_excel()
        
        # Assertions
        assert df is not None, "DataFrame should not be None"
        assert len(df) > 0, "DataFrame should have rows"
        assert len(df.columns) > 0, "DataFrame should have columns"
        
        print(f"✓ Data loaded successfully")
        print(f"✓ Shape: {df.shape}")
        print(f"✓ Columns: {len(df.columns)}")
        
        return True
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_data_loading()