#!/usr/bin/env python3
"""
Test script to validate the session metrics system using existing reports
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_metrics_with_existing_reports():
    """Test metrics computation with existing reports"""
    
    reports_dir = Path("reports")
    if not reports_dir.exists():
        print("❌ No reports directory found. Run some tests first.")
        return
    
    # Find evaluation reports
    eval_files = list(reports_dir.glob("evaluation_*.json"))
    
    if not eval_files:
        print("❌ No evaluation reports found. Run some tests first.")
        return
    
    print(f"📊 Found {len(eval_files)} evaluation reports. Testing metrics system...")
    
    # Test with the first report
    test_file = eval_files[0]
    print(f"🧪 Testing with: {test_file}")
    
    try:
        from compute_session_metrics import compute_metrics_from_file
        
        # Compute metrics without uploading (for testing)
        metrics = compute_metrics_from_file(
            file_path=str(test_file),
            upload=False  # Don't upload during testing
        )
        
        print("\n✅ Test successful! Computed metrics:")
        print(f"   Session ID: {metrics.session_id}")
        print(f"   User Type: {metrics.user_type}")
        print(f"   Concepts Covered: {metrics.num_concepts_covered}")
        print(f"   Quiz Score: {metrics.quiz_score:.1f}%")
        print(f"   Engagement: {metrics.user_engagement_rating:.1f}/5")
        print(f"   Interest: {metrics.user_interest_rating:.1f}/5")
        print(f"   Enjoyment: {metrics.enjoyment_probability:.0%}")
        
        # Save test results
        test_output = reports_dir / f"test_metrics_{metrics.session_id}.json"
        with open(test_output, 'w') as f:
            json.dump(metrics.model_dump(), f, indent=2)
        
        print(f"\n💾 Test metrics saved to: {test_output}")
        print("🎉 Session metrics system is working correctly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"Metrics test failed: {e}") from e


def test_langfuse_upload():
    """Test uploading metrics to Langfuse"""
    
    print("\n🔄 Testing Langfuse upload...")
    
    try:
        from tester_agent.session_metrics import MetricsComputer, SessionMetrics
        
        # Create a simple test metrics object
        test_metrics = SessionMetrics(
            concepts_covered=["simple pendulum", "oscillation"],
            num_concepts_covered=2,
            quiz_score=85.0,
            clarity_conciseness_score=4.2,
            error_handling_count=1,
            user_type="Medium",
            user_interest_rating=4.0,
            user_engagement_rating=3.8,
            average_response_time=45.0,
            adaptability=True,
            enjoyment_probability=0.75,
            session_id="test_session_metrics_validation",
            total_interactions=8,
            session_duration=20.5,
            persona_name="test_persona"
        )
        
        # Try to upload
        computer = MetricsComputer()
        success = computer.upload_to_langfuse(test_metrics)
        
        if success:
            print("✅ Langfuse upload test successful!")
        else:
            print("⚠️ Langfuse upload test failed (check API keys and connection)")
            
    except Exception as e:
        print(f"❌ Langfuse upload test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🧪 Testing Session Metrics System")
    print("=" * 40)
    
    test_metrics_with_existing_reports()
    test_langfuse_upload()
    
    print("\n🏁 Testing complete!")
