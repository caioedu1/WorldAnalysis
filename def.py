import win32com.client as win32 
import os


def send_email(emails):
    # Check if emails is a list of strings
    if not isinstance(emails, list):
        raise TypeError("Expected a list of strings")
    for email in emails:
        if not isinstance(email, str):
            raise TypeError("Expected a list of strings")
        
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = ';'.join(emails)
    mail.Subject = 'Requested Files' 
    mail.HTMLBody = '<h2> Files based on the analysis of "world-data-2023.csv" </h2>'

    pasta_arquivos = r'C:\\Users\\Caioe\\Desktop\\Caio\\Learn Coding\\html e css\\HarvardCS50\\plot_figs'

    attachment_list = []
    for root, dirs, files in os.walk(pasta_arquivos):
        for arquivo in files:
            caminho_completo = os.path.join(root, arquivo)
            attachment = mail.Attachments.Add(caminho_completo)
            attachment_list.append(attachment)
    
        
    mail.Send() 

    print ('Email sent successfully!')
    