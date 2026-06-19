from database.models.profile import Profile


class SustainabilityProfile:

    def __init__(
        self,
        name,
        age,
        location,
        family_size,
        electricity_bill,
        water_usage,
        vehicle_type,
        daily_travel_km,
        waste_generated
    ):
        self.name = name
        self.age = age
        self.location = location
        self.family_size = family_size
        self.electricity_bill = electricity_bill
        self.water_usage = water_usage
        self.vehicle_type = vehicle_type
        self.daily_travel_km = daily_travel_km
        self.waste_generated = waste_generated

    def validate_profile(self):

        if self.age <= 0:
            raise ValueError("Age must be positive")

        if self.family_size <= 0:
            raise ValueError("Family size must be positive")

        if self.electricity_bill < 0:
            raise ValueError("Electricity bill cannot be negative")

        return True

    def get_profile(self):

        return {
            "name": self.name,
            "age": self.age,
            "location": self.location,
            "family_size": self.family_size,
            "electricity_bill": self.electricity_bill,
            "water_usage": self.water_usage,
            "vehicle_type": self.vehicle_type,
            "daily_travel_km": self.daily_travel_km,
            "waste_generated": self.waste_generated
        }

    def to_dict(self):
        """
        Serialize profile to dictionary.
        
        Returns:
            Dictionary containing all profile attributes
        """
        return self.get_profile()

    def to_profile_dataclass(self, user_id: int, profile_id: int | None = None) -> Profile:
        """
        Convert to Profile dataclass for database operations.
        
        Args:
            user_id: ID of the associated user
            profile_id: Optional profile ID (if updating existing profile)
            
        Returns:
            Profile dataclass instance
        """
        return Profile(
            id=profile_id,
            user_id=user_id,
            age=self.age,
            location=self.location,
            family_size=self.family_size,
            electricity_bill=self.electricity_bill,
            water_usage=self.water_usage,
            vehicle_type=self.vehicle_type,
            daily_travel_km=self.daily_travel_km,
            waste_generated=self.waste_generated
        )

    @classmethod
    def from_dict(cls, data: dict) -> "SustainabilityProfile":
        """
        Create SustainabilityProfile from dictionary.
        
        Args:
            data: Dictionary containing profile data
            
        Returns:
            SustainabilityProfile instance
        """
        return cls(
            name=data.get("name"),
            age=data.get("age"),
            location=data.get("location"),
            family_size=data.get("family_size"),
            electricity_bill=data.get("electricity_bill"),
            water_usage=data.get("water_usage"),
            vehicle_type=data.get("vehicle_type"),
            daily_travel_km=data.get("daily_travel_km"),
            waste_generated=data.get("waste_generated")
        )