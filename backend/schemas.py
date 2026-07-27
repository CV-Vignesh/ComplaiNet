from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ComplaintBase(BaseModel):
    complaintSource: Optional[str] = None
    customerName: Optional[str] = None
    productName: Optional[str] = None
    productStrengthGrade: Optional[str] = None
    batchLotNumber: Optional[str] = None
    manufacturingDate: Optional[str] = None
    expiryDate: Optional[str] = None
    quantityAffected: Optional[str] = None
    complaintType: Optional[str] = None
    complaintDate: Optional[str] = None
    detailedComplaintDescription: Optional[str] = None
    initialSeverity: Optional[str] = None
    priority: Optional[str] = None
    aiRiskAssessmentReasoning: Optional[str] = None
    capaRequired: Optional[str] = None
    suggestedRootCause: Optional[str] = None
    regulatoryReportability: Optional[str] = None
    investigationStatus: Optional[str] = "Pending Triage"

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(ComplaintBase):
    pass

class ComplaintResponse(ComplaintBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    model_config = ConfigDict(from_attributes=True)
