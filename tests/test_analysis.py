
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
    analyzer = AnalysisEngine(threshold=500)
    data = [500, 600, 900, 1000]
    results = analyzer.analyze_with_severity(data)

    assert results[0]['severity'] == 'low'       # 500 -> 0% excess
    assert results[1]['severity'] == 'moderate'  # 600 -> 20% excess
    assert results[2]['severity'] == 'critical'  # 900 -> 80% excess
    assert results[3]['severity'] == 'critical'  # 1000 -> 100% excess
