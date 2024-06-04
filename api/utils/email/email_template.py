EMAIL_FROM_WEBSITE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Ticket Confirmation</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f7f7f7;">
    <div style="max-width: 600px; margin: 20px auto; padding: 0; text-align: center;">
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 15px 15px 0 0;">
            <img src="https://www.uxlivinglab.org/wp-content/uploads/2023/08/logo-e1531386713115.webp" alt="Company Logo" style="max-width: 150px; height: auto;">
        </div>
        <div style="background-color: #fff; border-radius: 0 0 15px 15px; padding: 30px; margin-bottom: 20px;">
            <h3 style="font-size: 24px; margin-bottom: 20px;">Your ticket {} has been opened</h3>
            <p style="font-size: 18px; margin-bottom: 20px; text-align: left;">Hello Customer,</p>
            <p style="font-size: 18px; margin-bottom: 20px; text-align: left;">Thank you for contacting us. Your ticket has been received and will be answered shortly. The details of your ticket are shown below:</p>
            <div style="text-align: left; margin-bottom: 20px;">
                <p><strong>Ticket ID:</strong> {}</p>
                <p><strong>Priority:</strong> Normal</p>
                <p><strong>Status:</strong> Open</p>
            </div>
            <a href="https://www.dowellchat.uxlivinglab.online" style="display: inline-block; background-color: #007bff; color: #fff; text-decoration: none; font-size: 16px; padding: 10px 20px; border-radius: 5px; border: none;">View Ticket</a>

        </div>
        <div style="font-size: 14px; margin-bottom: 20px;">
            <p>DoWell UX LivingLab</p>
        </div>
    </div>
</body>
</html>

"""
