from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Response Models
class StatusBreakdown(BaseModel):
    """Status breakdown statistics"""
    Completed: int = 0
    Drop_Off: int = Field(0, alias="Drop Off")
    Rejected: int = 0
    Pending: int = 0
    More_Info: int = Field(0, alias="More Info")
    
    class Config:
        populate_by_name = True

class PaymentStatusBreakdown(BaseModel):
    """Payment status breakdown"""
    Paid: int = 0
    Unpaid: int = 0
    FOC: int = 0

class DateRange(BaseModel):
    """Date range for data"""
    start: Optional[str] = None
    end: Optional[str] = None

class SummaryStats(BaseModel):
    """Summary statistics response"""
    total_records: int
    date_range: DateRange
    status_breakdown: Dict[str, int]
    payment_status_breakdown: Dict[str, int]
    total_revenue_egp: float
    total_revenue_usd: float
    drop_off_rate: float

class RegistrationRecord(BaseModel):
    """Individual registration record"""
    urn: Optional[str] = None
    status: Optional[str] = None
    badgeCategory_name: Optional[str] = None
    created_at: Optional[str] = None
    paid_amount_egp: Optional[float] = 0.0
    paid_amount_usd: Optional[float] = 0.0
    payment_status: Optional[str] = None
    Country_of_Residence: Optional[str] = None
    Industry: Optional[str] = None
    Company_Type: Optional[str] = None
    source: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow additional fields

class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[Dict[str, Any]]

class ChartData(BaseModel):
    """Chart data response"""
    labels: List[str]
    values: List[float]
    chart_type: str

class TopNData(BaseModel):
    """Top N items response"""
    items: List[Dict[str, Any]]
    total_count: int

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    data_records: int

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    timestamp: str