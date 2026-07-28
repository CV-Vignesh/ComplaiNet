import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  data: {
    complaintSource: '',
    customerName: '',
    productName: '',
    productStrengthGrade: '',
    batchLotNumber: '',
    manufacturingDate: '',
    expiryDate: '',
    quantityAffected: '',
    complaintType: '',
    complaintDate: '',
    detailedComplaintDescription: '',
    initialSeverity: '',
    priority: '',
    aiRiskAssessmentReasoning: '',
    capaRequired: '',
    suggestedRootCause: '',
    regulatoryReportability: '',
    investigationStatus: 'Pending Triage'
  },
  isDuplicate: false,
  status: 'idle',
  error: null
};

export const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    updateComplaintField: (state, action) => {
      const { field, value } = action.payload;
      state.data[field] = value;
    },
    updateEntireComplaint: (state, action) => {
      state.data = { ...state.data, ...action.payload };
    },
    setComplaintData: (state, action) => {
      state.data = action.payload.data;
      state.isDuplicate = action.payload.isDuplicate || false;
    },
    resetComplaint: (state) => {
      state.data = initialState.data;
      state.isDuplicate = false;
    }
  }
});

export const { updateComplaintField, updateEntireComplaint, setComplaintData, resetComplaint } = complaintSlice.actions;
export default complaintSlice.reducer;
