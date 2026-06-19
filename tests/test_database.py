"""
Database Integration Tests for EcoGen AI

End-to-end testing of database operations:
- User management
- Profile management
- Carbon data persistence
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.sqlite.db_manager import DatabaseManager
from database.models.carbon_data import CarbonData
from ml.carbon.carbon_engine import CarbonCalculator
from ml.scoring.scoring_engine import SustainabilityScorer
from ml.profiling.profiling_engine import SustainabilityProfile


def cleanup_test_db():
    """Remove test database if it exists."""
    test_db = "test_ecogen.db"
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
            print(f"[+] Cleaned up {test_db}")
        except Exception as e:
            print(f"[-] Could not clean up: {e}")


def test_database_connection():
    """Test database connection and table creation."""
    print("\n" + "="*60)
    print("TEST 1: Database Connection & Schema")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        print("[+] Database initialized successfully")


def test_user_creation():
    """Test user creation."""
    print("\n" + "="*60)
    print("TEST 2: User Creation")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        user_id = db.insert_user(
            name="John Doe",
            email="john@example.com"
        )
        assert user_id > 0, "User creation failed"
        print(f"[+] User created with ID: {user_id}")


def test_profile_creation_and_retrieval():
    """Test profile creation and retrieval."""
    print("\n" + "="*60)
    print("TEST 3: Profile Creation & Retrieval")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        
        # Create user
        user_id = db.insert_user(
            name="Jane Smith",
            email="jane@example.com"
        )
        
        # Create profile using SustainabilityProfile
        profile_obj = SustainabilityProfile(
            name="Jane Smith",
            age=28,
            location="Mumbai",
            family_size=4,
            electricity_bill=1500,
            water_usage=500,
            vehicle_type="Car",
            daily_travel_km=20,
            waste_generated=30
        )
        
        # Validate profile
        profile_obj.validate_profile()
        print("[+] Profile validation passed")
        
        # Convert to dataclass and insert
        profile_dataclass = profile_obj.to_profile_dataclass(user_id)
        profile_id = db.insert_profile(profile_dataclass)
        assert profile_id > 0, "Profile creation failed"
        print(f"[+] Profile created with ID: {profile_id}")
        
        # Retrieve profile
        retrieved_profile = db.get_profile(user_id)
        assert retrieved_profile is not None, "Profile retrieval failed"
        assert retrieved_profile.user_id == user_id
        assert retrieved_profile.age == 28
        assert retrieved_profile.location == "Mumbai"
        print("[+] Profile retrieved successfully")
        print(f"  - Age: {retrieved_profile.age}")
        print(f"  - Location: {retrieved_profile.location}")
        print(f"  - Family Size: {retrieved_profile.family_size}")


def test_carbon_calculation_and_storage():
    """Test carbon calculation and storage."""
    print("\n" + "="*60)
    print("TEST 4: Carbon Calculation & Storage")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        
        # Create user
        user_id = db.insert_user(
            name="Alice Johnson",
            email="alice@example.com"
        )
        
        # Create and save profile
        profile_obj = SustainabilityProfile(
            name="Alice Johnson",
            age=35,
            location="Delhi",
            family_size=3,
            electricity_bill=2000,
            water_usage=600,
            vehicle_type="SUV",
            daily_travel_km=30,
            waste_generated=50
        )
        
        profile_obj.validate_profile()
        profile_dataclass = profile_obj.to_profile_dataclass(user_id)
        db.insert_profile(profile_dataclass)
        
        # Calculate carbon footprint
        calculator = CarbonCalculator(
            electricity_bill=2000,
            water_usage=600,
            daily_travel_km=30,
            waste_generated=50
        )
        
        energy_emission = calculator.calculate_energy_emission()
        transport_emission = calculator.calculate_transport_emission()
        water_impact = calculator.calculate_water_impact()
        waste_impact = calculator.calculate_waste_impact()
        total_footprint = calculator.calculate_total_footprint()
        
        print(f"[+] Carbon calculations completed:")
        print(f"  - Energy Emission: {energy_emission} kg CO2")
        print(f"  - Transport Emission: {transport_emission} kg CO2")
        print(f"  - Water Impact: {water_impact} kg CO2")
        print(f"  - Waste Impact: {waste_impact} kg CO2")
        print(f"  - Total Footprint: {total_footprint} kg CO2")
        
        # Store carbon result
        carbon_data = CarbonData(
            id=None,
            user_id=user_id,
            electricity_emission=energy_emission,
            transport_emission=transport_emission,
            water_impact=water_impact,
            waste_impact=waste_impact,
            total_carbon_footprint=total_footprint
        )
        
        carbon_id = db.insert_carbon_result(carbon_data)
        assert carbon_id > 0, "Carbon data insertion failed"
        print(f"[+] Carbon data stored with ID: {carbon_id}")


def test_carbon_retrieval_and_scoring():
    """Test carbon data retrieval and sustainability scoring."""
    print("\n" + "="*60)
    print("TEST 5: Carbon Retrieval & Sustainability Scoring")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        
        # Create user
        user_id = db.insert_user(
            name="Bob Wilson",
            email="bob@example.com"
        )
        
        # Create profile
        profile_obj = SustainabilityProfile(
            name="Bob Wilson",
            age=42,
            location="Bangalore",
            family_size=2,
            electricity_bill=1200,
            water_usage=400,
            vehicle_type="Bike",
            daily_travel_km=15,
            waste_generated=20
        )
        
        profile_obj.validate_profile()
        profile_dataclass = profile_obj.to_profile_dataclass(user_id)
        db.insert_profile(profile_dataclass)
        
        # Calculate and store carbon
        calculator = CarbonCalculator(
            electricity_bill=1200,
            water_usage=400,
            daily_travel_km=15,
            waste_generated=20
        )
        
        total_footprint = calculator.calculate_total_footprint()
        
        carbon_data = CarbonData(
            id=None,
            user_id=user_id,
            electricity_emission=calculator.calculate_energy_emission(),
            transport_emission=calculator.calculate_transport_emission(),
            water_impact=calculator.calculate_water_impact(),
            waste_impact=calculator.calculate_waste_impact(),
            total_carbon_footprint=total_footprint
        )
        
        db.insert_carbon_result(carbon_data)
        
        # Retrieve carbon data
        retrieved_carbon = db.get_carbon_result(user_id)
        assert retrieved_carbon is not None, "Carbon data retrieval failed"
        assert retrieved_carbon.user_id == user_id
        assert retrieved_carbon.total_carbon_footprint == total_footprint
        print(f"[+] Carbon data retrieved: {retrieved_carbon.total_carbon_footprint} kg CO2")
        
        # Score sustainability
        scorer = SustainabilityScorer(retrieved_carbon.total_carbon_footprint)
        overall_score = scorer.overall_score()
        
        print(f"[+] Sustainability scores calculated:")
        print(f"  - Energy Score: {scorer.energy_score()}")
        print(f"  - Water Score: {scorer.water_score()}")
        print(f"  - Waste Score: {scorer.waste_score()}")
        print(f"  - Transport Score: {scorer.transport_score()}")
        print(f"  - Overall Score: {overall_score}")


def test_end_to_end_workflow():
    """Test complete end-to-end workflow."""
    print("\n" + "="*60)
    print("TEST 6: End-to-End Workflow")
    print("="*60)
    
    cleanup_test_db()
    
    with DatabaseManager("test_ecogen.db") as db:
        db.create_tables()
        print("[+] Step 1: Database initialized")
        
        # Step 1: Create User
        user_id = db.insert_user(
            name="Emma Davis",
            email="emma@example.com"
        )
        print(f"[+] Step 2: User created (ID: {user_id})")
        
        # Step 2: Create Profile
        profile_obj = SustainabilityProfile(
            name="Emma Davis",
            age=26,
            location="Chennai",
            family_size=3,
            electricity_bill=1800,
            water_usage=550,
            vehicle_type="Car",
            daily_travel_km=25,
            waste_generated=35
        )
        profile_obj.validate_profile()
        print("[+] Step 3: Profile created and validated")
        
        # Step 3: Save Profile
        profile_dataclass = profile_obj.to_profile_dataclass(user_id)
        profile_id = db.insert_profile(profile_dataclass)
        print(f"[+] Step 4: Profile saved (ID: {profile_id})")
        
        # Step 4: Retrieve Profile
        retrieved_profile = db.get_profile(user_id)
        assert retrieved_profile is not None
        print(f"[+] Step 5: Profile retrieved from database")
        
        # Step 5: Calculate Carbon Footprint
        calculator = CarbonCalculator(
            electricity_bill=retrieved_profile.electricity_bill,
            water_usage=retrieved_profile.water_usage,
            daily_travel_km=retrieved_profile.daily_travel_km,
            waste_generated=retrieved_profile.waste_generated
        )
        total_footprint = calculator.calculate_total_footprint()
        print(f"[+] Step 6: Carbon footprint calculated: {total_footprint} kg CO2")
        
        # Step 6: Save Carbon Result
        carbon_data = CarbonData(
            id=None,
            user_id=user_id,
            electricity_emission=calculator.calculate_energy_emission(),
            transport_emission=calculator.calculate_transport_emission(),
            water_impact=calculator.calculate_water_impact(),
            waste_impact=calculator.calculate_waste_impact(),
            total_carbon_footprint=total_footprint
        )
        carbon_id = db.insert_carbon_result(carbon_data)
        print(f"[+] Step 7: Carbon result saved (ID: {carbon_id})")
        
        # Step 7: Retrieve Carbon Result
        retrieved_carbon = db.get_carbon_result(user_id)
        assert retrieved_carbon is not None
        print(f"[+] Step 8: Carbon result retrieved from database")
        
        # Final: Score sustainability
        scorer = SustainabilityScorer(retrieved_carbon.total_carbon_footprint)
        overall_score = scorer.overall_score()
        print(f"[+] Step 9: Sustainability score calculated: {overall_score}")
        
        print("\n" + "="*60)
        print("WORKFLOW COMPLETE [+]")
        print("="*60)


def run_all_tests():
    """Run all database tests."""
    print("\n" + "="*70)
    print(" ECOGEN AI - DATABASE INTEGRATION TEST SUITE")
    print("="*70)
    
    try:
        test_database_connection()
        test_user_creation()
        test_profile_creation_and_retrieval()
        test_carbon_calculation_and_storage()
        test_carbon_retrieval_and_scoring()
        test_end_to_end_workflow()
        
        print("\n" + "="*70)
        print(" ALL TESTS PASSED [OK]")
        print("="*70)
        
    except Exception as e:
        print(f"\n[-] TEST FAILED: {e}")
        raise
    finally:
        cleanup_test_db()


if __name__ == "__main__":
    run_all_tests()
