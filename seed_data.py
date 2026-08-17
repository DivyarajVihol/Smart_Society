import os
import django
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartsociety.settings')
django.setup()

from accounts.models import CustomUser, Role
from core.models import Wing, Flat, ParkingSlot, Notice, EmergencyContact
from billing.models import MaintenanceBill, Payment
from complaints.models import Complaint
from events.models import Event, EventRSVP, Poll, PollOption, PollVote
from visitors.models import VisitorLog, GatePassRequest

def seed():
    print("[*] Seeding Smart Society database...")

    # 1. Wings and Flats
    wing_a, _ = Wing.objects.get_or_create(name='A')
    wing_b, _ = Wing.objects.get_or_create(name='B')
    wing_c, _ = Wing.objects.get_or_create(name='C')

    flat_a101, _ = Flat.objects.get_or_create(wing=wing_a, number='101')
    flat_a102, _ = Flat.objects.get_or_create(wing=wing_a, number='102')
    flat_a103, _ = Flat.objects.get_or_create(wing=wing_a, number='103')
    flat_b201, _ = Flat.objects.get_or_create(wing=wing_b, number='201')
    flat_b202, _ = Flat.objects.get_or_create(wing=wing_b, number='202')
    flat_c301, _ = Flat.objects.get_or_create(wing=wing_c, number='301')

    # Parking Slots
    ParkingSlot.objects.get_or_create(slot_number='P-A101', defaults={'assigned_to': flat_a101})
    ParkingSlot.objects.get_or_create(slot_number='P-A102', defaults={'assigned_to': flat_a102})
    ParkingSlot.objects.get_or_create(slot_number='P-B201', defaults={'assigned_to': flat_b201})

    # 2. Users (Secretary, Resident, Guard)
    # Secretary
    secretary, created = CustomUser.objects.get_or_create(
        username='secretary',
        defaults={
            'first_name': 'Rajesh',
            'last_name': 'Sharma',
            'email': 'secretary@smartsociety.com',
            'phone': '+91 98765 43210',
            'role': Role.SECRETARY,
            'flat': flat_a101,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    secretary.set_password('Password@123')
    secretary.role = Role.SECRETARY
    secretary.flat = flat_a101
    secretary.save()

    # Resident
    resident, created = CustomUser.objects.get_or_create(
        username='resident',
        defaults={
            'first_name': 'Aarav',
            'last_name': 'Mehta',
            'email': 'resident@smartsociety.com',
            'phone': '+91 98234 56789',
            'role': Role.RESIDENT,
            'flat': flat_a102,
        }
    )
    resident.set_password('Password@123')
    resident.role = Role.RESIDENT
    resident.flat = flat_a102
    resident.save()

    # Security Guard
    guard, created = CustomUser.objects.get_or_create(
        username='guard',
        defaults={
            'first_name': 'Vikram',
            'last_name': 'Singh',
            'email': 'guard@smartsociety.com',
            'phone': '+91 97123 45678',
            'role': Role.SECURITY,
            'is_on_duty': True,
        }
    )
    guard.set_password('Password@123')
    guard.role = Role.SECURITY
    guard.is_on_duty = True
    guard.save()

    # Additional Resident for community density
    resident2, created = CustomUser.objects.get_or_create(
        username='priya_patel',
        defaults={
            'first_name': 'Priya',
            'last_name': 'Patel',
            'email': 'priya@smartsociety.com',
            'phone': '+91 98111 22334',
            'role': Role.RESIDENT,
            'flat': flat_b201,
        }
    )
    resident2.set_password('Password@123')
    resident2.save()

    # 3. Emergency Contacts
    EmergencyContact.objects.get_or_create(
        name='Main Gate Security Post',
        defaults={'role_or_category': 'Security Station', 'phone': '+91 97123 45678'}
    )
    EmergencyContact.objects.get_or_create(
        name='Dr. Ananya Roy (Apollo Clinic)',
        defaults={'role_or_category': 'Resident Medical Doctor', 'phone': '+91 98222 33445'}
    )
    EmergencyContact.objects.get_or_create(
        name='Sanjay Plumber',
        defaults={'role_or_category': 'Society Plumber', 'phone': '+91 98333 44556'}
    )
    EmergencyContact.objects.get_or_create(
        name='Kishore Electrician',
        defaults={'role_or_category': 'Building Electrician', 'phone': '+91 98444 55667'}
    )

    # 4. Official Notices
    today = date.today()
    Notice.objects.get_or_create(
        title='Solar Rooftop Panel Installation Phase 2',
        defaults={
            'description': 'The eco-energy committee will commence installation of 50kW solar panels on Wing A & B terrace starting Monday. Terrace access will remain restricted between 9 AM to 5 PM.',
            'category': 'MAINTENANCE',
            'start_date': today,
            'expiry_date': today + timedelta(days=15),
            'created_by': secretary,
        }
    )
    Notice.objects.get_or_create(
        title='Annual Society Gala & Cultural Night 2026',
        defaults={
            'description': 'Join us at the Central Amphitheatre for an evening of live music, food stalls, and kids talent showcase. RSVPs are now open in the Events hub.',
            'category': 'EVENT',
            'start_date': today,
            'expiry_date': today + timedelta(days=20),
            'created_by': secretary,
        }
    )
    Notice.objects.get_or_create(
        title='Water Tank Disinfection & Pressure Test',
        defaults={
            'description': 'Municipal water tank scheduled cleaning will take place this Thursday from 1:00 PM to 4:00 PM. Please store adequate water for afternoon usage.',
            'category': 'GENERAL',
            'start_date': today - timedelta(days=2),
            'expiry_date': today + timedelta(days=5),
            'created_by': secretary,
        }
    )

    # 5. Maintenance Bills & Payments
    # Paid Bill for resident (Flat A-102)
    dec_bill, created = MaintenanceBill.objects.get_or_create(
        flat=flat_a102,
        month='December',
        year=2025,
        defaults={
            'amount': 4500.00,
            'due_date': today - timedelta(days=20),
            'is_paid': True,
        }
    )
    if created or dec_bill.is_paid:
        Payment.objects.get_or_create(
            bill=dec_bill,
            defaults={
                'method': 'UPI',
                'transaction_id': 'TXN983274982374',
            }
        )

    # Unpaid Bill for resident (Flat A-102)
    MaintenanceBill.objects.get_or_create(
        flat=flat_a102,
        month='January',
        year=2026,
        defaults={
            'amount': 4500.00,
            'due_date': today + timedelta(days=10),
            'late_fine': 0.00,
            'is_paid': False,
        }
    )

    # Bills for other flats
    MaintenanceBill.objects.get_or_create(
        flat=flat_a101,
        month='January',
        year=2026,
        defaults={
            'amount': 5000.00,
            'due_date': today + timedelta(days=10),
            'is_paid': True,
        }
    )
    MaintenanceBill.objects.get_or_create(
        flat=flat_b201,
        month='January',
        year=2026,
        defaults={
            'amount': 4500.00,
            'due_date': today + timedelta(days=10),
            'is_paid': False,
        }
    )

    # 6. Service Complaints
    Complaint.objects.get_or_create(
        title='Corridor LED sensor light flickering on 1st Floor',
        defaults={
            'description': 'The motion sensor near Flat A-102 flickers repeatedly at night and turns off abruptly.',
            'category': 'ELECTRICITY',
            'status': 'OPEN',
            'resident': resident,
        }
    )
    Complaint.objects.get_or_create(
        title='Wing B Elevator Intercom Low Audio',
        defaults={
            'description': 'The emergency call button intercom speaker inside Elevator 2 has static noise.',
            'category': 'OTHER',
            'status': 'IN_PROGRESS',
            'resident': resident2,
        }
    )
    Complaint.objects.get_or_create(
        title='Garden Sprinkler Timer Calibration',
        defaults={
            'description': 'Sprinklers near central lawn were running during peak morning jogging hours.',
            'category': 'PLUMBING',
            'status': 'RESOLVED',
            'resident': resident,
        }
    )

    # 7. Community Events & RSVPs
    gala_event, _ = Event.objects.get_or_create(
        title='Smart Society Annual Cultural Gala 2026',
        defaults={
            'date': today + timedelta(days=12),
            'time': '18:30',
            'venue': 'Central Sky Pavilion & Garden',
            'description': 'Grand community celebration featuring live acoustics, organic culinary stalls, children game zones, and annual society awards.',
            'created_by': secretary,
        }
    )
    EventRSVP.objects.get_or_create(event=gala_event, resident=resident, defaults={'is_attending': True})
    EventRSVP.objects.get_or_create(event=gala_event, resident=resident2, defaults={'is_attending': True})

    yoga_event, _ = Event.objects.get_or_create(
        title='Sunrise Yoga & Mindfulness Workshop',
        defaults={
            'date': today + timedelta(days=5),
            'time': '06:30',
            'venue': 'Clubhouse Rooftop Deck',
            'description': 'Guided breathing exercises, Vinyasa flow, and refreshing cold-pressed smoothies session led by certified instructor.',
            'created_by': secretary,
        }
    )
    EventRSVP.objects.get_or_create(event=yoga_event, resident=resident, defaults={'is_attending': True})

    # 8. Community Polls & Voting
    poll, _ = Poll.objects.get_or_create(
        question='Should we install 8 dedicated high-speed EV charging stations in Basement 1?',
        defaults={'is_active': True}
    )
    opt1, _ = PollOption.objects.get_or_create(poll=poll, option_text='Yes, install fast EV chargers immediately')
    opt2, _ = PollOption.objects.get_or_create(poll=poll, option_text='Yes, but phase 4 chargers first')
    opt3, _ = PollOption.objects.get_or_create(poll=poll, option_text='No, evaluate power load first')

    PollVote.objects.get_or_create(poll=poll, resident=resident2, defaults={'option': opt1})

    # 9. Gate Passes (Temporary & Permanent)
    GatePassRequest.objects.get_or_create(
        flat=flat_a102,
        visitor_name='Rohit Sharma (Amazon Logistics)',
        defaults={
            'phone': '+91 99887 76655',
            'purpose': 'Courier Package Delivery',
            'pass_type': 'TEMPORARY',
            'expected_date': today,
            'is_approved': True,
            'is_active': True,
        }
    )
    GatePassRequest.objects.get_or_create(
        flat=flat_a102,
        visitor_name='Maya Devi (Housekeeping)',
        defaults={
            'phone': '+91 98776 65544',
            'purpose': 'Daily Household Staff',
            'pass_type': 'PERMANENT',
            'is_approved': True,
            'is_active': True,
        }
    )
    GatePassRequest.objects.get_or_create(
        flat=flat_b201,
        visitor_name='Deepak Verma (Driver)',
        defaults={
            'phone': '+91 98665 54433',
            'purpose': 'Personal Driver',
            'pass_type': 'PERMANENT',
            'is_approved': True,
            'is_active': True,
        }
    )

    # 10. Visitor Logs (Active inside + Checked out)
    VisitorLog.objects.get_or_create(
        name='Suresh Patel (Zomato Food)',
        flat=flat_a102,
        defaults={
            'purpose': 'Lunch Delivery',
            'visitor_type': 'DELIVERY',
        }
    )
    VisitorLog.objects.get_or_create(
        name='Kavita Sen',
        flat=flat_b201,
        defaults={
            'purpose': 'Family Guest',
            'visitor_type': 'GUEST',
            'exit_time': timezone.now() - timedelta(minutes=45),
        }
    )

    print("[SUCCESS] Seed data populated successfully!")
    print("\n" + "="*55)
    print(" SMART SOCIETY LOGIN CREDENTIALS FOR TESTING")
    print("="*55)
    print(" 1. SECRETARY ACCOUNT (Admin & Management)")
    print("    Username: secretary")
    print("    Password: Password@123")
    print("    Role:     Secretary (Flat A-101)")
    print("-" * 55)
    print(" 2. RESIDENT ACCOUNT (Flat Owner / Tenant)")
    print("    Username: resident")
    print("    Password: Password@123")
    print("    Role:     Resident (Flat A-102)")
    print("-" * 55)
    print(" 3. SECURITY GUARD ACCOUNT (Gate & Visitor Console)")
    print("    Username: guard")
    print("    Password: Password@123")
    print("    Role:     Security Guard (On Duty)")
    print("="*55)

if __name__ == '__main__':
    seed()
