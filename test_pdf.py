#!/usr/bin/env python3
"""
Simple test script for PDF report generation.
"""

import os
import sys
from generate_pdf_report import SRLPReportGenerator

def test_pdf_generation():
    print("Testing PDF generation...")
    
    # Create output directory
    os.makedirs('./output', exist_ok=True)
    
    try:
        # Create report generator
        gen = SRLPReportGenerator('./output')
        
        # Generate report
        path = gen.generate_report('./results', 'test_report.pdf')
        
        print(f"SUCCESS: Report generated at {path}")
        
        # Check if file exists
        if os.path.exists(path):
            file_size = os.path.getsize(path)
            print(f"File size: {file_size} bytes")
        else:
            print("ERROR: File was not created")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()