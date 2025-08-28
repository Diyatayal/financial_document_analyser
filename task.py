## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from tools import search_tool, financial_document_tool, risk_tool, investment_tool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=(
        "Analyze the financial document at the provided file path. "
        "Extract key financial metrics, identify trends, and provide comprehensive insights. "
        "Use the file_path variable to read the document: {file_path}"
    ),
    expected_output=(
        "Return a structured summary with:\n"
        "- Main financial metrics (revenue, profit, assets, liabilities)\n"
        "- Key performance indicators and ratios\n"
        "- Notable trends and year-over-year changes\n"
        "- Overall financial health assessment\n"
        "- Relevant recommendations for stakeholders"
    ),
    agent=financial_analyst,
    tools=[financial_document_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Based on the financial document analysis, provide detailed investment recommendations. "
        "Consider company performance, market conditions, and financial health. "
        "Use the file_path to access the document: {file_path}"
    ),
    expected_output=(
        "Return actionable investment insights including:\n"
        "- Clear buy/sell/hold recommendation with rationale\n"
        "- Key financial metrics supporting the recommendation\n"
        "- Risk factors to consider\n"
        "- Price targets or valuation estimates if applicable\n"
        "- Timeline and conditions for the recommendation"
    ),
    agent=investment_advisor,
    tools=[financial_document_tool, investment_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Conduct comprehensive risk assessment of the financial document. "
        "Analyze risks across market, credit, operational, liquidity, and regulatory categories. "
        "Use the file_path to access the document: {file_path}"
    ),
    expected_output=(
        "Return a structured risk report with:\n"
        "- Risk categories (Market, Credit, Operational, Liquidity, Regulatory)\n"
        "- Likelihood assessment (Low/Medium/High) for each risk\n"
        "- Impact evaluation with supporting evidence from document\n"
        "- Specific mitigation recommendations\n"
        "- Priority ranking of identified risks"
    ),
    agent=risk_assessor,
    tools=[financial_document_tool, risk_tool],
    async_execution=False,
)

## Creating document verification task
verification = Task(
    description=(
        "Verify whether the uploaded document is a valid financial document. "
        "Check document structure, content relevance, and financial data presence. "
        "Use the file_path to access the document: {file_path}"
    ),
    expected_output=(
        "Return verification result with:\n"
        "- 'Valid Financial Document' or 'Invalid Document'\n"
        "- Document type identification (Annual Report, 10-K, Balance Sheet, etc.)\n"
        "- Key financial sections found in the document\n"
        "- Detailed reasoning for validation decision\n"
        "- Confidence level in the assessment"
    ),
    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)