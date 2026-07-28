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
    
    # 7. BONUS FEATURES
    complaintSummary = Column(String, nullable=True)
    completenessScore = Column(String, nullable=True)
    missingInformation = Column(String, nullable=True)
    
    # 8. ADVANCED AI BONUS FEATURES
    immediateActionPlan = Column(String, nullable=True)
    customerSentiment = Column(String, nullable=True)
    escalationRisk = Column(String, nullable=True)  # Using String/Boolean mapped in DB, but SQLAlchemy Boolean is better. Let's use String for flexibility with sqlite/postgres mix, wait SQLAlchemy Boolean is fine, but string 'true'/'false' is safer for now. Actually, let's use String for simple migration. No, wait, schema is bool. Let's use String and cast it if needed, or just import Boolean. Wait, let's just use String for all to be extremely safe without schema mismatch, except SQLAlchemy handles Boolean.
    
    # Let's import Boolean at the top and use Boolean. Wait, I'll just use String for all to avoid postgres conversion issues during my raw alter table, wait, I'll use String.
    # ACTUALLY, I'll use String for all to be safe.
    
    # Wait, let's just use String for everything except escalationRisk which is boolean in schema. I'll make escalationRisk a String in SQLAlchemy and cast it in Pydantic. Wait, if schema is bool, Pydantic converts. Let's just make it String in SQLAlchemy. Or import Boolean.
    
    immediateActionPlan = Column(String, nullable=True)
    customerSentiment = Column(String, nullable=True)
    escalationRisk = Column(String, nullable=True) # Will store "True" or "False"
    regulatoryFramework = Column(String, nullable=True)
    
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updatedAt = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
