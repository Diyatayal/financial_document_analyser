from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
from crewai import Crew, Process
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)
from tools import financial_document_tool
from task import (  # Fixed import name
    analyze_financial_document,
    investment_analysis,
    risk_assessment,
    verification
)

app = FastAPI(title="Financial Document Analyzer")

def run_crew_sync(query: str, file_path: str):
    """Run all agents and tasks of the Crew on a financial document - SYNC VERSION."""
    
    # Verify file exists
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    
    # Test file reading first
    try:
        test_content = financial_document_tool._run(file_path)
        if "Error" in test_content:
            raise Exception(f"File reading error: {test_content}")
    except Exception as e:
        raise Exception(f"Cannot read PDF file: {str(e)}")

    # Create a Crew with all agents and tasks
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True
    )

    # Prepare inputs for the crew
    inputs = {
        'query': query,
        'file_path': file_path
    }

    # Kickoff the Crew synchronously
    result = financial_crew.kickoff(inputs)
    
    return result

async def run_crew(query: str, file_path: str):
    """Async wrapper for crew execution."""
    try:
        # Run the synchronous crew in a thread pool
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            run_crew_sync, 
            query, 
            file_path
        )
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crew execution failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Financial Document Analyzer",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_financial_document_api(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for comprehensive insights")
):
    """
    Analyze a financial document (PDF) and return comprehensive analysis including:
    - Document verification
    - Financial analysis
    - Investment recommendations  
    - Risk assessment
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported"
        )
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            f.write(content)
        
        # Validate query
        if not query or not query.strip():
            query = "Analyze this financial document for comprehensive insights"
        
        # Run the crew analysis
        response = await run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "filename": file.filename,
            "analysis": response,
            "message": "Financial document analysis completed successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_error:
                print(f"Warning: Could not remove temporary file {file_path}: {cleanup_error}")

@app.post("/verify-only")
async def verify_document_api(
    file: UploadFile = File(...)
):
    """
    Verify if uploaded document is a valid financial document
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    file_id = str(uuid.uuid4())
    file_path = f"data/verify_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            f.write(content)
        
        # Create crew with only verifier agent and verification task
        verify_crew = Crew(
            agents=[verifier],
            tasks=[verification],
            process=Process.sequential,
            verbose=True
        )
        
        # Run synchronously in executor
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            verify_crew.kickoff, 
            {'file_path': file_path}
        )
        
        return {
            "status": "success",
            "filename": file.filename,
            "verification_result": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=True)