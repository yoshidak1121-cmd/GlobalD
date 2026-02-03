"""Database models for GlobalD."""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Machine(Base):
    """Machine model with searchable fields."""
    
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_model = Column(String, index=True)
    machine_serial = Column(String, index=True)
    maker = Column(String, index=True)
    nc_model = Column(String, index=True)
    contract_number = Column(String, index=True)
    end_user = Column(String, index=True)
    install_country = Column(String, index=True)
    service_base = Column(String, index=True)
    
    def to_dict(self):
        """Convert model to dictionary for API response."""
        return {
            "id": self.id,
            "machine_model": self.machine_model,
            "machine_serial": self.machine_serial,
            "maker": self.maker,
            "nc_model": self.nc_model,
            "contract_number": self.contract_number,
            "end_user": self.end_user,
            "install_country": self.install_country,
            "service_base": self.service_base,
        }


# Database setup
DATABASE_URL = "sqlite:///./globald.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database with schema."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
