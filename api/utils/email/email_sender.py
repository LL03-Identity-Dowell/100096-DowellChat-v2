import requests
import re

def send_email(toname, toemail, subject, email_content):
    """
    The `send_email` function sends an email using the Dowell Mail API services.
    
    :param toname: The `toname` parameter is the name of the recipient to whom the email will be sent.
    :param toemail: The `toemail` parameter in the `send_email` function is the email address of the
    recipient to whom you want to send the email. 
    :param subject: The `subject` parameter in the `send_email` function refers to the subject line of
    the email that will be sent. 
    :param email_content: The `email_content` parameter in the `send_email` function refers to the
    content or body of the email that you want to send. 
    :return: The function `send_email` is returning the response text from the API call made to the
    specified URL.
    """
    url = "https://100085.pythonanywhere.com/api/email/"

    payload = {
        "toname": toname,
        "toemail": toemail,
        "subject": subject,
        "email_content": email_content
    }
    response = requests.post(url, json=payload)
    return response.text




def is_valid_email(email):
    """
    The function `is_valid_email` checks if a given email address is valid based on a specific pattern.
    
    :param email: The function `is_valid_email` takes an email address as input and checks if it is a
    valid email address based on a regular expression pattern. 
    :return: The function `is_valid_email(email)` returns `True` if the email passed as an argument
    matches the specified email pattern, and `False` otherwise.
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_pattern, email):
        return True
    else:
        return False
