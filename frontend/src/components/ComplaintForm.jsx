import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateComplaintField } from '../store/complaintSlice';
import { ShieldCheck, Save, CheckCircle, AlertTriangle, AlertCircle } from 'lucide-react';
import { saveComplaint } from '../services/api';

const ComplaintForm = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.complaint.data);
  const isDuplicate = useSelector((state) => state.complaint.isDuplicate);
  const [isSaving, setIsSaving] = React.useState(false);
  const [saveSuccess, setSaveSuccess] = React.useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    dispatch(updateComplaintField({ field: name, value }));
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      await saveComplaint(formData);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (error) {
      console.error("Error saving complaint:", error);
      alert("Failed to save complaint. See console.");
    } finally {
      setIsSaving(false);
    }
  };

  const getSeverityStyle = (severity) => {
    const baseStyle = { backgroundColor: '#e2e8f0' };
    if (!severity) return baseStyle;
    const lower = severity.toLowerCase();
    if (lower.includes('minor')) return { ...baseStyle, color: '#856404', backgroundColor: '#fff3cd', fontWeight: 'bold' };
    if (lower.includes('major')) return { ...baseStyle, color: '#b95000', backgroundColor: '#ffd8a8', fontWeight: 'bold' };
    if (lower.includes('critical')) return { ...baseStyle, color: '#721c24', backgroundColor: '#f8d7da', fontWeight: 'bold' };
    return baseStyle;
  };

  return (
    <form className="form-grid" onSubmit={(e) => e.preventDefault()}>
      
      {isDuplicate && (
        <div className="form-group full-width" style={{ 
          backgroundColor: '#fffbeb', border: '1px solid #fef3c7', 
          borderLeft: '4px solid #f59e0b', padding: '1rem', 
          borderRadius: '4px', display: 'flex', gap: '0.5rem', alignItems: 'center', color: '#b45309',
          fontWeight: 'bold'
        }}>
          <AlertTriangle size={20} />
          ⚠️ Potential Duplicate Detected: A complaint for this Product and Batch Number already exists in the database!
        </div>
      )}

      {/* Bonus Feature: Complaint Summary */}
      {formData.complaintSummary && (
        <div className="form-group full-width" style={{ backgroundColor: '#f0fdf4', padding: '1rem', borderRadius: '8px', border: '1px solid #bbf7d0' }}>
          <label className="form-label" style={{ color: '#166534', fontWeight: 'bold' }}>Complaint Summary (AI Generated)</label>
          <div style={{ color: '#15803d', fontSize: '0.95rem', marginTop: '0.25rem' }}>{formData.complaintSummary}</div>
        </div>
      )}

      {/* Bonus Feature: Completeness Checker */}
      {formData.completenessScore && (
        <div className="form-group full-width" style={{ backgroundColor: '#eff6ff', padding: '1rem', borderRadius: '8px', border: '1px solid #bfdbfe' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <label className="form-label" style={{ color: '#1e40af', fontWeight: 'bold' }}>Completeness Score</label>
            <span style={{ fontWeight: 'bold', color: '#1d4ed8' }}>{formData.completenessScore}</span>
          </div>
          {formData.missingInformation && (
            <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.5rem', color: '#b91c1c', fontSize: '0.85rem', alignItems: 'center', backgroundColor: '#fef2f2', padding: '0.5rem', borderRadius: '4px' }}>
              <AlertCircle size={16} />
              <strong>Missing Info:</strong> {formData.missingInformation}
            </div>
          )}
        </div>
      )}

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
          type="text" name="manufacturingDate" className="form-input"
          value={formData.manufacturingDate || ''} onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Expiry Date</label>
        <input 
          type="text" name="expiryDate" className="form-input"
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

      <div className="form-group">
        <label className="form-label">Complaint Date</label>
        <input 
          type="text" name="complaintDate" className="form-input"
          value={formData.complaintDate || ''} onChange={handleChange}
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
              value={formData.initialSeverity || ''} readOnly style={getSeverityStyle(formData.initialSeverity)}
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

      <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
        <button 
          onClick={handleSave} 
          disabled={isSaving || saveSuccess}
          style={{
            display: 'flex', alignItems: 'center', gap: '0.5rem',
            padding: '0.75rem 1.5rem', borderRadius: '8px',
            backgroundColor: saveSuccess ? '#00897b' : '#0d47a1', color: 'white',
            border: 'none', cursor: (isSaving || saveSuccess) ? 'not-allowed' : 'pointer',
            fontWeight: '600', transition: 'all 0.3s ease'
          }}
        >
          {saveSuccess ? <CheckCircle size={20} /> : <Save size={20} />}
          {isSaving ? 'Saving...' : saveSuccess ? 'Saved Successfully!' : 'Save Complaint'}
        </button>
      </div>
    </form>
  );
};

export default ComplaintForm;
