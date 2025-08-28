import os
import re
import fitz  # PyMuPDF
from dotenv import load_dotenv
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool

# Load environment variables
load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")

# Initialize search tool
search_tool = SerperDevTool(api_key=serper_api_key)


# -----------------------
# PDF Reader Tool
# -----------------------
class FinancialDocumentTool(BaseTool):
    name: str = "financial_document_tool"
    description: str = "Reads PDF financial documents and extracts the text content."

    def _run(self, file_path: str) -> str:
        """Read PDF and return its text"""
        try:
            if not os.path.exists(file_path):
                return f"Error: File not found at {file_path}"
            
            text = ""
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            
            if not text.strip():
                return "Error: No text content found in the PDF"
            
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"


financial_document_tool = FinancialDocumentTool()


# ---------------------------
# Investment Analysis Tool
# ---------------------------
class InvestmentTool(BaseTool):
    name: str = "investment_tool"
    description: str = "Analyzes financial document text to provide investment insights."

    def _run(self, financial_document_data: str) -> dict:
        """Analyze financial data for investment insights"""
        try:
            processed_data = " ".join(financial_document_data.split())

            # Extract financial metrics using regex
            revenue_patterns = [
                r"Revenue[:\s]*\$?([\d,]+(?:\.\d+)?)",
                r"Total Revenue[:\s]*\$?([\d,]+(?:\.\d+)?)",
                r"Net Revenue[:\s]*\$?([\d,]+(?:\.\d+)?)"
            ]
            
            profit_patterns = [
                r"(?:Net )?Profit[:\s]*\$?([\d,]+(?:\.\d+)?)",
                r"Net Income[:\s]*\$?([\d,]+(?:\.\d+)?)",
                r"Earnings[:\s]*\$?([\d,]+(?:\.\d+)?)"
            ]
            
            debt_patterns = [
                r"(?:Total )?Debt[:\s]*\$?([\d,]+(?:\.\d+)?)",
                r"Total Liabilities[:\s]*\$?([\d,]+(?:\.\d+)?)"
            ]

            def extract_value(patterns, text):
                for pattern in patterns:
                    match = re.search(pattern, text, re.I)
                    if match:
                        return float(match.group(1).replace(",", ""))
                return None

            revenue = extract_value(revenue_patterns, processed_data)
            profit = extract_value(profit_patterns, processed_data)
            debt = extract_value(debt_patterns, processed_data)

            insights = []
            
            # Calculate metrics if data is available
            if profit and revenue:
                profit_margin = (profit / revenue) * 100
                insights.append(f"Profit margin is {profit_margin:.2f}%")
                if profit_margin > 20:
                    insights.append("Strong profitability - Consider BUY")
                elif profit_margin > 10:
                    insights.append("Moderate profitability - HOLD recommended")
                else:
                    insights.append("Low profitability - Exercise caution")
                    
            if debt and revenue:
                debt_to_revenue = (debt / revenue) * 100
                insights.append(f"Debt-to-Revenue ratio: {debt_to_revenue:.1f}%")
                if debt_to_revenue > 100:
                    insights.append("High debt burden - Risk of financial distress")
                    
            if debt:
                insights.append(f"Total debt: ${debt:,}")
                if debt > 1_000_000_000:
                    insights.append("High debt level - Monitor cash flow carefully")

            return {
                "metrics": {
                    "revenue": revenue,
                    "profit": profit,
                    "debt": debt
                },
                "insights": insights
            }
        except Exception as e:
            return {"error": f"Investment analysis failed: {str(e)}"}


investment_tool = InvestmentTool()


# ---------------------------
# Risk Assessment Tool
# ---------------------------
class RiskTool(BaseTool):
    name: str = "risk_tool"
    description: str = "Performs comprehensive risk assessment on financial document text."

    def _run(self, financial_document_data: str) -> dict:
        """Perform risk assessment on financial data"""
        try:
            risks = []
            text_lower = financial_document_data.lower()

            # Market risk assessment
            market_risk_keywords = ['loss', 'decline', 'drop', 'downturn', 'volatility', 'market risk']
            market_risk_count = sum(1 for keyword in market_risk_keywords if keyword in text_lower)
            
            if market_risk_count >= 3:
                risks.append({
                    "type": "Market Risk",
                    "likelihood": "High",
                    "impact": "High",
                    "evidence": f"Multiple market risk indicators found ({market_risk_count} keywords)",
                    "mitigation": "Diversify portfolio and consider hedging strategies"
                })
            elif market_risk_count >= 1:
                risks.append({
                    "type": "Market Risk",
                    "likelihood": "Medium",
                    "impact": "Medium",
                    "evidence": f"Some market risk indicators found ({market_risk_count} keywords)",
                    "mitigation": "Monitor market conditions closely"
                })
            else:
                risks.append({
                    "type": "Market Risk",
                    "likelihood": "Low",
                    "impact": "Low",
                    "evidence": "No significant market risk indicators found",
                    "mitigation": "Standard market monitoring"
                })

            # Credit risk assessment
            debt_match = re.search(r"(?:Total )?Debt[:\s]*\$?([\d,]+(?:\.\d+)?)", financial_document_data, re.I)
            debt = float(debt_match.group(1).replace(",", "")) if debt_match else 0
            
            if debt > 5_000_000_000:
                likelihood, impact = "High", "High"
                evidence = f"Very high debt level: ${debt:,}"
                mitigation = "Immediate debt restructuring may be required"
            elif debt > 1_000_000_000:
                likelihood, impact = "Medium", "High"
                evidence = f"High debt level: ${debt:,}"
                mitigation = "Monitor debt service coverage and refinancing options"
            elif debt > 0:
                likelihood, impact = "Low", "Medium"
                evidence = f"Moderate debt level: ${debt:,}"
                mitigation = "Regular debt monitoring recommended"
            else:
                likelihood, impact = "Low", "Low"
                evidence = "No significant debt found"
                mitigation = "Maintain current debt management practices"
                
            risks.append({
                "type": "Credit Risk",
                "likelihood": likelihood,
                "impact": impact,
                "evidence": evidence,
                "mitigation": mitigation
            })

            # Operational risk assessment
            operational_keywords = ['recall', 'lawsuit', 'litigation', 'regulatory', 'compliance', 'investigation']
            operational_issues = [keyword for keyword in operational_keywords if keyword in text_lower]
            
            if operational_issues:
                risks.append({
                    "type": "Operational Risk",
                    "likelihood": "High",
                    "impact": "High",
                    "evidence": f"Operational issues found: {', '.join(operational_issues)}",
                    "mitigation": "Implement stronger compliance and operational controls"
                })
            else:
                risks.append({
                    "type": "Operational Risk",
                    "likelihood": "Low",
                    "impact": "Medium",
                    "evidence": "No major operational issues identified",
                    "mitigation": "Continue standard operational risk monitoring"
                })

            # Liquidity risk assessment
            liquidity_keywords = ['cash flow', 'liquidity', 'working capital', 'current assets', 'current liabilities']
            liquidity_mentions = sum(1 for keyword in liquidity_keywords if keyword in text_lower)
            
            if 'cash flow' in text_lower and ('negative' in text_lower or 'deficit' in text_lower):
                risks.append({
                    "type": "Liquidity Risk",
                    "likelihood": "High",
                    "impact": "High",
                    "evidence": "Negative cash flow indicators found",
                    "mitigation": "Secure additional funding sources and improve cash management"
                })
            elif liquidity_mentions > 0:
                risks.append({
                    "type": "Liquidity Risk",
                    "likelihood": "Medium",
                    "impact": "Medium",
                    "evidence": f"Liquidity metrics mentioned {liquidity_mentions} times",
                    "mitigation": "Monitor liquidity ratios and cash position"
                })
            else:
                risks.append({
                    "type": "Liquidity Risk",
                    "likelihood": "Low",
                    "impact": "Medium",
                    "evidence": "Limited liquidity information available",
                    "mitigation": "Request detailed cash flow analysis"
                })

            return {"risk_report": risks}
            
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}


risk_tool = RiskTool()