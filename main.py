from send_email import EmailSender
import utils 
import pandas
import time

email_sender = EmailSender(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        sender_email='mahmoodabadihamid@gmail.com',
        sender_password="jbot optu gnwa ubfc")


df = pandas.read_excel("excel.xlsx")
df['Email title'] = df['Email title'].astype('object')
df['Email body'] = df['Email body'].astype('object')

for i in range(len(df)):
    if not pandas.isna(df.iloc[i]['Website']) and (pandas.isna(df.iloc[i]['Email body']) or df.iloc[i]['Email body'] == 'Err'):
        output = utils.fetch_and_process_webpages(df.iloc[i]['Website'])
        if output and len(output['email_body']) > 50:
            df.iloc[i, df.columns.get_loc('Email')] = output['email']
            df.iloc[i, df.columns.get_loc('Email title')] = "Expressing Interest in Ph.D. Position and Research Collaboration" #output['email_title']
            df.iloc[i, df.columns.get_loc('Email body')] = output['email_body']
            df.to_excel("excel.xlsx")
            email_sender.send_email(to_email = output['email'],#"mahmoodabadi.h@seo.com",#,
                                subject="Interested in Ph.D. Position and Research Collaboration", #output['email_title'],
                                body=output["email_body"],
                                attachment_path="MahmoodabadiHamid_CV_0708.pdf")
            
        else:
            df.iloc[i, df.columns.get_loc('Email body')] = "Err"
        df.to_excel("excel.xlsx")
        time.sleep(240)

