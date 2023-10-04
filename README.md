# Business-Client-Capture
A python automation, command line tool that, contains 2 tools within. One being a google maps query tool, that given a business and a location, queries about 120 business information, like phone number which can be user to later automatically send messages and files to them using the second tool.

# Google Maps Query
This version of this code uses selenium to open chrome, query the data and saving it in a excel and csv file. In more detail, it first opens google on the general location of the search to make the results more accurate, then searches for the business type, loading each one on the chrome page, then clicking the elemente of each, capturing and saving the information about the business, then later saving the excel and csv file to the results directory.

# Client Capture
It's the main automation that uses the produced excel or csv file from the Google Maps Query. It contains a timer, in which you can give the hour you'd like the messagens to start sending, it'l ask that you loging to whatsapp, it stores the login info for when the clock reaches it's time. The message can be custumisable fairly easily, by opening the messages.py file, and editing the placeholders there, as well as adding wheter to use he business name, add a 'good morning' or 'good evening' to the message, among other things.

# Editing messages in messages.py
You'll find 2 variables, being one 'txt' a lambda function that has the business name as just 'business' and the time denimination as 'time', you can add or remove as you liking in the string, but should not remove from the input of the function. the 'time_var' variable is a list that can be changed if usinng the sistem in another language, and is optional to change, either if you are already  using in english, or if your message already does not use the time variable in the txt lambda function.

To change the image send, add more, remove, send another type of file, check the Business_Client_Capture.py line line 61 on the send_message function, where the enviar_media function being used,  there you can either add more instances of the funciton, change the file being sent by giving the file location, or exclude it complitly.



the code in client_cap_experiment.py contains some experiments with a automatic time, and timezone detection given the business location, for a more accurete message, as well as a message language selector that stored messages in portuguese and english, created as a necessity, becouse i used to run it in both languages. Both ideas are not fully implemented, just mainly concepts.
