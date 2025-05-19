
from agno.agent import Agent
from fpdf import FPDF
from typing import List, Dict, Any

class PDFAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PDF Report Agent",
            description="Generates comprehensive PDF reports from SEO analysis data"
        )
    
    async def execute(self, data: List[Dict[str, Any]], filename: str = 'seo_report.pdf') -> str:
        """Generate PDF report using Agno framework"""
        self.logger.info(f"Generating PDF report for {len(data)} websites")
        
        try:
            await self.log_event("pdf_generation_started", {
                "sites_count": len(data),
                "filename": filename
            })
            
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 20)
            pdf.cell(0, 15, 'SEO InsightHub Analysis Report', ln=True, align='C')
            pdf.ln(10)
            
            # Date
            from datetime import datetime
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='C')
            pdf.ln(15)

            # Process each website
            for i, site in enumerate(data):
                # Website header
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(0, 10, f"Website {i+1}: {site['url']}", ln=True)
                pdf.ln(5)
                
                if 'error' in site:
                    pdf.set_font('Arial', '', 12)
                    pdf.set_text_color(255, 0, 0)  # Red for errors
                    pdf.cell(0, 10, f"Error: {site['error']}", ln=True)
                    pdf.set_text_color(0, 0, 0)  # Reset to black
                    pdf.ln(10)
                    continue

                # Basic SEO info
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, "Title:", ln=True)
                pdf.set_font('Arial', '', 11)
                pdf.multi_cell(0, 6, site['title'] or "No title found")
                pdf.ln(3)
                
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, "Meta Description:", ln=True)
                pdf.set_font('Arial', '', 11)
                pdf.multi_cell(0, 6, site['meta_description'] or "No meta description found")
                pdf.ln(3)
                
                # Headings analysis
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, "Headings Structure:", ln=True)
                pdf.set_font('Arial', '', 11)
                for htag, texts in site['headings'].items():
                    if texts:
                        pdf.cell(0, 6, f"  {htag.upper()} ({len(texts)}): ", ln=False)
                        pdf.multi_cell(0, 6, f"{', '.join(texts[:3])}{'...' if len(texts) > 3 else ''}")
                    else:
                        pdf.cell(0, 6, f"  {htag.upper()}: None found", ln=True)
                
                pdf.ln(10)

            pdf.output(filename)
            
            await self.log_event("pdf_generation_completed", {
                "filename": filename,
                "sites_processed": len(data)
            })
            
            self.logger.info(f"PDF report generated successfully: {filename}")
            return filename
            
        except Exception as e:
            await self.log_event("pdf_generation_failed", {
                "error": str(e)
            })
            self.logger.error(f"PDF generation failed: {str(e)}")
            raise e