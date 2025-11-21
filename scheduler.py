"""
Irrigation Scheduler - Background task processor
Implements the decision logic from the diagram
"""
from datetime import datetime, timedelta
from app import app, db, IrrigationSchedule, User
import requests

def check_rain_forecast(location, hours=24):
    """
    Step 2.0: Check if rain is expected in next 24h
    Returns: (bool, probability)
    """
    try:
        # Mock implementation - in production, use real weather API
        # For now, return False (no rain) to allow testing
        return False, 0.0
    except Exception as e:
        print(f"Error checking rain: {e}")
        return False, 0.0

def check_soil_moisture_threshold(soil_moisture, crop_type):
    """
    Step 4.0: Check if soil moisture is below threshold
    Returns: bool (True if below threshold, needs irrigation)
    """
    # Threshold values for different crops (in moisture units 0-1000)
    thresholds = {
        'Wheat': 400,
        'Rice': 600,
        'Cotton': 350,
        'Sugarcane': 500,
        'Maize': 380,
        'Soybean': 370,
        'default': 400
    }
    
    threshold = thresholds.get(crop_type, thresholds['default'])
    return soil_moisture < threshold

def process_schedule(schedule_id):
    """
    Main scheduler logic - processes one schedule
    Implements the complete decision diagram
    """
    with app.app_context():
        schedule = IrrigationSchedule.query.get(schedule_id)
        if not schedule or schedule.status != 'pending':
            return
        
        user = schedule.user
        prediction = schedule.prediction
        
        print(f"Processing schedule {schedule_id} for user {user.username}")
        
        # Step 1.0: Fetch & Process Data
        location = user.location or "New Delhi"
        
        # Step 2.0: Is Rain Expected (next 24h)?
        rain_expected, rain_prob = check_rain_forecast(location)
        
        if rain_expected:
            # Step 3.0: CANCEL Schedule
            schedule.status = 'cancelled'
            schedule.cancellation_reason = f'Rain expected (probability: {rain_prob}%)'
            schedule.notification_sent = True
            db.session.commit()
            
            print(f"✗ Schedule {schedule_id} CANCELLED - Rain expected")
            send_notification(user, f"Irrigation cancelled - Rain expected ({rain_prob}%)")
            return
        
        # Step 4.0: Is Soil Moisture < Threshold?
        if prediction:
            soil_ok = not check_soil_moisture_threshold(prediction.soil_moisture, prediction.crop_type)
        else:
            soil_ok = False
        
        if soil_ok:
            # Step 5.0: POSTPONE Schedule
            schedule.status = 'postponed'
            schedule.scheduled_time = datetime.utcnow() + timedelta(hours=12)
            schedule.cancellation_reason = 'Soil moisture adequate'
            schedule.notification_sent = True
            db.session.commit()
            
            print(f"⏸ Schedule {schedule_id} POSTPONED - Soil OK")
            send_notification(user, "Irrigation postponed - Soil moisture adequate. Rescheduled for 12h later.")
            return
        
        # Step 6.0: RUN AI PREDICTION MODEL (already done, using stored prediction)
        # Water amount already calculated in prediction
        
        # Step 7.0: EXECUTE IRRIGATION
        schedule.status = 'executing'
        db.session.commit()
        
        print(f"▶ Schedule {schedule_id} EXECUTING - {schedule.water_amount}mm for {schedule.duration} minutes")
        
        # Simulate irrigation execution
        execute_irrigation(schedule)
        
        # Mark as completed
        schedule.status = 'completed'
        schedule.executed_at = datetime.utcnow()
        schedule.notification_sent = True
        db.session.commit()
        
        print(f"✓ Schedule {schedule_id} COMPLETED")
        send_notification(user, f"Irrigation completed! Applied {schedule.water_amount}mm of water.")

def execute_irrigation(schedule):
    """
    Step 7.0: Execute irrigation
    In production, this would send commands to hardware
    For now, it's a simulation
    """
    # Log execution
    print(f"  → Sending command to hardware...")
    print(f"  → Water amount: {schedule.water_amount}mm")
    print(f"  → Duration: {schedule.duration} minutes")
    print(f"  → Start timer...")
    
    # In production:
    # - Send command to IoT device
    # - Monitor execution
    # - Handle errors
    
    # Simulate execution time (instant for now)
    pass

def send_notification(user, message):
    """
    Send notification to farmer
    In production: SMS, Email, Push notification
    For now: Just log it
    """
    print(f"  📧 Notification to {user.username}: {message}")
    # In production:
    # - Send email via Flask-Mail
    # - Send SMS via Twilio
    # - Send push notification

def check_pending_schedules():
    """
    Background task that runs every hour
    Checks all pending schedules that are due
    """
    with app.app_context():
        now = datetime.utcnow()
        
        # Find all pending schedules that are due
        due_schedules = IrrigationSchedule.query.filter(
            IrrigationSchedule.status == 'pending',
            IrrigationSchedule.scheduled_time <= now
        ).all()
        
        print(f"\n⏰ Checking schedules at {now}")
        print(f"Found {len(due_schedules)} due schedules")
        
        for schedule in due_schedules:
            try:
                process_schedule(schedule.id)
            except Exception as e:
                print(f"Error processing schedule {schedule.id}: {e}")
                schedule.status = 'failed'
                schedule.cancellation_reason = str(e)
                db.session.commit()

if __name__ == '__main__':
    # Test the scheduler
    check_pending_schedules()
