from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = "Roles"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(200), nullable=False)

    # one-to-many
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    RoleId = Column(Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=False)
    PhoneNumber = Column(String(11), nullable=False)
    Email = Column(String(200), nullable=True)
    PasswordHash = Column(String(1000), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=True)
    IsEmailVerified = Column(Boolean, nullable=False, default=False)
    IsPhoneVerified = Column(Boolean, nullable=False, default=False)
    CreatedAt = Column(DateTime(timezone=True), nullable=False)
    UpdatedAt = Column(DateTime(timezone=True), nullable=True)
    LastLoginAt = Column(DateTime(timezone=True), nullable=True)
    ImageUrl = Column(String(1000), nullable=True)

    
    role = relationship("Role", back_populates="users")
    customer = relationship("Customer", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    airline = relationship("Airline", back_populates="user", uselist=False)  


class Customer(Base):
    __tablename__ = "Customers"

    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="CASCADE"), primary_key=True)
    FirstName = Column(String(200), nullable=False)
    LastName = Column(String(200), nullable=False)
    BirthDate = Column(Date, nullable=True)
    Gender = Column(Integer, nullable=False)

    user = relationship("User", back_populates="customer")


class Admin(Base):
    __tablename__ = "Admins"

    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="CASCADE"), primary_key=True)
    FirstName = Column(String(200), nullable=False)
    LastName = Column(String(200), nullable=False)
    BirthDate = Column(Date, nullable=True)
    Gender = Column(Integer, nullable=False)

    user = relationship("User", back_populates="admin")


class Airline(Base):
    __tablename__ = "Airlines"

    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="CASCADE"), primary_key=True)
    CompanyName = Column(String(200), nullable=False)

    user = relationship("User", back_populates="airline")