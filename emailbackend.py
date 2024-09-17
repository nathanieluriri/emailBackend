from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import yagmail

# FastAPI instance
app = FastAPI()

# SMTP server details
smtp_user = 'admin@247privatesecurity.co.uk'
smtp_password = 'Password10!'
smtp_host = 'smtp.hostinger.com'
smtp_port = 465  # Port for SMTP with SSL/TLS encryption

# Pydantic model for the request body
class OrderEmailRequest(BaseModel):
    customers_name: str
    customers_email: EmailStr
    status: str
    order_id: str

# Function to send email based on the order status
def send_email(customers_name: str, customers_email: str, status: str, order_id: str):
    """
    Sends an email to the customer based on the order status.
    
    Args:
        customers_name (str): Name of the customer.
        customers_email (str): Customer's email address.
        status (str): The current status of the order (e.g., "Order Confirmed", "Cooking in Progress").
        order_id (str): Unique identifier of the order.
    
    Raises:
        HTTPException: If the status is not recognized.
    """
    
    # Determine email subject and body based on status
    if status == "Order Confirmed":
        email_subject = 'Your Order has been Confirmed! 🍽️'
        email_body = f"""
        Hi {customers_name},
        
        Great news! Your order #{order_id} has been successfully confirmed. Our team is preparing everything to ensure you get the best meal experience.
        
        You’ll receive updates as soon as your food is being prepared. We’ll let you know when it’s on its way!
        
        Thank you for choosing [Company Name].
        
        Bon appétit! 
        The [Company Name] Team
        """
        
    elif status == "Cooking in Progress":
        email_subject = 'Your Meal is Being Prepared 🍳'
        email_body = f"""
        Hi {customers_name},
        
        Your order #{order_id} is now being freshly prepared by our chefs. We’re making sure everything is cooked to perfection just for you.
        
        We’ll notify you when the meal is on its way!
        
        If you have any questions, feel free to reach out.
        
        Kind regards,
        The [Company Name] Team
        """
        
    elif status == "Order is About to be Delivered":
        email_subject = 'Your Order is on the Way! 🚴‍♂️'
        email_body = f"""
        Hi {customers_name},
        
        Your order #{order_id} is almost there! Our delivery partner is on their way to your location with your delicious meal.
        
        Estimated delivery time: [Delivery Time]
        
        Thank you for your patience. Enjoy your meal soon!
        
        Cheers,
        The [Company Name] Team
        """
        
    elif status == "Order Delivered":
        email_subject = 'Enjoy Your Meal! 🍴'
        email_body = f"""
        Hi {customers_name},
        
        Your order #{order_id} has just been delivered to your door! We hope everything arrived just as expected and that you’re ready to dig in.
        
        If you have any feedback or issues with the order, please don’t hesitate to contact us.
        
        Thank you for choosing [Company Name]. We look forward to serving you again soon!
        
        Bon appétit,
        The [Company Name] Team
        """
        
    else:
        # Raise an exception if the status is unrecognized
        raise HTTPException(status_code=400, detail="Invalid order status.")
    
    # Send email using Yagmail
    with yagmail.SMTP(smtp_user, smtp_password, host=smtp_host, port=smtp_port) as yag:
        yag.send(to=customers_email, subject=email_subject, contents=email_body)
        print(f"Email sent to {customers_email} successfully!")


# FastAPI route to handle email sending
@app.post("/send-order-status-email/")
def send_order_status_email(request: OrderEmailRequest):
    """
    Endpoint to send an order status email to a customer.

    Args:
        request (OrderEmailRequest): JSON payload containing customer's name, email, status, and order ID.
    
    Returns:
        dict: Confirmation message on successful email sending.
    """
    send_email(request.customers_name, request.customers_email, request.status, request.order_id)
    return {"message": "Email sent successfully!"}
