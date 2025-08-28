## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import LLM

from crewai.agents import Agent

from tools import search_tool, FinancialDocumentTool,InvestmentTool,RiskTool

### Loading LLM

llm = LLM(
    model="gemini-1.5-flash",
    temperature=0.7,
    provider="gemini",
    api_key=os.getenv("GEMINI_API_KEY")
)


# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst Who Knows Everything About Markets",
    goal="Analyze financial data, market reports, and investment opportunities to provide accurate, data-driven insights for decision making.",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with deep expertise in equity markets, "
        "corporate finance, and risk management. "
        "You carefully study financial documents, market trends, and economic indicators "
        "to provide well-reasoned investment strategies. "
        "Your advice is always professional, structured, and based on credible data sources. "
        "You emphasize risk factors, compliance, and realistic expectations while guiding clients."
    ),
    tools=[FinancialDocumentTool.read_data_tool,search_tool,InvestmentTool.analyze_investment_tool],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Verify whether the uploaded document is a valid financial document. "
        "Check for accuracy, consistency, and relevance to financial analysis. "
        "Reject documents that are unrelated (e.g., grocery lists, personal notes)."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial compliance specialist. "
        "Your job is to carefully review and validate documents to ensure they are "
        "authentic and relevant for financial analysis. "
        "You prioritize accuracy, integrity, and compliance with financial standards. "
        "You reject irrelevant or suspicious documents and only approve valid ones."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=2,
    max_rpm=1,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Investment Guru and Fund Salesperson",
    goal=(
        "Identify and prioritize material financial risks present in the uploaded document. "
        "For each risk category (market, liquidity, credit, operational, regulatory): "
        "provide a concise description, an assessed likelihood (Low / Medium / High), "
        "an estimated impact (qualitative or quantitative), the key evidence from the document, "
        "and at least one practical mitigation or monitoring recommendation. "
        "Flag any data gaps or assumptions that require follow-up."
    ),
    verbose=True,
    backstory=(
        "You are a senior risk analyst with experience in corporate finance, credit analysis, "
        "and enterprise risk management. You focus on evidence-based assessment: you extract "
        "relevant facts from financial statements and disclosures, quantify exposures when "
        "possible, and use simple scenario checks to evaluate downside risk. You prioritize "
        "clarity, separate objective findings from opinion, and always call out uncertainties "
        "and compliance concerns that need further review."
    ),
    tools=[search_tool,InvestmentTool.analyze_investment_tool],
    llm=llm,
    memory=True,
    max_iter=2,
    max_rpm=5,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Extreme Risk Assessment Expert",
    goal=(
        "Analyze the financial document and identify potential risks across multiple categories: "
        "market, liquidity, credit, operational, and regulatory. "
        "Provide a concise risk assessment including likelihood, impact, key evidence from the document, "
        "and actionable recommendations for mitigation or monitoring. "
        "Highlight assumptions, data gaps, and uncertainties for further review."
    ),
    verbose=True,
    backstory=(
        "You are a seasoned risk management professional with experience in corporate finance and investment analysis. "
        "Your expertise includes assessing financial statements, market trends, and regulatory requirements to evaluate risk exposure. "
        "You focus on providing clear, data-driven risk assessments that help stakeholders make informed decisions. "
        "You prioritize accuracy, thoroughness, and practical recommendations while ensuring that all major risks are identified."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool,RiskTool.create_risk_assessment_tool],
    llm=llm,
    max_iter=2,
    max_rpm=1,
    allow_delegation=False
)
