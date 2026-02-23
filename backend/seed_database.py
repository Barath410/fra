"""Database seed script for VanAdhikar Drishti"""
import sys
import os
from datetime import date, datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine
from app.models.fra_models import (
    Base, FRAClaim, Village, Officer, DSSRecommendation,
    Grievance, SchemeEnrollment, ClaimStatus, ClaimType
)


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def seed_villages():
    """Seed village data"""
    db = SessionLocal()
    print("\nSeeding villages...")
    
    villages_data = [
        {"code": "MP-D01-V001", "name": "Bichhiya", "state": "MP", "district": "Mandla", "block": "Bichhiya",
         "total_households": 234, "tribal_households": 198, "total_population": 1156, "tribal_population": 982,
         "school_distance_km": 2.3, "ndvi_score": 0.72, "groundwater_depth_m": 15.4},
        
        {"code": "MP-D01-V002", "name": "Motinala", "state": "MP", "district": "Mandla", "block": "Nainpur",
         "total_households": 187, "tribal_households": 145, "total_population": 923, "tribal_population": 718,
         "school_distance_km": 5.8, "ndvi_score": 0.68, "groundwater_depth_m": 22.1},
        
        {"code": "OD-D02-V001", "name": "Karlapat", "state": "OD", "district": "Kalahandi", "block": "Thuamul Rampur",
         "total_households": 312, "tribal_households": 267, "total_population": 1543, "tribal_population": 1321,
         "school_distance_km": 3.2, "ndvi_score": 0.75, "groundwater_depth_m": 18.7},
        
        {"code": "TR-D03-V001", "name": "Takarjala", "state": "TR", "district": "West Tripura", "block": "Bishalgarh",
         "total_households": 156, "tribal_households": 89, "total_population": 771, "tribal_population": 441,
         "school_distance_km": 1.8, "ndvi_score": 0.81, "groundwater_depth_m": 12.3},
        
        {"code": "TG-D04-V001", "name": "Utnoor", "state": "TG", "district": "Adilabad", "block": "Utnoor",
         "total_households": 289, "tribal_households": 234, "total_population": 1432, "tribal_population": 1158,
         "school_distance_km": 4.5, "ndvi_score": 0.69, "groundwater_depth_m": 28.9},
    ]
    
    for v_data in villages_data:
        village = Village(**v_data)
        db.add(village)
    
    db.commit()
    print(f"✓ Seeded {len(villages_data)} villages")
    db.close()


def seed_officers():
    """Seed officer data"""
    db = SessionLocal()
    print("\nSeeding officers...")
    
    officers_data = [
        {"code": "OFF-MP-001", "name": "Rajesh Kumar Sharma", "designation": "District Collector",
         "role": "district-collector", "state": "MP", "district": "Mandla",
         "email": "rajesh.sharma@mp.gov.in", "mobile": "9876543210"},
        
        {"code": "OFF-MP-002", "name": "Priya Singh", "designation": "SDLC Officer",
         "role": "sdlc-officer", "state": "MP", "district": "Mandla",
         "email": "priya.singh@mp.gov.in", "mobile": "9876543211"},
        
        {"code": "OFF-OD-001", "name": "Santosh Patra", "designation": "State Commissioner",
         "role": "state-commissioner", "state": "OD", "district": None,
         "email": "santosh.patra@odisha.gov.in", "mobile": "9876543212"},
        
        {"code": "OFF-TR-001", "name": "Biplab Deb Roy", "designation": "Range Officer",
         "role": "range-officer", "state": "TR", "district": "West Tripura", "block": "Bishalgarh",
         "email": "biplab.roy@tripura.gov.in", "mobile": "9876543213"},
    ]
    
    for o_data in officers_data:
        officer = Officer(**o_data, last_active=datetime.now())
        db.add(officer)
    
    db.commit()
    print(f"✓ Seeded {len(officers_data)} officers")
    db.close()


def seed_claims():
    """Seed FRA claim data"""
    db = SessionLocal()
    print("\nSeeding claims...")
    
    villages = db.query(Village).all()
    tribal_groups = ["Gond", "Baiga", "Bhil", "Korku", "Sahariya", "Kondh", "Bonda", "Tripuri"]
    statuses = [ClaimStatus.granted, ClaimStatus.pending, ClaimStatus.rejected, ClaimStatus.verified]
    
    claims_count = 0
    for village in villages:
        num_claims = random.randint(10, 25)
        for i in range(num_claims):
            claim_id = f"{village.state}-{village.district[:3].upper()}-C{claims_count+1:06d}"
            status = random.choice(statuses)
            
            claim = FRAClaim(
                claim_id=claim_id,
                claimant_name=f"Claimant {claims_count+1}",
                father_husband_name=f"Father {claims_count+1}",
                mobile=f"98765{claims_count%100000:05d}",
                tribal_group=random.choice(tribal_groups),
                is_pvtg=random.random() < 0.15,
                state=village.state,
                district=village.district,
                block=village.block,
                village_code=village.code,
                claim_type=random.choice([ClaimType.IFR, ClaimType.CFR, ClaimType.CR]),
                area_claimed_ha=round(random.uniform(0.5, 4.0), 2),
                area_verified_ha=round(random.uniform(0.5, 4.0), 2) if status == ClaimStatus.granted else None,
                status=status,
                filed_date=date.today() - timedelta(days=random.randint(30, 730)),
                grant_date=date.today() - timedelta(days=random.randint(1, 90)) if status == ClaimStatus.granted else None,
                frc_verified=status != ClaimStatus.pending,
                sdlc_verified=status == ClaimStatus.granted,
            )
            db.add(claim)
            claims_count += 1
            
            # Update village claim counts
            village.total_claims += 1
            if status == ClaimStatus.granted:
                village.granted_claims += 1
                village.patta_holder_count += 1
            elif status == ClaimStatus.pending:
                village.pending_claims += 1
            elif status == ClaimStatus.rejected:
                village.rejected_claims += 1
    
    db.commit()
    print(f"✓ Seeded {claims_count} claims")
    db.close()


def seed_dss_recommendations():
    """Seed DSS recommendations"""
    db = SessionLocal()
    print("\nSeeding DSS recommendations...")
    
    villages = db.query(Village).all()
    schemes = [
        {"id": "PM-KISAN", "name": "PM-KISAN"},
        {"id": "JJM", "name": "Jal Jeevan Mission"},
        {"id": "PMAY-G", "name": "Pradhan Mantri Awas Yojana - Gramin"},
        {"id": "MGNREGA", "name": "MGNREGA"},
        {"id": "EMRS", "name": "Eklavya Model Residential Schools"},
    ]
    
    priorities = ["critical", "high", "medium", "low"]
    
    rec_count = 0
    for village in villages[:3]:  # Only for first 3 villages
        for scheme in random.sample(schemes, 2):  # 2 random schemes per village
            eligible = random.randint(50, 150)
            enrolled = random.randint(10, 80)
            gap = eligible - enrolled
            
            rec = DSSRecommendation(
                village_code=village.code,
                state=village.state,
                district=village.district,
                block=village.block,
                scheme_id=scheme["id"],
                scheme_name=scheme["name"],
                eligible_beneficiaries=eligible,
                currently_enrolled=enrolled,
                gap=gap,
                priority=random.choice(priorities),
                ai_score=round(random.uniform(0.6, 0.95), 2),
                trigger_condition=f"High gap detected: {gap} eligible beneficiaries not enrolled",
                action_required="Conduct village-level enrollment camp within 30 days",
            )
            db.add(rec)
            rec_count += 1
    
    db.commit()
    print(f"✓ Seeded {rec_count} DSS recommendations")
    db.close()


def seed_grievances():
    """Seed grievances"""
    db = SessionLocal()
    print("\nSeeding grievances...")
    
    claims = db.query(FRAClaim).limit(10).all()
    categories = ["Delay in Processing", "Incorrect Survey", "Rejection Not Justified", "Document Issues"]
    statuses = ["open", "in-progress", "resolved", "closed"]
    priorities = ["urgent", "high", "medium", "low"]
    
    griev_count = 0
    for claim in claims:
        if random.random() < 0.3:  # 30% claims have grievances
            griev_id = f"GRV-{claim.state}-{griev_count+1:06d}"
            status = random.choice(statuses)
            
            grievance = Grievance(
                grievance_id=griev_id,
                claimant_name=claim.claimant_name,
                mobile=claim.mobile,
                claim_id=claim.claim_id,
                state=claim.state,
                district=claim.district,
                block=claim.block,
                village=f"Village {griev_count+1}",
                category=random.choice(categories),
                description=f"Grievance description for {griev_id}",
                priority=random.choice(priorities),
                status=status,
                filed_date=date.today() - timedelta(days=random.randint(1, 60)),
                days_open=random.randint(1, 60) if status != "resolved" else None,
            )
            db.add(grievance)
            griev_count += 1
    
    db.commit()
    print(f"✓ Seeded {griev_count} grievances")
    db.close()


def main():
    """Run all seed functions"""
    print("=" * 60)
    print("VanAdhikar Drishti — Database Seeding")
    print("=" * 60)
    
    try:
        create_tables()
        seed_villages()
        seed_officers()
        seed_claims()
        seed_dss_recommendations()
        seed_grievances()
        
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        raise


if __name__ == "__main__":
    main()
