# Kube Secrets Finder (kubernetes cronjob)

<div style="text-align:center"><img src ="kubernetes.png" /><img src ="Python_logo_and_wordmark.png" /><img src="cronjob.png" /></div>  

Kubernetes cronjob. Finds unused secrets, drops secrets with "istio" in the name and sends result via email.  
Находит предположительно незадействованные секреты в конфиге Kubernetes. Отбрасывает секреты с именами содержащими "istio"

### IMPORTANT! Prerequisites
First make sure that you run under a service account that has sufficient rights to view the objects.  
To fulfill this requirement, you can apply the Roles-Setup.yaml file before deployment:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;kubectl apply -f Roles-Setup.yaml  

Role-setup.yml creates a new cluster role - view-secrets (it standard "view" clusterrole but extended to view secrets)  
and a new service account - view-secrets linked to clusterrole.  
Service account view-secrets runs pod described in cronjob.yaml  


### What is this Kronjob useful for?
Sends to ADDR_TO email a report on secrets that are not found in the bodies of Kubernetes objects and therefore,
may be unused.  

### SETUP
1. First of all apply Roles-setup.yml:  
kubectl apply -f Roles-setup.yml  
2. Build docker image:  
docker build .  
3. Push docker image into your docker registry  
4. In cronjob.yml change ${YOUR_IMAGE_PULL_SECRET} and ${YOUR_DOCKER_IMAGE} variables to fit your registry  
5. Apply cronjob.yml to your Kubernetes cluster:  
kubectl apply -f cronjob.yml  

### Variables:
SCHEDULE: "0 0 * * 0 " - (cronjob.yml) job run time (in this example every sunday 00:00)  
WHERE_AM_I: "DEV" - environment mark (Dev Stage Prod etc) appears in email Subject  
MAILSERVER: "mailserver" - smtp server name or IP (port 25)  
ADDR_FROM: "kube-secrets-finder@example.com" - field "From:"  
ADDR_TO: "devops@example.com" - email to send a report  
requirements.txt - python libs  

### How does it work
It's python. Connects to the kubernetes API, takes the names of all secrets in all namespaces  
and searches for references to them in the bodies of PODs, deployments, configmaps, service accounts and ingresses.  
After that, it connects to the mail server MAILSERVER and sends an email to the ADDR_TO mailbox.  

### Sample Report Letter
Subject: Kube DEV Secrets Finder  
From: kube-secrets-finder@example.com  
To: devops@example.com  

EmailBody:  
DEV. This 5 secrets looks like unused  

aservice-postgres-credentials  
bservice-rabbit-credentials  
cservice-postgres-credentials  
dservice-postgres-credentials  
eservice-postgres-credentials  

### Limitations
Secrets with the names of istio can be discarded in the first cycle, so as not to search for them by configs.  
The letter duplicates the names of secrets, when the names coincide in different namespaces.  


### ВАЖНО! Пререквизиты
Сначала убедитесь, что запускаете под под сервисным аккаунтом, который имеет достаточно прав на просмотр объектов.  
Чтобы выполнить это требование, перед деплоем можно применить файл Roles-Setup.yaml:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;kubectl apply -f Roles-Setup.yaml  

Создается новый сервисный аккаунт view-secrets, новая кластерная роль view-secrets  
View-secrets - копия кластерной роли view, но расширенная до просмотра секретов  
Создается привязка кластерной роли view-secrets к сервисному аккаунту view-secrets  

Сам сервисный аккаунт указан в манифесте cronjob.yaml  


### Для чего полезен этот кронджоб
Присылает на почту ADDR_TO отчет о секретах, которые не обнаружены в телах объектов Kubernetes и поэтому,  
возможно, являются неиспользуемыми.  


### Переменные для .gitlab-ci.yml:
SCHEDULE: "0 0 * * 0 " - время запуска джоба (здесь в воскресенье в 00:00 часов)  
WHERE_AM_I: примеры "Dev" "Stage" или "Prod" - в теме письма укажет с какого кластера пришел отчет  
MAILSERVER: "mailserver" - имя или IP почтового сервера/сервиса с 25 портом  
ADDR_FROM: "kube-secrets-finder@example.com" - не имеет значения, но разхардкодил  
ADDR_TO: "devops@example.com" - емаил куда слать отчет о проверке  
requirements.txt - список библиотек python  

### Логика
Основной модуль на python. Подключается к API kubernetes, берет имена всех секретов во всех неймспейсах  
и ищет упоминания о них в телах подов, деплойментов, конфигмапов, сервисных аккаунтов и ингресов.  
После этого подключается к почтовому серверу MAILSERVER и отправляет письмо на ящик ADDR_TO.  

### Пример письма с отчётом
Subject: Kube DEV Secrets Finder  
From: kube-secrets-finder@example.com  
To: devops@example.com  
DEV. This 5 secrets looks like unused  

aservice-postgres-credentials  
bservice-rabbit-credentials  
cservice-postgres-credentials  
dservice-postgres-credentials  
eservice-postgres-credentials  


### UPGR 22.04.19
Переписал тело программы, расписал по функциям
Изменил логику работы - теперь сначала вытягивает имена секретов в список и потом работает с ним
Изменил имена переменных и добавил ADDR_FROM, которая была захардкожена
Теперь перед отправкой письма из списка убираются секреты, содержащие 'istio' в имени
Теперь список более читаем, т.к. перед отправкой сортируется по алфавиту

### Недостатки
Секреты с именами istio можно отбрасывать в первом цикле, чтоб не искать их по конфигам
В письме дублируются имена секретов, когда в разных неймспейсах совпадают имена

