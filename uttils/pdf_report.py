from fpdf import FPDF

def generate_pdf_report(data, filename='seo_report.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'SEO InsightHub Report', ln=True, align='C')
    pdf.ln(10)

    for site in data:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"Website: {site['url']}", ln=True)
        if 'error' in site:
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f"Error: {site['error']}", ln=True)
            continue

        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Title: {site['title']}", ln=True)
        pdf.cell(0, 10, f"Meta Description: {site['meta_description']}", ln=True)
        pdf.cell(0, 10, "Headings:", ln=True)
        for htag, texts in site['headings'].items():
            pdf.cell(0, 10, f"  {htag.upper()}: {', '.join(texts)}", ln=True)
        pdf.ln(10)

    pdf.output(filename)
    return filename
