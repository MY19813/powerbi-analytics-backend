from fastapi import APIRouter, HTTPException
from ..models.schemas import SummaryStats, HealthCheck
from ..services.data_service import data_service
from datetime import datetime

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])

@router.get("/summary", response_model=SummaryStats)
async def get_summary_stats():
    """Get summary statistics"""
    try:
        summary = data_service.get_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status-breakdown")
async def get_status_breakdown():
    """Get registration status breakdown"""
    try:
        breakdown = data_service.get_status_breakdown()
        return {"data": breakdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payment-status-breakdown")
async def get_payment_status_breakdown():
    """Get payment status breakdown"""
    try:
        breakdown = data_service.get_payment_status_breakdown()
        return {"data": breakdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/badge-categories")
async def get_badge_categories():
    """Get badge category breakdown"""
    try:
        breakdown = data_service.get_badge_category_breakdown()
        return {"data": breakdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/revenue")
async def get_revenue_metrics():
    """Get revenue metrics"""
    try:
        summary = data_service.get_summary()
        revenue_by_badge = data_service.get_revenue_by_badge()
        
        return {
            "total_egp": summary['total_revenue_egp'],
            "total_usd": summary['total_revenue_usd'],
            "by_badge": revenue_by_badge
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kpis")
async def get_key_performance_indicators():
    """Get key performance indicators"""
    try:
        summary = data_service.get_summary()
        df = data_service.get_full_data()
        
        # Calculate KPIs
        total_registrations = summary['total_records']
        completed = summary['status_breakdown'].get('Completed', 0)
        completion_rate = (completed / total_registrations * 100) if total_registrations > 0 else 0
        
        paid_count = summary['payment_status_breakdown'].get('Paid', 0)
        payment_rate = (paid_count / total_registrations * 100) if total_registrations > 0 else 0
        
        return {
            "total_registrations": total_registrations,
            "completion_rate": round(completion_rate, 2),
            "drop_off_rate": round(summary['drop_off_rate'], 2),
            "payment_rate": round(payment_rate, 2),
            "total_revenue_egp": summary['total_revenue_egp'],
            "total_revenue_usd": summary['total_revenue_usd'],
            "average_revenue_egp": round(summary['total_revenue_egp'] / paid_count, 2) if paid_count > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    try:
        summary = data_service.get_summary()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "data_records": summary['total_records']
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable")