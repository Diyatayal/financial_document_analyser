## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from tools import search_tool, FinancialDocumentTool, InvestmentTool, RiskTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the uploaded financial document and provide a summary of key insights, trends, and notable figures.",
    expected_output="Return a structured summary with main financial metrics, trends, and recommendations if relevant.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Review the financial data and provide investment recommendations based on company performance and market conditions.",
    expected_output="Return actionable investment insights with reasoning based on financial metrics, e.g., buy/sell/hold recommendations.",
    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool, InvestmentTool.analyze_investment_tool, search_tool],
    async_execution=False,
)


## Creating a risk assessment task
risk_assessment = Task(
    description="Assess financial risks from the document across categories like market, credit, operational, and liquidity.",
    expected_output="Return a structured risk report including risk likelihood, impact, and recommendations for mitigation.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool, RiskTool.create_risk_assessment_tool],
    async_execution=False,
)

    
verification = Task(
    description="Verify whether the uploaded document is a valid financial document.",
    expected_output="Return 'Valid' or 'Invalid' with reasoning based on document structure and content.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)