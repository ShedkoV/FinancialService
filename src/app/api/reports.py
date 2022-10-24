"""Api urls and views for reports operations"""
from fastapi import (
    Depends,
    BackgroundTasks,
    APIRouter,
    File,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from ..models.auth import User
from ..services.auth import get_current_user
from ..services.reports import ReportsService


router = APIRouter(
    prefix='/reports',
    tags=['Report'],
)


@router.post('/import')
def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    report_service: ReportsService = Depends(),
):
    """import file with operations"""
    background_tasks.add_task(
        report_service.import_csv,
        user.id,
        file.file
    )


@router.get('/export')
def export_csv(
    user: User = Depends(get_current_user),
    report_service: ReportsService = Depends(),
):
    """export file with operations"""
    report = report_service.export_csv(user_id=user.id)
    
    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=report.csv'},
    ) 
