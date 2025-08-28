## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import Pdf

from crewai_tools import tools
from crewai_tools.tools.serper_dev_tool import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @staticmethod
    def read_data_tool(path='data/TSLA-Q2-2025-Update.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/TSLA-Q2-2025-Update.pdf'.

        Returns:
            str: Full Financial Document file
        """
        
        docs = Pdf(file_path=path).load()

        full_report = ""
        for data in docs:
           content = data.page_content.replace("\n\n", "\n")
           full_report += content + "\n"

        return full_report

## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """
        Processes financial document data and extracts key insights
        for investment decision-making.

        Args:
            financial_document_data (str): The text of the financial document.

        Returns:
            dict: A dictionary containing financial metrics and investment insights.
        """
        # Clean the data
        processed_data = " ".join(financial_document_data.split())  # remove extra spaces

        # Example logic: extract some financial metrics (simulated)
        import re

        revenue_match = re.search(r"Revenue[:\s]\$?([\d,.]+)", processed_data)
        profit_match = re.search(r"Profit[:\s]\$?([\d,.]+)", processed_data)
        debt_match = re.search(r"Debt[:\s]\$?([\d,.]+)", processed_data)

        revenue = float(revenue_match.group(1).replace(",", "")) if revenue_match else None
        profit = float(profit_match.group(1).replace(",", "")) if profit_match else None
        debt = float(debt_match.group(1).replace(",", "")) if debt_match else None

        # Generate simple insights
        insights = []
        if profit and revenue:
            profit_margin = (profit / revenue) * 100
            insights.append(f"Profit margin is {profit_margin:.2f}%")
            if profit_margin > 20:
                insights.append("The company has strong profitability.")
            else:
                insights.append("Profitability is moderate or low.")
        if debt:
            insights.append(f"Total debt is ${debt:,}")
            if debt > 1_000_000_000:
                insights.append("The company has high debt. Be cautious!")

        return {
            "metrics": {
                "revenue": revenue,
                "profit": profit,
                "debt": debt
            },
            "insights": insights
        }


## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        """
        Evaluates financial risks based on the document content.

        Args:
            financial_document_data (str): The text of the financial document.

        Returns:
            dict: Risk assessment report with likelihood and impact.
        """
        import re

        # Example: identify high-level risks
        risks = []

        # Market risk (high if revenue fluctuates a lot)
        if re.search(r"(loss|decline|drop)", financial_document_data, re.I):
            risks.append({
                "type": "Market Risk",
                "likelihood": "High",
                "impact": "High",
                "evidence": "Mentions of loss, decline, or drop in financial performance.",
                "mitigation": "Diversify investments and monitor market trends closely."
            })
        else:
            risks.append({
                "type": "Market Risk",
                "likelihood": "Medium",
                "impact": "Medium",
                "evidence": "No major negative trends detected.",
                "mitigation": "Monitor revenue and profit trends regularly."
            })

        # Credit risk (based on debt)
        debt_match = re.search(r"Debt[:\s]\$?([\d,.]+)", financial_document_data)
        if debt_match:
            debt = float(debt_match.group(1).replace(",", ""))
            if debt > 1_000_000_000:
                likelihood = "High"
                impact = "High"
            else:
                likelihood = "Medium"
                impact = "Medium"
        else:
            likelihood = "Low"
            impact = "Low"

        risks.append({
            "type": "Credit Risk",
            "likelihood": likelihood,
            "impact": impact,
            "evidence": f"Total debt detected: {debt if debt_match else 'Not reported'}",
            "mitigation": "Maintain conservative debt exposure and monitor debt ratios."
        })

        # Operational risk (dummy example)
        if "recall" in financial_document_data.lower() or "lawsuit" in financial_document_data.lower():
            risks.append({
                "type": "Operational Risk",
                "likelihood": "High",
                "impact": "High",
                "evidence": "Mentions of recall or lawsuit in the document.",
                "mitigation": "Review operational processes and legal compliance."
            })
        else:
            risks.append({
                "type": "Operational Risk",
                "likelihood": "Low",
                "impact": "Low",
                "evidence": "No operational issues detected.",
                "mitigation": "Maintain regular audits and monitoring."
            })

        return {
            "risk_report": risks
        }
