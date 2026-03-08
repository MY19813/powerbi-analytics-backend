import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataProcessor:
    """Clean and transform Power BI data"""
    
    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.processed_df = None
        
    def clean_data(self):
        """Apply all cleaning operations"""
        print("\n=== STARTING DATA CLEANING ===")
        
        # 1. Clean datetime columns
        self._clean_datetime_columns()
        
        # 2. Handle missing values
        self._handle_missing_values()
        
        # 3. Remove duplicates
        self._remove_duplicates()
        
        # 4. Clean string columns
        self._clean_string_columns()
        
        # 5. Convert boolean columns
        self._convert_boolean_columns()
        
        # 6. Clean numeric columns
        self._clean_numeric_columns()
        
        self.processed_df = self.df
        print("\n=== DATA CLEANING COMPLETE ===")
        return self.processed_df
    
    def _clean_datetime_columns(self):
        """Clean and convert datetime columns"""
        datetime_cols = ['created_at', 'updated_at']
        
        for col in datetime_cols:
            if col in self.df.columns:
                print(f"Cleaning datetime column: {col}")
                # Remove extra quotes if present
                self.df[col] = self.df[col].astype(str).str.replace('"""', '')
                # Convert to datetime
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
    
    def _handle_missing_values(self):
        """Handle missing values appropriately"""
        print("Handling missing values...")
        
        # For numeric columns, you might fill with 0 or median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().any():
                self.df[col].fillna(0, inplace=True)
        
        # For categorical columns, fill with 'Unknown' or most frequent
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.df[col].isnull().any():
                self.df[col].fillna('Unknown', inplace=True)
    
    def _remove_duplicates(self):
        """Remove duplicate rows"""
        initial_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed = initial_count - len(self.df)
        print(f"Removed {removed} duplicate rows")
    
    def _clean_string_columns(self):
        """Clean string columns (trim whitespace, etc.)"""
        print("Cleaning string columns...")
        string_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in string_cols:
            # Strip whitespace
            self.df[col] = self.df[col].astype(str).str.strip()
    
    def _convert_boolean_columns(self):
        """Convert boolean-like columns"""
        boolean_cols = ['isDropOff', 'Is_this_your_first_time_attending_Ai_Everything', 
                       'Visa_invitation_Letter']
        
        for col in boolean_cols:
            if col in self.df.columns:
                print(f"Converting boolean column: {col}")
                self.df[col] = self.df[col].map({
                    'TRUE': True, 'True': True, 'true': True, True: True,
                    'FALSE': False, 'False': False, 'false': False, False: False
                })
    
    def _clean_numeric_columns(self):
        """Clean numeric columns"""
        numeric_cols = ['paid_amount_egp', 'paid_amount_usd']
        
        for col in numeric_cols:
            if col in self.df.columns:
                # Ensure numeric type
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                self.df[col] = self.df[col].fillna(0)
    
    def generate_summary_stats(self):
        """Generate summary statistics"""
        if self.processed_df is None:
            raise ValueError("No processed data. Call clean_data() first.")
        
        stats = {
            'total_records': len(self.processed_df),
            'date_range': {
                'start': self.processed_df['created_at'].min().isoformat() if 'created_at' in self.processed_df else None,
                'end': self.processed_df['created_at'].max().isoformat() if 'created_at' in self.processed_df else None
            },
            'status_breakdown': self.processed_df['status'].value_counts().to_dict() if 'status' in self.processed_df else {},
            'payment_status_breakdown': self.processed_df['payment_status'].value_counts().to_dict() if 'payment_status' in self.processed_df else {},
            'total_revenue_egp': float(self.processed_df['paid_amount_egp'].sum()) if 'paid_amount_egp' in self.processed_df else 0,
            'total_revenue_usd': float(self.processed_df['paid_amount_usd'].sum()) if 'paid_amount_usd' in self.processed_df else 0,
            'drop_off_rate': float((self.processed_df['isDropOff'].sum() / len(self.processed_df)) * 100) if 'isDropOff' in self.processed_df else 0
        }
        
        return stats
    
    def export_to_json(self, output_path):
        """Export processed data to JSON"""
        if self.processed_df is None:
            raise ValueError("No processed data. Call clean_data() first.")
        
        print(f"\nExporting data to: {output_path}")
        
        # Convert DataFrame to JSON-serializable format
        # Handle datetime columns
        df_export = self.processed_df.copy()
        for col in df_export.select_dtypes(include=['datetime64']).columns:
            df_export[col] = df_export[col].astype(str)
        
        # Export full data
        full_data_path = output_path.replace('.json', '_full.json')
        df_export.to_json(full_data_path, orient='records', indent=2)
        print(f"Full data exported to: {full_data_path}")
        
        # Export summary stats
        summary = self.generate_summary_stats()
        summary_path = output_path.replace('.json', '_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary stats exported to: {summary_path}")
        
        return {
            'full_data': full_data_path,
            'summary': summary_path
        }