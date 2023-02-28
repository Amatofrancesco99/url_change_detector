import streamlit as st, time, hashlib, sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from urllib.request import urlopen

def send_mail(receiver_mail, url):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[sib_api_v3_sdk.SendSmtpEmailTo(email=receiver_mail)],
        sender=sib_api_v3_sdk.SendSmtpEmailSender(email='urlChangeDetector@gmail.com', name='URL Change Detector'),
        html_content='<html><body><p>Hi '+ receiver_mail.split("@", 1)[0] + ',<br><br>The following mail to inform you that the URL '+ url+ ' has been updated.<br><br>Hope you liked this service, <br>See you soon. </p></body></html>',
        subject= 'URL updated'
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        st.exception(e)


def url_change_detector(url, seconds, mail):
    if (url != ""):
        no_changes = True
        while no_changes:
            try:
                response = urlopen(url).read() # perform the get request and store it in a var
                currentHash = hashlib.sha224(response).hexdigest() # create a hash
                time.sleep(seconds) # wait for 30 seconds
                response = urlopen(url).read() # perform the get request
                newHash = hashlib.sha224(response).hexdigest() # create a new hash

                if newHash == currentHash: # check if new hash is same as the previous hash
                    continue            
                else: # if something changed in the hashes
                    st.success('URL updated', icon="🦜")
                    st.snow()
                    if (mail != ""):
                        send_mail(mail, url)
                    no_changes = False
                        
            # To handle exceptions
            except Exception as e:
                st.exception(e)
                break


apptitle = 'URL Change Detector'
st.set_page_config(page_title=apptitle, page_icon='🦦')
st.title(apptitle + ' 🦦')

with st.sidebar:
    st.subheader("About")
    st.write("The URL Change Detector web-app has been purposely created in order to get notified once an URL has been updated.\n"
             "The mail is not mandatory, but you can insert it to get also notified with a mail (our mail plan has a *maximum of 300 mails per day* that can be sent, so"
             " some problem may occur if the users exeed this maximum).\n\n"
             "*Why you should use this service?*\nIs **simpler, and much faster with respect to all the other websites** you can find on the internet that do the"
             "same. The only disadvantage is that you have to maintain opened this page (otherwise no notifications will be sent).")
    st.subheader("Author")
    st.write("If you want to get further details on the author, you can have a look [here](https://amatofrancesco.altervista.org).\n\n"
             "Contact me or consider contributing to this repository with any suggestion or question.")


mail = st.text_input('Mail', value="")
seconds = st.number_input('Seconds between checks (*)', value=30, min_value=0, step=30)
url = st.text_input('URL (*)', value="")
button = st.button(label="Start detection", on_click=url_change_detector(url, seconds, mail), type="primary")