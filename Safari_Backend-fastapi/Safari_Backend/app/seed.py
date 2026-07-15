#creat admin(To test the user module)
from datetime import datetime, timezone
from app.database import SessionLocal
from app.core.security import get_password_hash
from app.core.modules.users import models

def seed_admin():
    db = SessionLocal()
    try:
        if not db.query(models.Role).filter(models.Role.Id == 1).first():
            db.add_all([
                models.Role(Id=1, Name="Admin"),
                models.Role(Id=2, Name="Airline"),
                models.Role(Id=3, Name="Customer")
            ])
            db.commit()
            print("Roles created successfully.")

        admin_user = db.query(models.User).filter(models.User.RoleId == 1).first()
        if not admin_user:
            hashed_pwd = get_password_hash("admin123456")
            
            new_user = models.User(
                RoleId=1,
                PhoneNumber="09000000000",
                Email="admin@system.com",
                PasswordHash=hashed_pwd,
                IsActive=True,
                IsEmailVerified=True,
                IsPhoneVerified=True,
                CreatedAt=datetime.now(timezone.utc)
            )
            db.add(new_user)
            db.flush() 

            new_admin_profile = models.Admin(
                UserId=new_user.Id,
                FirstName="Super",
                LastName="Admin",
                Gender=0 
            )
            db.add(new_admin_profile)
            db.commit()
            
            print("-------------------------------------------------")
            print("✅ Super Admin created successfully!")
            print("📱 Phone Number : 09000000000")
            print("🔑 Password     : admin123456")
            print("-------------------------------------------------")
        else:
            print("✅ Admin user already exists in the database.")
            
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()