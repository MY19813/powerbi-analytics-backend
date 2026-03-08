import pandas as pd
import os
from pathlib import Path

class DataLoader:
    """Load and inspect Power BI export data"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        
    def load_excel(self):
        """Load Excel file and return DataFrame"""
        print(f"Loading data from: {self.file_path}")
        
        # Determine file type and load accordingly
        if self.file_path.endswith('.xlsx'):
            self.data = pd.read_excel(self.file_path, engine='openpyxl')
        elif self.file_path.endswith('.csv'):
            self.data = pd.read_csv(self.file_path)
        else:
            raise ValueError("Unsupported file format. Use .xlsx or .csv")
        
        print(f"Data loaded successfully: {self.data.shape[0]} rows, {self.data.shape[1]} columns")
        return self.data
    
    def inspect_data(self):
        """Print basic information about the dataset"""
        if self.data is None:
            raise ValueError("No data loaded. Call load_excel() first.")
        
        print("\n=== DATA INSPECTION ===")
        print(f"\nShape: {self.data.shape}")
        print(f"\nColumns ({len(self.data.columns)}):")
        for col in self.data.columns:
            print(f"  - {col}")
        
        print("\n--- Data Types ---")
        print(self.data.dtypes)
        
        print("\n--- Missing Values ---")
        missing = self.data.isnull().sum()
        print(missing[missing > 0])
        
        print("\n--- First 5 Rows ---")
        print(self.data.head())
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict()
        }