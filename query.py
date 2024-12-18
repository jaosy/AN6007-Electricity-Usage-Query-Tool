"""
This program allows users to query average electricity consumption data per month for a particular year, region, and dwelling type. It continues to prompt for input until the user enters '-' for the year selection.

Author: Jacqueline Ong
Date: 12/17/2024
"""

from complete import get_electricity_data
from models import ElectricityRecord


dwelling_types = {
    1: '1-room / 2-room',
    2: 'Private Apartments and Condominiums',
    3: 'Landed Properties',
    4: '5-room and Executive',
    5: '3-room',
    6: '4-room'
}


regions = {
    1: "Central Region",
    2: "North Region",
    3: "West Region",
    4: "North East Region",
    5: "East Region"
}


def get_int_from_input(prompt):
    """
    Helper function to get and validate integer input from user. 
    
    Parameters:
        prompt (str): Input prompt from program

    Returns:
        int: The input cast as an int
        None: If user enters '-' for year prompt.
    """
    while True:
        try:
            value = input(prompt).strip()
            if 'year' in prompt.lower() and value == '-':
                return None
            num = int(value)
            return num
        except ValueError:
            print("Please enter a valid number")


def validate_year(year_input):
    """
    Validates if the year is within acceptable range
    
    Parameters:
        year_input (int): Validated year input

    Returns:
        int: If the year is within the valid range of the dataset
        None: If the year is outside of the valid range of the dataset or is None
    """
    return 2010 <= year_input <= 2023 if year_input is not None else None


def validate_region(region_input):
    """
    Validates if the input region is within the known regions
    
    Parameters:
        region_input (int): Region input

    Returns:
        str: The name of the region, if recognized
        False: If the region's code is not in the dictionary
    """
    if region_input in regions:
        return regions[region_input]
    
    return False


def validate_dwelling_type(dwelling_type_input):
    """
    Validates if the input dwelling type is within the known dwelling types
    
    Parameters:
        dwelling_type_input (int): Dwelling type input

    Returns:
        str: The name of the dwelling type, if recognized
        False: If the dwelling type's code is not in the dictionary
    """
    if dwelling_type_input in dwelling_types:
        return dwelling_types[dwelling_type_input]
    
    return False


def find_matching_records(data, year, region, dwelling_type):
    """
    Finds and returns matching records based on user input

    Parameters:
        data ([ElectricityRecords]): List of ELectricityRecord objects
        year (int)
        region (str)
        dwelling_type (str)
    
    Returns:
        [ElectricityRecords]: List of ElectricityRecord objects matching user search filters
    """
    matching_records = [
        record for record in data 
        if record.year == year and 
            record.region == region and 
            record.dwelling_type == dwelling_type
    ]
        
    print(f"Found {len(matching_records)} matching records.")
    return matching_records


def display_results(records, chosen_year, chosen_region, chosen_dwelling_type):
    """
    Displays the matching records

    Parameters:
        records ([ElectricityRecords]): List of ElectricityRecord objects matching user search filters
        chosen_year (int)
        chosen_region (str)
        chosen_dwelling_type (str)

    Returns:
        None (prints output)
    """
    # print header info
    print(f"Monthly Electricity Consumption for {chosen_year}")
    print(f"Region: {chosen_region}")
    print(f"Dwelling Type: {chosen_dwelling_type}")
    print('\n')

    if not records:
        print("\nNo matching records found.")
        return

    # group records by area over month
    area_groupings = {}
    for record in records:
        if record.area not in area_groupings:
            area_groupings[record.area] = {}
        print(record.avg_kwh_per_acc)
        area_groupings[record.area][record.month] = record.avg_kwh_per_acc
    
    # print 'table' header
    print("Area".ljust(20), end="")
    for month in range(1, 13):
        print(f"{month:>8}", end="")
    print()
    print("-" * 116)

    for area in sorted(area_groupings.keys()):
        print(f"{area:<20}", end="")
        for month in range(1, 13):
            value = area_groupings[area].get(str(month))
            if value is None:
                print(f"{'':>8}", end="")
            else:
                print(f"{value:>8.2f}", end="")
        print()


def menu():
    """
    Main function that handles user input and program flow

    Parameters:
        None

    Returns:
        None
    """
    # get denormalized dataset as list of ElectricityRecord objects
    merged_data = get_electricity_data()

    while True:
        print("\n" + "="*50)
        print("Electricity Usage Query System")
        print("="*50)

        # Get year input
        year = get_int_from_input("\nPlease enter a year from 2010 - 2023 (inclusive) or '-' to exit: ")
        if year is None:
            print("\nThank you for using the system. Goodbye!")
            break

        if not validate_year(year):
            print("Invalid year. Please enter a year between 2010 and 2023.")
            continue

        # prompt for region until valid input received
        while True:
            region_choices = """
            1: Central Region        2: North Region          3: West Region           
            4: North East Region     5: East Region         
            """
            print(region_choices)
            region_input = get_int_from_input("Please select a region (enter its numerical code) :")

            region_name = validate_region(region_input)

            if region_name:
                break
            else:
                print("Invalid region code. Please try again.")

        # prompt for dwelling type until valid input received
        while True:
            dwelling_type_choices = """
            1: 1-room / 2-room
            2: Private Apartments and Condominiums
            3: Landed Properties
            4: 5-room and Executive
            5: 3-room
            6: 4-room
            """
            print(dwelling_type_choices)
            dwelling_type_input = get_int_from_input("Please enter the dwelling type code: ")

            dwelling_type = validate_dwelling_type(dwelling_type_input)

            if dwelling_type: 
                break
            else:
                print("Invalid dwelling type code. Please try again.")

        # find and display matching records
        matching_records = find_matching_records(merged_data, year, region_name, dwelling_type)
        display_results(matching_records, year, region_name, dwelling_type)


if __name__ == "__main__":
    menu()