#!/usr/bin/env python3
"""
SRLP Framework - Run Evaluation with PDF Report Generation
Combines framework evaluation with automatic PDF report generation.
"""

import os
import sys
import argparse
from typing import List, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_demo import run_comprehensive_demo
from generate_pdf_report import SRLPReportGenerator

# Optional import for visualizations
try:
    from create_comprehensive_visualizations import main as create_visualizations
    VISUALIZATIONS_AVAILABLE = True
except ImportError:
    VISUALIZATIONS_AVAILABLE = False
    create_visualizations = None


def run_evaluation_with_pdf_report(scenarios: Optional[List[str]] = None,
                                  provider: str = "mock",
                                  model: Optional[str] = None,
                                  output_dir: str = "./output",
                                  report_name: str = "srlp_report.pdf",
                                  include_visualizations: bool = True) -> str:
    """
    Run complete SRLP evaluation and generate PDF report.
    
    Args:
        scenarios: List of scenarios to evaluate (default: all)
        provider: LLM provider to use
        model: Specific model name
        output_dir: Directory for output files
        report_name: Name of the PDF report file
        include_visualizations: Whether to generate visualizations first
        
    Returns:
        Path to generated PDF report
    """
    print("🚀 SRLP Framework - Evaluation with PDF Report Generation")
    print("=" * 70)
    
    # Step 1: Run comprehensive demo/evaluation
    print("\n📊 Step 1: Running SRLP Framework Evaluation...")
    try:
        if scenarios:
            print(f"   🎯 Scenarios: {', '.join(scenarios)}")
        else:
            print("   🎯 Scenarios: All available scenarios")
        print(f"   🤖 Provider: {provider}")
        if model:
            print(f"   🧠 Model: {model}")
        
        # Run the comprehensive demo
        run_comprehensive_demo()
        print("   ✅ Evaluation completed successfully")
        
    except Exception as e:
        print(f"   ❌ Evaluation failed: {e}")
        return None
    
    # Step 2: Generate visualizations (if requested and available)
    if include_visualizations:
        print("\n📈 Step 2: Generating Comprehensive Visualizations...")
        if VISUALIZATIONS_AVAILABLE:
            try:
                create_visualizations()
                print("   ✅ Visualizations generated successfully")
            except Exception as e:
                print(f"   ⚠️  Visualization generation failed: {e}")
                print("   📄 Proceeding with PDF report generation...")
        else:
            print("   ⚠️  Visualization dependencies not available (seaborn missing)")
            print("   📄 Proceeding with PDF report generation...")
    
    # Step 3: Generate PDF report
    print("\n📄 Step 3: Generating PDF Report...")
    try:
        # Create report generator
        generator = SRLPReportGenerator(output_dir=output_dir)
        
        # Generate the report
        report_path = generator.generate_report(
            results_dir="./results",
            output_filename=report_name
        )
        
        print(f"   ✅ PDF report generated: {report_path}")
        return report_path
        
    except Exception as e:
        print(f"   ❌ PDF generation failed: {e}")
        return None


def main():
    """
    Main CLI interface for evaluation with PDF report generation.
    """
    parser = argparse.ArgumentParser(
        description='SRLP Framework - Evaluation with PDF Report Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete evaluation with PDF report
  python run_with_pdf_report.py
  
  # Specify custom output directory and report name
  python run_with_pdf_report.py --output-dir ./reports --report-name my_srlp_report.pdf
  
  # Run with specific provider (when API keys available)
  python run_with_pdf_report.py --provider openai --model gpt-4
  
  # Skip visualization generation
  python run_with_pdf_report.py --no-visualizations
"""
    )
    
    parser.add_argument('--scenarios', nargs='+', 
                       help='Specific scenarios to evaluate')
    parser.add_argument('--provider', default='mock',
                       help='LLM provider to use (default: mock)')
    parser.add_argument('--model', 
                       help='Specific model name')
    parser.add_argument('--output-dir', default='./output',
                       help='Output directory for PDF report (default: ./output)')
    parser.add_argument('--report-name', default='srlp_report.pdf',
                       help='Name of the PDF report file (default: srlp_report.pdf)')
    parser.add_argument('--no-visualizations', action='store_true',
                       help='Skip visualization generation')
    
    args = parser.parse_args()
    
    # Run evaluation with PDF report
    report_path = run_evaluation_with_pdf_report(
        scenarios=args.scenarios,
        provider=args.provider,
        model=args.model,
        output_dir=args.output_dir,
        report_name=args.report_name,
        include_visualizations=not args.no_visualizations
    )
    
    if report_path:
        print("\n" + "=" * 70)
        print("🎉 EVALUATION AND REPORT GENERATION COMPLETE!")
        print("=" * 70)
        print(f"📄 PDF Report: {report_path}")
        print(f"📁 Output Directory: {args.output_dir}")
        print("\n📋 Report Contents:")
        print("   • Executive Summary with Key Findings")
        print("   • Detailed Performance Metrics Table")
        print("   • Comprehensive Visualizations and Charts")
        print("   • Scenario-based Analysis")
        print("   • Academic Conclusions and Recommendations")
        print("\n🎓 Ready for Academic Submission!")
        print("   The PDF report is formatted for thesis documentation,")
        print("   academic review, and professional presentation.")
    else:
        print("\n❌ Report generation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()