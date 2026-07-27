from sqlalchemy import Column, String, Float, DateTime
import uuid
from database import Base
from datetime import datetime, timezone

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # 1. ORIGIN & CUSTOMER DETAILS
    complaintSource = Column(String, nullable=True)
    customerName = Column(String, nullable=True)
    
    # 2. PRODUCT & BATCH IDENTIFICATION
    productName = Column(String, nullable=True)
    productStrengthGrade = Column(String, nullable=True)
    batchLotNumber = Column(String, nullable=True)
    manufacturingDate = Column(String, nullable=True) # Using String for flexibility initially
    expiryDate = Column(String, nullable=True)
    quantityAffected = Column(String, nullable=True) 
    
    # 3. COMPLAINT DETAILS
    complaintType = Column(String, nullable=True)
    complaintDate = Column(String, nullable=True)
    detailedComplaintDescription = Column(String, nullable=True)
    
    # 4. INITIAL ASSESSMENT & PRIORITY
    initialSeverity = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    
    # 5. AI COPILOT RISK ASSESSMENT
    aiRiskAssessmentReasoning = Column(String, nullable=True)
    
    # 6. QMS / ICH Q10 ALIGNMENT
    capaRequired = Column(String, nullable=True)
    suggestedRootCause = Column(String, nullable=True)
    regulatoryReportability = Column(String, nullable=True)
    investigationStatus = Column(String, nullable=True, default="Pending Triage")
    
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
