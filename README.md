# Credit_Card_Statement_Parser_SURE_TASK

This is simple Flask Web application that parses PDF bank and credit card statements. This project is a task for SURE.finance company.


![UI](Screenshot%202025-10-23%20103541.png)
![Result](Screenshot%202025-10-23%20101943.png)


## Features
 
- Simple Web UI : Clean interface to upload a file and extract the result.

- Flexible Parsing: The regex-based approach is designed to handle multiple bank statement formats (e.g., Chase, Amex, HDFC, SBI, Citi).

- Pure Python: Relies only on Python libraries, making installation simple across all operating systems.

## Tech Stack
| Category        | Technology / Tool   | Purpose                                                                 |
|-----------------|------------------|-------------------------------------------------------------------------|
| Backend         | Python 3 / Flask  | A lightweight web framework to build the server, handle file uploads, and render HTML. |
| PDF Parsing     | pdfplumber        | Pure-Python library to extract text from digital PDF files without external binaries. |
| OCR             | Tesseract         | Optical Character Recognition engine to extract text from images or scanned PDFs. |
| PDF Rendering   | Poppler           | A PDF rendering library used to convert PDF pages to images for OCR.    |
| Data Extraction | re (Python Regex) | Used to find and parse the required data points (Name, Account No., etc.) from the raw text. |
| Frontend        | HTML / CSS        | Used to build the upload form and the results page.                     |


## How It Works

1. Upload PDF: User uploads a PDF via the web form.

2. In-Memory Processing: File is read in memory to ensure privacy.

3. Text Extraction: pdfplumber (or Tesseract for scanned PDFs) extracts the text.

4. Regex Parsing: Python regex finds the key data points.

5. Display Results: Data is shown neatly in an HTML table.


## Python Regex Output in Terminal
![Regex](Screenshot%202025-10-23%20095448.png)

## Statements Folder 

-  This folder contains the sample pdf credit card statement like AMERICAN_EXPRESS.pdf , HDFC.pdf , etc

## Made by JAINAM BHEDA 
