# This txt can be edited as you'r liking, adding the time discriber below (calculated with the corrent time), and business name. You canadd and remove both variables as you like inside the string, no need to check the references.

# For image or file adition check Business_Client_Capture.py - line 61 on the send_message function, where the enviar_media function being used,  there you can either add more instances, change the file being sent by giving the file location, or exclude it complitly.

# Fore more info check main github repository!

#Main text message
txt = lambda time, business: f'''
{time}, {business} this is a test message for my automation application, check it out at the link below.

https://github.com/Superjoa10/business-client-capture/tree/main
'''
#Main time denominators
time_var = ['Good Morning', 'Good Evening', 'Good Night']