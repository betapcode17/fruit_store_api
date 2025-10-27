class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True)
    address = Column(String(255))
    moneySpent = Column(DECIMAL(10, 2), default=0)
    admin = Column(String(100))
