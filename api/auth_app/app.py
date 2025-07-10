from fastapi import Body, APIRouter,Query, HTTPException, BackgroundTasks
from sqlalchemy import create_engine, Column, Boolean, Float, Integer, String
from db.database import Base,get_db
from fastapi import Request, FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, declarative_base


# authenticate router
router = APIRouter()


from typing import Dict
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

# class EmailData(Base):
#     email: str
#     data: dict

def email_send(email,data):
    send_email(email,data)

def send_email(email: str, data: dict):
    # Email configuration
    sender_email = "faizan@gmail.com"
    sender_password = "kwnd sfgc dtui vrvs"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create message container - the correct MIME type is multipart/alternative
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Parking Booking Confirmation"
    msg['From'] = sender_email
    msg['To'] = email

    # Create the body of the message (a plain-text and an HTML version).
    text = f"Here is your data: {data}"

    html_email_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parking Booking Confirmation</title>
    </head>
    <body style="font-family: Arial, sans-serif;">

    <h2 style="color: #333;">Parking Booking Confirmation</h2>

    <p>Dear,</p>

    <p>Thank you for booking a parking space with us. Below are the details of your booking:</p>

    <ul>
        <li><strong>Price:</strong> Rs {data.get("price")}</li>
        <li><strong>Status:</strong> {data.get("status")}</li>
        <li><strong>Parking Slot:</strong> {data.get("parking_slot")}</li>
        <li><strong>Floor:</strong>{data.get("floor")} </li>
    </ul>

    <p>Your parking space has been successfully reserved. Please make sure to arrive on time and present this email confirmation at the parking lot entrance for validation.</p>


    <p>Thank you for choosing our parking service!</p>

    <p>Best regards,<br>
    SmartParking</p>

    </body>
    </html>
    """

    # Attach parts into message container
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html_email_template, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via an SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())

@router.post("/send_email/")
async def send_email_handler(email_data: dict, bg_task:BackgroundTasks):
    try:
        bg_task.add_task(email_send,email_data.get("email"), email_data.get("data"))
        # send_email(email_data.get("email"), email_data.get("data"))
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")



class ParkingLot(Base):
    __tablename__ = "parking_lot"

    parking_slot = Column(String(100), primary_key=True, index=True)
    status = Column(Boolean)
    price = Column(Float)
    floor = Column(Integer)


@router.get("/parking_lot")
def read_all_parking_lots(floor=None, db: Session = Depends(get_db)):
    print(floor)
    parking_lots = db.query(ParkingLot).all() if floor in ["0",""] or floor is None else db.query(ParkingLot).filter(ParkingLot.floor == floor).all()
    for p in parking_lots:
        p.status = "Available" if p.status == 1 else "Not Available"
    return parking_lots


@router.get("/reserve_parking_slot/{slot_number}")
def check_parking_slot(slot_number: str, db: Session = Depends(get_db)):
    parking_slot = db.query(ParkingLot).filter(ParkingLot.parking_slot == slot_number,ParkingLot.status == 1).first()
    if parking_slot is None:
        return {"status": False}
    return {"status": True}


from api.schema import ParkingData
from fastapi import Request


@router.post("/send_parking_data")
async def receive_parking_data(request:Request, db: Session = Depends(get_db)):
    body = await request.body()
    # print(body)
    # Decode the body content into a string
    body_str = body.decode("utf-8")

    # Splitting the data into key-value pairs
    data = {}
    for item in body_str.split("&"):
        key, value = item.split("=")
        data[key] = value

    print(data)
    # Validate API key (optional)
    if data["api_key"] != "#54321":
        return {"error": "Invalid API key"}

    # Perform operations with received data
    value = data["value"]
    parking_slot = db.query(ParkingLot).first()

    # Update the status field of the first row
    if parking_slot:
        # Update the status to 1 or 0 based on your condition
        parking_slot.status = int(value)  # or 0

        # Commit the transaction
        db.commit()

        print("Status updated successfully")
    else:
        print("No data found")

    return {"message": "Data received successfully"}
