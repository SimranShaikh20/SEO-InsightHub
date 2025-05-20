from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SEO InsightHub Report', 0, 1, 'C')

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 8, content)
        self.ln(4)

def format_structured_data(data):
    """
    Format structured data (dicts, lists) into readable text for PDF.
    """
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{key.capitalize()}:")
                for subkey, subval in value.items():
                    if isinstance(subval, list):
                        lines.append(f"  {subkey}:")
                        for item in subval:
                            lines.append(f"    - {item}")
                    else:
                        lines.append(f"  {subkey}: {subval}")
            elif isinstance(value, list):
                lines.append(f"{key.capitalize()}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key.capitalize()}: {value}")
        return "\n".join(lines)
    elif isinstance(data, list):
        return "\n".join(f"- {item}" for item in data)
    else:
        # fallback to str
        return str(data)

def generate_pdf_report(analysis_summary, keywords, groq_advice, agno_output):
    pdf = PDF()
    pdf.add_page()

    # Format analysis_summary if it's structured data
    formatted_summary = format_structured_data(analysis_summary)
    pdf.add_section("Website Analysis Summary", formatted_summary)

    # keywords might be list or string
    if isinstance(keywords, (list, tuple)):
        formatted_keywords = ", ".join(keywords)
    else:
        formatted_keywords = str(keywords)
    pdf.add_section("Trending Keywords", formatted_keywords)

    pdf.add_section("GROQ AI Advice", groq_advice)
    pdf.add_section("AGNO Agent Insight", agno_output)

    pdf.output("SEO_Report.pdf")
