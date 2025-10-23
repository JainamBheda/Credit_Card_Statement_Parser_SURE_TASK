import pdfplumber
import re
import os
from flask import Flask, render_template, request, redirect, url_for

# --- Flask App Setup ---
app = Flask(__name__)

# --- PDF Parsing Logic (Copied from your script) ---

def extract_text_from_pdf(pdf_stream):
    """Extract all text from a PDF file stream using pdfplumber."""
    text = ""
    # pdfplumber.open() can accept a file path OR a file-like object (stream)
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_statement(text):
    """Extract 5 reliable fields from any bank statement."""
    data = {}

    # 1️⃣ Account Holder
    match = re.search(
        r"(?:Account Holder|Customer Name|Name)(?:\s*Name)?[:\s]*\n?([A-Za-z\s]+)",
        text, re.IGNORECASE
    )
    if match:
        holder = match.group(1).strip().title()
        holder = holder.split("Account Number")[0].strip()
        holder = holder.split("Address")[0].strip()
        data["Account Holder"] = holder
    else:
        data["Account Holder"] = "N/A"

    # 2️⃣ Account Number
    match = re.search(
        r"Account (?:Number|No)[:\s]*([\d\sX-]+)", 
        text, re.IGNORECASE
    )
    data["Account Number"] = match.group(1).strip() if match else "N/A"

    # 3️⃣ Statement Period
    date_regex = r"[\d]{1,2}[\/\-.][\d]{1,2}[\/\-.][\d]{2,4}"
    match = re.search(
        r"(?:Statement\s*(?:Period|Date))[:\s]*(?:From\s*)?(" + date_regex + r"\s*(?:to|\-)\s*" + date_regex + r")",
        text, re.IGNORECASE
    )
    if not match:
        match = re.search(
            r"(" + date_regex + r"\s*(?:to|\-)\s*" + date_regex + r")",
            text, re.IGNORECASE
        )
    data["Statement Period"] = match.group(1).strip() if match else "N/A"

    # 4️⃣ Opening / Previous Balance
    match = re.search(
        r"(?:Your\s*)?(?:Opening|Beginning|Previous)\s*Balance[:\s₹$\.]*([0-9,]+\.\d{2})",
        text, re.IGNORECASE
    )
    data["Opening Balance"] = match.group(1) if match else "N/A"

    # 5️⃣ Closing / Ending / New Balance
    match = re.search(
        r"(?:Your\s*)?(?:Closing|Ending|New)\s*Balance[:\s₹$\.]*([0-9,]+\.\d{2})",
        text, re.IGNORECASE
    )
    data["Closing Balance"] = match.group(1) if match else "N/A"

    return data

# --- Flask Web Routes ---

@app.route('/')
def index():
    """Renders the homepage with the upload form."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload and parsing."""
    if 'pdf_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith('.pdf'):
        try:
            # Pass the file stream directly to the extraction function
            text = extract_text_from_pdf(file.stream)
            
            # Parse the extracted text
            parsed_data = parse_statement(text)
            
            # Render the results page, passing the data to it
            return render_template('results.html', data=parsed_data, filename=file.filename)
        
        except Exception as e:
            # Handle cases where the PDF is scanned, encrypted, or unreadable
            return render_template('results.html', error=f"Error processing {file.filename}: {e}")

    return redirect(request.url)

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True auto-reloads when you save changes