from app import create_app, db
from app.repositories.user_repo import (
    get_role_by_name, create_role,
    get_user_by_email, create_user
)

app = create_app()

with app.app_context():
    print("Seeding database...")

    # Create roles
    ceo_role = get_role_by_name("CEO")
    if not ceo_role:
        ceo_role = create_role("CEO", "Chief Executive Officer - Full access")
        print("Created role: CEO")

    hr_role = get_role_by_name("HR")
    if not hr_role:
        hr_role = create_role("HR", "HR Manager - Data upload access")
        print("Created role: HR")

    # Create CEO user
    if not get_user_by_email("ceo@smartmart.com"):
        create_user(
            full_name="SmartMart CEO",
            email="ceo@smartmart.com",
            password="Ceo@1234",
            role_id=ceo_role.id
        )
        print("Created CEO: ceo@smartmart.com | Password: Ceo@1234")

    # Create HR user
    if not get_user_by_email("hr@smartmart.com"):
        create_user(
            full_name="SmartMart HR",
            email="hr@smartmart.com",
            password="Hr@1234",
            role_id=hr_role.id
        )
        print("Created HR: hr@smartmart.com | Password: Hr@1234")

    print("Seeding complete!")