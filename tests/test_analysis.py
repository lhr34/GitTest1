
"""
Analysis Engine Tests:
- Threshold alerts for values exceeding 500
- Severity classification (moderate/critical) based on thresholds
"""
from app.analysis import AnalysisEngine  # Import the class responsible for analyzing data

# Test that the analyzer correctly identifies values above the threshold
def test_threshold_analysis():
    analyzer = AnalysisEngine(threshold=500)  # Initialize the analysis engine with a threshold
    data = [400, 550, 700, 300]  # Sample data
    alerts = analyzer.analyze(data)  # Run threshold analysis
    assert alerts == [550, 700]  # Only values above 500 should be returned

# Test that the analyzer classifies severity correctly based on thresholds
def test_severity_classification():
    analyzer = AnalysisEngine(threshold=500)  # Same threshold for consistency
    data = [500, 600, 900, 1000]  # Test data
    results = analyzer.analyze_with_severity(data)  # Analyze data with severity levels

    # Check the severity of individual results
    assert results[1]['severity'] == 'moderate'  # 600 should be classified as 'moderate'
    assert results[2]['severity'] == 'critical'  # 900 should be classified as 'critical'
