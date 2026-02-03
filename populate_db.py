"""Script to populate database with sample machine data."""
from models import SessionLocal, init_db, Machine


def populate_sample_data():
    """Populate database with sample machine data."""
    init_db()
    
    db = SessionLocal()
    
    # Clear existing data
    db.query(Machine).delete()
    
    # Sample machine data
    sample_machines = [
        Machine(
            machine_model="CNC-1000X",
            machine_serial="SN-2023-001",
            maker="Makino",
            nc_model="FANUC 31i-B5",
            contract_number="CT-2023-0045",
            end_user="Toyota Manufacturing",
            install_country="Japan",
            service_base="Tokyo Service Center"
        ),
        Machine(
            machine_model="CNC-2000Y",
            machine_serial="SN-2023-002",
            maker="DMG MORI",
            nc_model="FANUC 32i-B",
            contract_number="CT-2023-0046",
            end_user="Honda Motor Co.",
            install_country="Japan",
            service_base="Osaka Service Center"
        ),
        Machine(
            machine_model="CNC-3000Z",
            machine_serial="SN-2023-003",
            maker="Okuma",
            nc_model="OSP-P300M",
            contract_number="CT-2023-0047",
            end_user="Boeing",
            install_country="USA",
            service_base="Seattle Service Center"
        ),
        Machine(
            machine_model="CNC-1500A",
            machine_serial="SN-2023-004",
            maker="Makino",
            nc_model="FANUC 31i-B5",
            contract_number="CT-2023-0048",
            end_user="Airbus",
            install_country="France",
            service_base="Toulouse Service Center"
        ),
        Machine(
            machine_model="CNC-2500B",
            machine_serial="SN-2023-005",
            maker="Haas",
            nc_model="Haas NGC",
            contract_number="CT-2023-0049",
            end_user="General Electric",
            install_country="USA",
            service_base="Boston Service Center"
        ),
        Machine(
            machine_model="CNC-3500C",
            machine_serial="SN-2024-001",
            maker="DMG MORI",
            nc_model="FANUC 32i-B",
            contract_number="CT-2024-0001",
            end_user="Volkswagen",
            install_country="Germany",
            service_base="Berlin Service Center"
        ),
        Machine(
            machine_model="CNC-4000D",
            machine_serial="SN-2024-002",
            maker="Mazak",
            nc_model="MAZATROL Matrix 2",
            contract_number="CT-2024-0002",
            end_user="Tesla",
            install_country="USA",
            service_base="Austin Service Center"
        ),
        Machine(
            machine_model="CNC-4500E",
            machine_serial="SN-2024-003",
            maker="Okuma",
            nc_model="OSP-P300L",
            contract_number="CT-2024-0003",
            end_user="Nissan",
            install_country="Japan",
            service_base="Yokohama Service Center"
        ),
    ]
    
    # Add all sample machines
    for machine in sample_machines:
        db.add(machine)
    
    db.commit()
    print(f"Successfully added {len(sample_machines)} sample machines to the database.")
    db.close()


if __name__ == "__main__":
    populate_sample_data()
