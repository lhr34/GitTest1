from app.analysis import AnalysisEngine

def test_threshold_analysis():
    analyzer = AnalysisEngine(threshold=500)
    data = [400, 550, 700, 300]
    alerts = analyzer.analyze(data)
    assert alerts == [550, 700]  # 验证阈值检测

def test_severity_classification():
    analyzer = AnalysisEngine(threshold=500)
    data = [500, 600, 900, 1000]
    results = analyzer.analyze_with_severity(data)
    assert results[1]['severity'] == 'moderate'
    assert results[2]['severity'] == 'critical'