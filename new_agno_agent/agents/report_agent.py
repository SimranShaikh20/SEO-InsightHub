from agno_agent import Agent
from fpdf import FPDF
from datetime import datetime

class ReportAgent(Agent):
    def __init__(self):
        super().__init__("ReportAgent")
    
    def generate_pdf(self, analysis_results, ai_recommendations, user_url, competitor_urls):
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "SEO InsightHub Analysis Report", 0, 1, 'C')
        pdf.ln(10)
        
        # Date and URLs
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.cell(0, 10, f"Your website: {user_url}", 0, 1)
        pdf.cell(0, 10, f"Competitors: {', '.join(competitor_urls)}", 0, 1)
        pdf.ln(10)
        
        # Comparison table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "SEO Metrics Comparison", 0, 1)
        pdf.set_font("Arial", '', 10)
        
        # Create table
        self._create_table(pdf, analysis_results['comparison_table'])
        pdf.ln(10)
        
        # Quick wins
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Top 5 Quick SEO Improvements", 0, 1)
        pdf.set_font("Arial", '', 12)
        
        for i, rec in enumerate(ai_recommendations['quick_wins'], 1):
            pdf.cell(0, 10, f"{i}. {rec}", 0, 1)
        pdf.ln(5)
        
        # Detailed analysis
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Detailed SEO Recommendations", 0, 1)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, ai_recommendations['detailed_analysis'])
        
        return pdf.output(dest='S').encode('latin1')
    
    def _create_table(self, pdf, df):
        col_width = pdf.w / (len(df.columns) + 1)
        row_height = pdf.font_size * 1.5
        
        # Header
        pdf.set_fill_color(200, 220, 255)
        for col in df.columns:
            pdf.cell(col_width, row_height, str(col), border=1, fill=True)
        pdf.ln(row_height)
        
        # Data
        pdf.set_fill_color(255, 255, 255)
        for _, row in df.iterrows():
            for col in df.columns:
                value = str(row[col]) if not isinstance(row[col], float) else f"{row[col]:.2f}"
                pdf.cell(col_width, row_height, value, border=1)
            pdf.ln(row_height)