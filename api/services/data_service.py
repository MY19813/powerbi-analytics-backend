import json
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
from ..config import settings

class DataService:
    """Service for data operations"""
    
    def __init__(self):
        self.summary_path = settings.DATA_DIR / "processed_data_summary.json"
        self.full_data_path = settings.DATA_DIR / "processed_data_full.json"
        self._summary_cache = None
        self._data_cache = None
        
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if self._summary_cache is None:
            with open(self.summary_path, 'r') as f:
                self._summary_cache = json.load(f)
        return self._summary_cache
    
    def get_full_data(self) -> pd.DataFrame:
        """Get full dataset as DataFrame"""
        if self._data_cache is None:
            with open(self.full_data_path, 'r') as f:
                data = json.load(f)
            self._data_cache = pd.DataFrame(data)
        return self._data_cache
    
    def get_paginated_data(
        self, 
        page: int = 1, 
        page_size: int = 50,
        status: Optional[str] = None,
        payment_status: Optional[str] = None,
        badge_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated and filtered data"""
        df = self.get_full_data().copy()
        
        # Apply filters
        if status:
            df = df[df['status'] == status]
        if payment_status:
            df = df[df['payment_status'] == payment_status]
        if badge_category:
            df = df[df['badgeCategory_name'] == badge_category]
        
        # Calculate pagination
        total = len(df)
        total_pages = (total + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Get page data
        page_data = pd.DataFrame(df).iloc[start_idx:end_idx].to_dict('records')
        
        return {
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'data': page_data
        }
    
    def get_status_breakdown(self) -> Dict[str, int]:
        """Get status distribution"""
        df = self.get_full_data()
        if 'status' in df.columns:
            return df['status'].value_counts().to_dict()
        return {}
    
    def get_payment_status_breakdown(self) -> Dict[str, int]:
        """Get payment status distribution"""
        df = self.get_full_data()
        if 'payment_status' in df.columns:
            return df['payment_status'].value_counts().to_dict()
        return {}
    
    def get_badge_category_breakdown(self) -> Dict[str, int]:
        """Get badge category distribution"""
        df = self.get_full_data()
        if 'badgeCategory_name' in df.columns:
            return df['badgeCategory_name'].value_counts().to_dict()
        return {}
    
    def get_top_countries(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N countries"""
        df = self.get_full_data()
        if 'Country_of_Residence' in df.columns:
            counts = df['Country_of_Residence'].value_counts().head(n)
            return [{'country': k, 'count': int(v)} for k, v in counts.items()]
        return []
    
    def get_top_industries(self, n: int = 15) -> List[Dict[str, Any]]:
        """Get top N industries"""
        df = self.get_full_data()
        if 'Industry' in df.columns:
            counts = df['Industry'].value_counts().head(n)
            return [{'industry': k, 'count': int(v)} for k, v in counts.items()]
        return []
    
    def get_revenue_by_badge(self) -> List[Dict[str, Any]]:
        """Get revenue breakdown by badge category"""
        df = self.get_full_data()
        if 'badgeCategory_name' in df.columns and 'paid_amount_egp' in df.columns:
            revenue = df.groupby('badgeCategory_name')['paid_amount_egp'].agg(['sum', 'count']).reset_index()
            revenue.columns = ['badge', 'total_revenue', 'count']
            return revenue.to_dict('records')
        return []
    
    def get_registration_trends(self, groupby: str = 'day') -> List[Dict[str, Any]]:
        """Get registration trends over time"""
        df = self.get_full_data()
        if 'created_at' not in df.columns:
            return []
        
        # Convert to datetime
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        df = df.dropna(subset=['created_at'])
        
        if len(df) == 0:
            return []
        
        # Group by time period
        if groupby == 'day':
            df['period'] = df['created_at'].dt.date
        elif groupby == 'week':
            df['period'] = df['created_at'].dt.to_period('W').astype(str)
        elif groupby == 'month':
            df['period'] = df['created_at'].dt.to_period('M').astype(str)
        else:
            df['period'] = df['created_at'].dt.date
        
        trends = df.groupby('period').size().to_frame(name='count').reset_index()
        trends['period'] = trends['period'].astype(str)
        return trends.to_dict('records')
    
    def search_registrations(self, query: str, fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search registrations by text query"""
        df = self.get_full_data()
        
        if fields is None:
            fields = ['urn', 'First_Name', 'Last_Name', 'Email', 'Company_Name', 'Job_Title']
        
        # Filter to existing columns
        fields = [f for f in fields if f in df.columns]
        
        if not fields:
            return []
        
        # Search across fields
        mask = pd.Series([False] * len(df))
        for field in fields:
            mask |= df[field].astype(str).str.contains(query, case=False, na=False)
        
        results = df[mask].head(100)  # Limit to 100 results
        return pd.DataFrame(results).to_dict('records')

# Create singleton instance
data_service = DataService()