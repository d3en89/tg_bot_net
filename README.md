# tg_bot_net

Этот проект создан что бы можно было развернуть телеграмм бота внутри локальной сети,
представляет возможность выполнять на данный момент минимальные сетевые проверки\
\
Все модули необходимые для работы бота описаны в requirements.txt\
\ 
Проект мой личный, им занимаюсь исключительно я, он находится в состоянии дополнения \
по необходимсоти, переодически возвращаюсь к нему, чтобы навести красоту или добавить \
функционал. 

Работает на Ubuntu 22.04 + Python3.10\
\
Может выполнять  
-  ping
-  tracert
-  port ping
-  nslookup
-  generate password
-  Check zabbix status
-  whois
-  speedtest
 
###             ВАЖНЫЕ УСЛОВИЯ            
* Для работы бота необходим redis-server:
> Настраивать сервер не надо, достаточно установить и запустить его.\
> Я использую Ubuntu 22.04 устанавливаем с помощию snap:\
    ```
    sudo snap install redis
    ```
 
* Формат заполнения conf.ini :
    - [dns]\
       server=ip_вашего_dns_сервера,ip_вашего_2-го_dns_сервера
>Если необходимо указать несколько значений в настройках, то используйте этот шаблон(но не везде это сработает)\
>Для работы с ботом обязательно надо ввести свой id telegram в файл conf.ini\
>Для работы nslookup требуется вести dns сервер

* whois_ianna.py
> whois - функция использует локальный софт whois, устанавливается:\
    ```
    sudo apt-get update && sudo apt-get upgrade && sudo apt-get install whois
    ```
* get_speedtest.py
> Для работы этого скрипта необходимо установить программу speedtest-cli\
    ```
    sudo apt-get update && sudo apt-get upgrade && sudo apt-get install speedtest-cli
    ```
* my_tracert.py
> Для работы этого скрипта необходимо установить traceroute\
    ```
    sudo apt-get update && sudo apt-get upgrade && sudo apt-get install traceroute
    ```