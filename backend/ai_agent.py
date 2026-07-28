from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Define the structured output matching our Pydantic schema + ICH Q10 fields
class ComplaintExtraction(BaseModel):
    complaintSource: Optional[str] = Field(default=None, description="Must be exactly one of: 'Direct Customer', 'Hospital/Clinic', 'Pharmacy', or 'Distributor'.")
    customerName: Optional[str] = Field(default=None, description="Name of the person, hospital, pharmacy, or entity making the complaint. DO NOT auto-populate this from the complaint source. Only fill this if a specific name is explicitly provided in the text.")
    productName: Optional[str] = Field(default=None, description="Name of the pharmaceutical product")
    productStrengthGrade: Optional[str] = Field(default=None, description="Strength or grade, e.g., 500 mg")
    batchLotNumber: Optional[str] = Field(default=None, description="Batch or lot number")
    manufacturingDate: Optional[str] = Field(default=None, description="Date of manufacturing. Extract EXACTLY as provided (e.g., 'May 2023', '12-05-2023').")
    expiryDate: Optional[str] = Field(default=None, description="Expiry date. Extract EXACTLY as provided (e.g., 'May 2023', '12-05-2023').")
    quantityAffected: Optional[str] = Field(default=None, description="Quantity affected with unit, e.g., 48 capsules, 50 kg")
    complaintType: Optional[str] = Field(default=None, description="Category of the complaint, e.g., Discoloration, Packaging defect")
    complaintDate: Optional[str] = Field(default=None, description="Date the complaint was reported. Extract EXACTLY as provided.")
    detailedComplaintDescription: Optional[str] = Field(default=None, description="Full description of the issue")
    initialSeverity: Optional[str] = Field(default=None, description="Initial severity: Critical, Major, or Minor")
    priority: Optional[str] = Field(default=None, description="Priority: High, Medium, or Low")
    aiRiskAssessmentReasoning: Optional[str] = Field(default=None, description="AI's reasoning for risk and severity based on pharma context")
    capaRequired: Optional[str] = Field(default=None, description="Yes, No, or Needs Review based on systemic risk (ICH Q10)")
    suggestedRootCause: Optional[str] = Field(default=None, description="AI suggested likely root cause, e.g., Manufacturing, Storage, Packaging")
    regulatoryReportability: Optional[str] = Field(default=None, description="High, Low, or None. E.g., High for adverse events or contamination")
    investigationStatus: Optional[str] = Field(default="Pending Triage")
    complaintSummary: Optional[str] = Field(default=None, description="A 1-sentence TLDR summary of the complaint.")
    completenessScore: Optional[str] = Field(default=None, description="A percentage score (0-100%) indicating how complete the complaint details are. 100% means all product, batch, date, and defect info is present.")
    missingInformation: Optional[str] = Field(default=None, description="A comma-separated list of critical missing fields (e.g., 'Batch Number, Expiry Date'). If 100% complete, leave null.")
    
    # NEW ADVANCED AI FEATURES
    immediateActionPlan: Optional[str] = Field(default=None, description="A strict, 3-step immediate action plan for the QA team (e.g., '1. Quarantine stock. 2. Notify regulatory. 3. Investigate root cause.').")
    customerSentiment: Optional[str] = Field(default=None, description="The emotional tone of the complaint (e.g., 'Highly Litigious', 'Distressed', 'Neutral').")
    escalationRisk: Optional[str] = Field(default=None, description="Return 'Yes' if the customer is threatening a lawsuit, going to the press, or if it's a critical safety issue. Otherwise 'No'.")
    regulatoryFramework: Optional[str] = Field(default=None, description="Predict which specific FDA/EMA regulatory framework or form is triggered (e.g., 'FDA MedWatch Form 3500A', '21 CFR Part 211').")

class AgentState(TypedDict):
    messages: list[BaseMessage]
    current_complaint_data: Dict[str, Any]

def create_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0
    )
    structured_llm = llm.with_structured_output(ComplaintExtraction)

    def extract_node(state: AgentState):
        messages = state["messages"]
        current_data = state.get("current_complaint_data", {})
        
        user_input = messages[-1].content
        
        # If there is existing data, we are editing. Otherwise, we are creating.
        if current_data:
            safe_json = json.dumps(current_data).replace('{', '{{').replace('}', '}}')
            system_prompt = (
                "You are an Elite Pharma Tech QA AI Assistant. ACCURACY IS ABSOLUTE. "
                "Your task is to update the existing complaint data based on the user's new instructions. "
                "You MUST preserve all other existing information exactly as it is, word-for-word. "
                "CRITICAL: Based on the new updates, you must profoundly use your medical reasoning to re-evaluate and update "
                "the AI Copilot Risk Assessment Section (initialSeverity, priority, aiRiskAssessmentReasoning, "
                "capaRequired, suggestedRootCause, regulatoryReportability) applying ICH Q10 principles.\n"
                "NEW: You must generate a 3-step immediateActionPlan for QA triage. Analyze customerSentiment and flag escalationRisk ('Yes' or 'No'). Predict the exact FDA/EMA regulatoryFramework triggered by this issue.\n"
                f"Existing Data: {safe_json}"
            )
        else:
            system_prompt = (
                "You are an Elite Pharma Tech QA AI Assistant. ACCURACY IS ABSOLUTE. "
                "Your task is to extract complaint details from the provided text and structure them perfectly according to the schema. "
                "Do NOT hallucinate data. If a field is not mentioned, leave it null. Extract dates and quantities exactly as written. "
                "CRITICAL INSTRUCTION: Do NOT auto-populate the Customer/Source Name simply based on the Complaint Source. Only populate Customer/Source Name if a specific entity name is explicitly provided.\n"
                "CRITICAL: You must use your medical/pharma reasoning to comprehensively evaluate and populate the "
                "AI Copilot Risk Assessment Section (initialSeverity, priority, aiRiskAssessmentReasoning, "
                "capaRequired, suggestedRootCause, regulatoryReportability) applying ICH Q10 principles. "
                "Additionally, provide a 1-sentence complaintSummary. "
                "NEW ADVANCED FEATURES: You must generate a 3-step immediateActionPlan for QA triage. Analyze the text for customerSentiment (e.g. Litigious, Distressed) and flag escalationRisk ('Yes' or 'No'). Finally, predict the exact FDA/EMA regulatoryFramework triggered by this complaint."
            )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        chain = prompt | structured_llm
        result = chain.invoke({"input": user_input})
        
        # Merge if editing
        new_data = result.model_dump(exclude_unset=True, exclude_none=True)
        if current_data:
            current_data.update(new_data)
            final_data = current_data
        else:
            final_data = result.model_dump()

        # Add AI message
        ai_msg = AIMessage(content="I have processed the complaint details and updated the form.")
        
        return {"messages": messages + [ai_msg], "current_complaint_data": final_data}

    workflow = StateGraph(AgentState)
    workflow.add_node("extract", extract_node)
    workflow.add_edge(START, "extract")
    workflow.add_edge("extract", END)

    return workflow.compile()

agent_app = create_agent()

def process_prompt(prompt_text: str, current_data: Dict[str, Any] = None) -> Dict[str, Any]:
    state = {
        "messages": [HumanMessage(content=prompt_text)],
        "current_complaint_data": current_data or {}
    }
    result = agent_app.invoke(state)
    return {
        "reply": result["messages"][-1].content,
        "data": result["current_complaint_data"]
    }
