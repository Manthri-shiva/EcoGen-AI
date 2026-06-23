"""
Test script to verify environment configuration for EcoGen AI.

Run this script to check if all required environment variables are set correctly.
"""

import os
import sys
from pathlib import Path

# Try to load .env file
try:
    from dotenv import load_dotenv
    
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Loaded .env file from: {env_path}")
    else:
        print(f"✗ .env file not found at: {env_path}")
except ImportError:
    print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")


def test_gemini_api():
    """Test if Gemini API key is configured."""
    print("\n" + "="*60)
    print("Testing Gemini API Configuration")
    print("="*60)
    
    api_keys = ("GEMINI_API_KEY", "GOOGLE_API_KEY")
    
    for key_name in api_keys:
        api_key = os.getenv(key_name)
        if api_key:
            masked_key = api_key[:8] + "*" * (len(api_key) - 16) + api_key[-8:]
            print(f"✓ {key_name} is set: {masked_key}")
            return True
        else:
            print(f"✗ {key_name} is NOT set")
    
    return False


def test_streamlit_config():
    """Test if Streamlit is importable."""
    print("\n" + "="*60)
    print("Testing Streamlit Configuration")
    print("="*60)
    
    try:
        import streamlit as st
        print(f"✓ Streamlit version: {st.__version__}")
        return True
    except ImportError:
        print("✗ Streamlit not installed. Install with: pip install streamlit")
        return False


def test_ml_imports():
    """Test if ML modules are importable."""
    print("\n" + "="*60)
    print("Testing ML Module Imports")
    print("="*60)
    
    modules_to_test = [
        ("ml.location.location_engine", "Location Engine"),
        ("ml.prediction.predict", "Prediction Engine"),
        ("simulator.carbon_simulator", "Carbon Simulator"),
        ("chatbot.sustainability_advisor", "Sustainability Advisor"),
    ]
    
    results = []
    for module_path, display_name in modules_to_test:
        try:
            __import__(module_path)
            print(f"✓ {display_name} ({module_path}) imported successfully")
            results.append(True)
        except ImportError as e:
            print(f"✗ {display_name} ({module_path}) import failed: {e}")
            results.append(False)
    
    return all(results)


def test_prediction_model():
    """Test if ML prediction model can be loaded."""
    print("\n" + "="*60)
    print("Testing Prediction Model")
    print("="*60)
    
    try:
        from ml.prediction.predict import load_model, MODEL_PATH
        
        if MODEL_PATH.exists():
            print(f"✓ Model file found at: {MODEL_PATH}")
            try:
                model = load_model()
                print(f"✓ Model loaded successfully")
                return True
            except Exception as e:
                print(f"✗ Model loading failed: {e}")
                return False
        else:
            print(f"⚠ Model file not found at: {MODEL_PATH}")
            print("  The ML predictor will not work until the model is trained/added")
            return False
    except Exception as e:
        print(f"✗ Error checking model: {e}")
        return False


def test_location_engine():
    """Test if location engine works."""
    print("\n" + "="*60)
    print("Testing Location Engine")
    print("="*60)
    
    try:
        from ml.location.location_engine import (
            get_location_profile,
            generate_location_insights,
            generate_location_recommendations,
        )
        
        # Test with default city
        test_city = "Hyderabad"
        profile = get_location_profile(test_city)
        insights = generate_location_insights(test_city)
        recommendations = generate_location_recommendations(test_city)
        
        print(f"✓ Location profile for {test_city}:")
        for key, value in profile.items():
            print(f"  - {key}: {value}")
        
        print(f"\n✓ Generated {len(insights)} insights")
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        return True
    except Exception as e:
        print(f"✗ Location engine test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EcoGen AI Environment Test Suite")
    print("="*60)
    
    tests = [
        ("Gemini API", test_gemini_api),
        ("Streamlit", test_streamlit_config),
        ("ML Modules", test_ml_imports),
        ("Location Engine", test_location_engine),
        ("Prediction Model", test_prediction_model),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ {test_name} test encountered error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All systems ready! You can run the app with:")
        print("  streamlit run app/main.py")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
