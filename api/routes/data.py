from fastapi import APIRouter, HTTPException, Query
from ..models.schemas import PaginatedResponse
from ..services.data_service import data_service
from typing import Optional

router = APIRouter(prefix="/api/data", tags=["Data"])

@router.get("/registrations", response_model=PaginatedResponse)
async def get_registrations(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    payment_status: Optional[str] = None,
    badge_category: Optional[str] = None
):
    """Get paginated registration data with optional filters"""
    try:
        result = data_service.get_paginated_data(
            page=page,
            page_size=page_size,
            status=status,
            payment_status=payment_status,
            badge_category=badge_category
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_registrations(q: str = Query(..., min_length=2)):
    """Search registrations by query string"""
    try:
        results = data_service.search_registrations(q)
        return {
            "query": q,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filters")
async def get_available_filters():
    """Get available filter options"""
    try:
        df = data_service.get_full_data()
        
        filters = {}
        
        if 'status' in df.columns:
            filters['status'] = sorted(df['status'].dropna().unique().tolist())
        
        if 'payment_status' in df.columns:
            filters['payment_status'] = sorted(df['payment_status'].dropna().unique().tolist())
        
        if 'badgeCategory_name' in df.columns:
            filters['badge_category'] = sorted(df['badgeCategory_name'].dropna().unique().tolist())
        
        if 'Country_of_Residence' in df.columns:
            filters['countries'] = sorted(df['Country_of_Residence'].dropna().unique().tolist())
        
        return filters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))