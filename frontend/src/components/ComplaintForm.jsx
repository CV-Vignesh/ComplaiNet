import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateComplaintField } from '../store/complaintSlice';
import { ShieldCheck } from 'lucide-react';

const ComplaintForm = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.complaint.data);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateComplaintField({ field: name, value }));
  };

  return (
    <form className="form-grid" onSubmit={(e) => e.preventDefault()}>
      
      <div className="form-group">
        <label className="form-label">Customer / Source Name</label>
        <input 
          type="text" name="customerName" className="form-input"
          value={formData.customerName || ''} onChange={handleChange} 
          placeholder="e.g. Apollo Pharmacy"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Complaint Source</label>
        <select name="complaintSource" className="form-select" value={formData.complaintSource || ''} onChange={handleChange}>
          <option value="">Select Source</option>
          <option value="Direct Customer">Direct Customer</option>
          <option value="Hospital/Clinic">Hospital/Clinic</option>
          <option value="Pharmacy">Pharmacy</option>
          <option value="Distributor">Distributor</option>
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Product Name</label>
        <input 
          type="text" name="productName" className="form-input"
          value={formData.productName || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Strength / Grade</label>
        <input 
          type="text" name="productStrengthGrade" className="form-input"
          value={formData.productStrengthGrade || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Batch / Lot Number</label>
        <input 
          type="text" name="batchLotNumber" className="form-input"
          value={formData.batchLotNumber || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Manufacturing Date</label>
        <input 
          type="date" name="manufacturingDate" className="form-input"
          value={formData.manufacturingDate || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Expiry Date</label>
        <input 
          type="date" name="expiryDate" className="form-input"
          value={formData.expiryDate || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Quantity Affected</label>
        <input 
          type="text" name="quantityAffected" className="form-input"
          value={formData.quantityAffected || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group full-width">
        <label className="form-label">Detailed Description</label>
        <textarea 
          name="detailedComplaintDescription" className="form-textarea"
          value={formData.detailedComplaintDescription || ''} onChange={handleChange}
        />
      </div>
      
      {/* QMS and AI Section */}
      <div className="form-group full-width qms-section">
        <div className="qms-title">
          <ShieldCheck size={20} />
          Quality Management System (ICH Q10 Assessment)
        </div>
        
        <div className="form-grid" style={{marginTop: '1rem'}}>
          <div className="form-group">
            <label className="form-label">Initial Severity</label>
            <input 
              type="text" name="initialSeverity" className="form-input"
              value={formData.initialSeverity || ''} readOnly style={{backgroundColor: '#e2e8f0'}}
            />
          </div>
          
          <div className="form-group">
            <label className="form-label">Regulatory Reportability</label>
            <input 
              type="text" name="regulatoryReportability" className="form-input"
              value={formData.regulatoryReportability || ''} readOnly style={{backgroundColor: '#e2e8f0'}}
            />
          </div>

          <div className="form-group">
            <label className="form-label">CAPA Required?</label>
            <input 
              type="text" name="capaRequired" className="form-input"
              value={formData.capaRequired || ''} readOnly style={{backgroundColor: '#e2e8f0'}}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Suggested Root Cause</label>
            <input 
              type="text" name="suggestedRootCause" className="form-input"
              value={formData.suggestedRootCause || ''} readOnly style={{backgroundColor: '#e2e8f0'}}
            />
          </div>
          
          <div className="form-group full-width">
            <label className="form-label">AI Risk Reasoning</label>
            <textarea 
              name="aiRiskAssessmentReasoning" className="form-textarea"
              value={formData.aiRiskAssessmentReasoning || ''} readOnly style={{backgroundColor: '#e2e8f0', minHeight: '60px'}}
            />
          </div>
        </div>
      </div>
    </form>
  );
};

export default ComplaintForm;
