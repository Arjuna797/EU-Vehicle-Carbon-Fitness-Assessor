"""
This module defines the core business logic: the emission standards
and the function to check a vehicle's fitness against them.
"""

# NOTE: These are simplified, representative thresholds for demonstration.
# Real EU standards are more complex, often based on fleet-wide averages
# or vehicle weight (e.g., for Euro 6).
EU_STANDARDS_G_PER_KM = {
    "Car": 95,  # Based on the 2021 fleet-wide average target for new passenger cars (Regulation (EU) 2019/631).
    "Motorcycle": 100, # Representative of Euro 5 standards for motorcycles.
    "Truck": 750, # This is a heavily simplified g/km value. Real trucks are measured in g/t-km (grams per tonne-kilometer).
}

def check_fitness(vehicle_type: str, carbon_footprint_g_km: float) -> (bool, float):
    """
    Checks if a vehicle meets the simplified EU standard for its category.

    Args:
        vehicle_type (str): The category ("Car", "Truck", "Motorcycle").
        carbon_footprint_g_km (float): The vehicle's CO2 emissions in g/km.

    Returns:
        tuple: (is_fit, threshold)
            is_fit (bool): True if the vehicle is at or below the standard, False otherwise.
            threshold (float): The emission standard (g/km) for that vehicle type.
    """
    if vehicle_type not in EU_STANDARDS_G_PER_KM:
        raise ValueError("Invalid vehicle type specified.")
        
    threshold = EU_STANDARDS_G_PER_KM[vehicle_type]
    
    is_fit = carbon_footprint_g_km <= threshold
    
    return is_fit, threshold
