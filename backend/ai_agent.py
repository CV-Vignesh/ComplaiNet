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
    complaintSource: Optional[str] = Field(default=None, description="Origin of complaint, e.g. Pharmacy, Hospital, Direct Customer")
    customerName: Optional[str] = Field(default=None, description="Name of the person, hospital, pharmacy, or entity making the complaint (e.g. Apollo Pharmacy)")
    productName: Optional[str] = Field(default=None, description="Name of the pharmaceutical product")
    productStrengthGrade: Optional[str] = Field(default=None, description="Strength or grade, e.g., 500 mg")
    batchLotNumber: Optional[str] = Field(default=None, description="Batch or lot number")
    manufacturingDate: Optional[str] = Field(default=None, description="Date of manufacturing")
    expiryDate: Optional[str] = Field(default=None, description="Expiry date")
    quantityAffected: Optional[str] = Field(default=None, description="Quantity affected with unit, e.g., 48 capsules, 50 kg")
    complaintType: Optional[str] = Field(default=None, description="Category of the complaint, e.g., Discoloration, Packaging defect")
    complaintDate: Optional[str] = Field(default=None, description="Date the complaint was reported")
    detailedComplaintDescription: Optional[str] = Field(default=None, description="Full description of the issue")
    initialSeverity: Optional[str] = Field(default=None, description="Initial severity: Critical, Major, or Minor")
    priority: Optional[str] = Field(default=None, description="Priority: High, Medium, or Low")
    aiRiskAssessmentReasoning: Optional[str] = Field(default=None, description="AI's reasoning for risk and severity based on pharma context")
    capaRequired: Optional[str] = Field(default=None, description="Yes, No, or Needs Review based on systemic risk (ICH Q10)")
    suggestedRootCause: Optional[str] = Field(default=None, description="AI suggested likely root cause, e.g., Manufacturing, Storage, Packaging")
    regulatoryReportability: Optional[str] = Field(default=None, description="High, Low, or None. E.g., High for adverse events or contamination")
    investigationStatus: Optional[str] = Field(default="Pending Triage")

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
                "You are a Pharma Tech QA AI Assistant with a 100% accuracy requirement. "
                "Your task is to update the existing complaint data based on the user's new instructions. "
                "You MUST preserve all other existing information exactly as it is. "
                "CRITICAL: Based on the new updates, you must also use your reasoning to re-evaluate and update "
                "the AI Copilot Risk Assessment Section (initialSeverity, priority, aiRiskAssessmentReasoning, "
                "capaRequired, suggestedRootCause, regulatoryReportability) applying ICH Q10 principles.\n"
                f"Existing Data: {safe_json}"
            )
        else:
            system_prompt = (
                "You are a Pharma Tech QA AI Assistant with a 100% accuracy requirement. "
                "Your task is to extract complaint details from the provided text and structure them according to the schema. "
                "CRITICAL: You must use your medical/pharma reasoning to evaluate and populate the "
                "AI Copilot Risk Assessment Section (initialSeverity, priority, aiRiskAssessmentReasoning, "
                "capaRequired, suggestedRootCause, regulatoryReportability) applying ICH Q10 principles."
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
