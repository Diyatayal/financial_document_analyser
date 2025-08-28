## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import LLM
from crewai import Agent
from tools import financial_document_tool, search_tool, investment_tool, risk_tool

### Loading LLM
llm = LLM(
    model="gemini-1.5-flash",
    temperature=0.7,
    provider="gemini",
    api_key=os.getenv("GEMINI_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents to extract key metrics, trends, and provide comprehensive financial insights for decision making.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with deep expertise in equity markets, "
        "corporate finance, and financial statement analysis. "
        "You carefully study financial documents, extract key metrics, and identify trends "
        "to provide well-reasoned financial insights. "
        "Your analysis is always professional, structured, and based on credible data sources. "
        "You focus on financial performance, growth trends, and overall company health."
    ),
    tools=[financial_document_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Verify whether the uploaded document is a valid financial document. "
        "Check for accuracy, consistency, and relevance to financial analysis. "
        "Identify document type and ensure it contains financial information."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial compliance specialist with expertise in "
        "document verification and validation. Your job is to carefully review "
        "documents to ensure they are authentic financial documents suitable for analysis. "
        "You can identify various types of financial documents like annual reports, "
        "quarterly statements, balance sheets, income statements, and cash flow statements. "
        "You reject irrelevant documents and only approve valid financial documents."
    ),
    tools=[financial_document_tool],
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=False
)

# Fixed investment advisor agent
investment_advisor = Agent(
    role="Investment Advisor and Portfolio Strategist",
    goal=(
        "Analyze financial documents to provide actionable investment recommendations. "
        "Evaluate company performance, profitability, growth potential, and market position "
        "to determine buy, sell, or hold recommendations with clear reasoning. "
        "Consider valuation metrics, financial health, and market conditions in recommendations."
    ),
    verbose=True,
    backstory=(
        "You are a seasoned investment advisor with extensive experience in portfolio management "
        "and equity research. You specialize in analyzing company financials to identify "
        "investment opportunities and risks. Your recommendations are based on thorough "
        "analysis of financial metrics, industry trends, and market conditions. "
        "You provide clear, actionable investment advice with supporting rationale "
        "and always consider risk-adjusted returns in your recommendations."
    ),
    tools=[financial_document_tool, investment_tool, search_tool],
    llm=llm,
    memory=True,
    max_iter=3,
    max_rpm=5,
    allow_delegation=False
)

# Risk assessor agent
risk_assessor = Agent(
    role="Risk Management Specialist",
    goal=(
        "Identify and assess financial risks across multiple categories including "
        "market, liquidity, credit, operational, and regulatory risks. "
        "Provide detailed risk analysis with likelihood assessments, impact evaluations, "
        "supporting evidence, and practical mitigation recommendations. "
        "Flag critical risks that require immediate attention."
    ),
    verbose=True,
    backstory=(
        "You are a seasoned risk management professional with expertise in enterprise "
        "risk assessment and financial risk analysis. Your background includes corporate "
        "finance, credit analysis, and regulatory compliance. You excel at identifying "
        "potential risks from financial documents and market data, quantifying their "
        "impact, and developing practical risk mitigation strategies. "
        "You prioritize evidence-based risk assessment and provide actionable "
        "recommendations to help organizations manage their risk exposure effectively."
    ),
    tools=[financial_document_tool, risk_tool],
    llm=llm,
    max_iter=3,
    max_rpm=5,
    allow_delegation=False
)