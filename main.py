""" importing kubernetes modules """
from kubernetes import config, client
config.load_incluster_config()
v1 = client.CoreV1Api()

import kubernetes.client
configuration = kubernetes.client.Configuration()
api_instance = kubernetes.client.ExtensionsV1beta1Api(kubernetes.client.ApiClient(configuration))


""" Import email lib """
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


""" Imports OS variables """
import os
print(os.environ['WHERE_AM_I'])
environment = os.environ['WHERE_AM_I']
mailserver = os.environ['MAILSERVER']
addr_to = os.environ['ADDR_TO']
addr_from = os.environ['ADDR_FROM']



""" Declare functions """
def secrets_list():
        a = []
        for i in allsecrets.items:
                a.append(i.metadata.name)
        print(a)
        return a


def general(secrets, text):
    a = []
    for i in secrets:
        print("LOOKING FOR " + "%s" % (i))
        n = text.find(i)
        if n == -1:
            print("%s" % (i) + " NOT FOUND!")
            a.append(i)
    print(a)
    return a


def rm_istio_secrets(secrets):
        a = []
        for i in secrets:
                if 'istio' not in i:
                        print('istio not found in ' + i)
                        a.append(i)
                else:
                        print('istio was found in ' + i)
        a.sort()
        return a


def email_body():
        mail = environment + ". This " + str(len(result)) + " secrets looks like unused \n\n"
        for i in range(len(result)):
                mail = mail + result[i] + " \n"
        mail = mail + " \n\n"
        return mail

""" Put all secrets names into a list """
allsecrets = v1.list_secret_for_all_namespaces(watch=False)
result = secrets_list()
print("The length of list is: ", len(result))


""" Get all pods config as a text and try to find secrets names in it """
allpods = str(v1.list_pod_for_all_namespaces(watch=False))
result = general(result, allpods)
print("The length of list is: ", len(result))


""" Get all ingrass config as a text and try to find secrets names in it """
allingress = str(api_instance.list_ingress_for_all_namespaces(watch=False))
result = general(result, allingress)
print("The length of list is: ", len(result))


""" Gets all configmaps as a text and try to find secrets names in it """
allconfigmaps = str(v1.list_config_map_for_all_namespaces(watch=False))
result = general(result, allconfigmaps)
print("The length of list is: ", len(result))


""" Gets all serviceaccounts config as a text and try to find secrets names in it """
allserviceaccounts = str(v1.list_service_account_for_all_namespaces(watch=False))
result = general(result, allserviceaccounts)
print("The length of list is: ", len(result))


""" Gets all deployments config as a text and try to find secrets names in it """
alldeployments = str(api_instance.list_deployment_for_all_namespaces(watch=False))
result = general(result, alldeployments)
print("The length of list is: ", len(result))


""" Drop istio secrets """
result = rm_istio_secrets(result)
print("The length of list is: ", len(result))


""" Make email body """
body = email_body()


""" Send email """
print('Sending email from ' + addr_from + ' to ' + addr_to)
msg = MIMEMultipart()
subject = "Kube " + environment + " Secrets Finder"

msg['From'] = addr_from
msg['To'] = addr_to
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))
text=msg.as_string()

s = smtplib.SMTP(mailserver)
s.sendmail(addr_from, addr_to, text)
s.quit()

print('JOB COMPLETE!')
