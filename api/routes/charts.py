from fastapi import APIRouter, HTTPException, Query
from ..services.data_service import data_service
from typing import Optional

router = APIRouter(prefix="/api/charts", tags=["Charts"])

@router.get("/top-countries")
async def get_top_countries(n: int = Query(10, ge=1, le=50)):
    """Get top N countries for chart"""
    try:
        data = data_service.get_top_countries(n)
        
        labels = [item['country'] for item in data]
        values = [item['count'] for item in data]
        
        return {
            "chart_type": "bar",
            "labels": labels,
            "values": values,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-industries")
async def get_top_industries(n: int = Query(15, ge=1, le=50)):
    """Get top N industries for chart"""
    try:
        data = data_service.get_top_industries(n)
        
        labels = [item['industry'] for item in data]
        values = [item['count'] for item in data]
        
        return {
            "chart_type": "horizontalBar",
            "labels": labels,
            "values": values,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/registration-trends")
async def get_registration_trends(groupby: str = Query("day", regex="^(day|week|month)$")):
    """Get registration trends over time"""
    try:
        data = data_service.get_registration_trends(groupby)
        
        labels = [item['period'] for item in data]
        values = [item['count'] for item in data]
        
        return {
            "chart_type": "line",
            "labels": labels,
            "values": values,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/revenue-by-badge")
async def get_revenue_by_badge():
    """Get revenue breakdown by badge category"""
    try:
        data = data_service.get_revenue_by_badge()
        
        labels = [item['badge'] for item in data]
        values = [item['total_revenue'] for item in data]
        
        return {
            "chart_type": "bar",
            "labels": labels,
            "values": values,
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))