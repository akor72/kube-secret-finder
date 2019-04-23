# kube-secret-finder
Kubernetes cronjob. Finds unused secrets. Drops secrets with "istio" in the name
Находит предположительно незадействованные секреты в конфиге Kubernetes. Отбрасывает секреты с именами содержащими "istio"

# Kube Secrets Finder (kube cronjob)

<div style="text-align:center"><img src ="Python_logo_and_wordmark.png" /><img src="cronjob.png" /></div>


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
После этого подключается к почтовому серверу MAILSERVER и отправляет письмо на ящик EMAIL_ADDR.  

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

