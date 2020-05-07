# csfd_scraper

## Nový projekt

```shell
pipenv install scrapy
pipenv shell
scrapy startproject <nazev projektu>
```



## Spuštění lokálně

```shell
cd <název projektu>
scrapy crawl <název spideru>
```

## Nasazení na Scrapy Cloud

```shell
pipenv install shub
pipenv shell
shub login
API key: <api key vytvořeného projektu>
shub deploy (project_ID)

# v nastavení projektu pak nastavit ITEM_PIPELINES = {}
```

## Nasazení pomocí scrapyd

### Instalace

```
pip3 install cryptography==2.8
pip3 install setuptools
pip3 install scrapyd
mkdir /etc/scrapyd
touch /etc/scrapyd/scrapyd.conf
scrapyd
```

### Vytvoření servisy

```
vim /etc/systemd/system/scrapyd.service
```

```properties
[Unit]
Description=Scrapyd service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=<zvolený domovský adresář pro scrapyd (logy, atd)>
ExecStart=/usr/local/bin/scrapyd

[Install]
WantedBy=multi-user.target
```

```shell
systemctl enable scrapyd.service
systemctl status scrapyd.service
systemctl restart scrapyd.service
systemctl stop scrapyd.service
```



### Nasazení projektu

Scrapyd se dá ovládat přes HTTP rozhraní, čili například *curlem*. Tady je [odkaz](https://scrapyd.readthedocs.io/en/stable/api.html) do dokumentace. Je potřeba projekt zabalit do vajíčka a to poslat do scrapyd. Uloží se do něj určitá verze projektu. Pokud zadaný projekt ve scrapyd není, tak se vytvoří

#### Zabalení do vajíčka

```shell
python3 setup.py bdist_egg
```

Vajíčko by potom mělo být ve složce ```dist```.

#### Přidání verze do scrapyd

```shell
curl http://localhost:6800/addversion.json -F project=<název projektu> -F version=<číslo verze> -F egg=@< cesta k vajíčku, např. dist/project-1.0-py3.6.egg>
```

### Ovládání scrapyd

Předpokládám, že scrapyd běží na http://localhost:6800.

```shell
# zobrazení projektů
curl http://localhost:6800/listprojects.json

# zobrazení verzí projektu
curl http://localhost:6800/listversions.json?project=<název projektu>

# zobrazení spiderů v projektu
curl http://localhost:6800/listspiders.json?project=<název projektu>

# zapnutí spidera (vytvoření jobu)
curl http://localhost:6800/schedule.json -d project=<název projektu> -d spider=<název spidera>

# zobrazení jobů (běžících i doběhlých jobů)
curl http://localhost:6800/listjobs.json?project=<název projektu>

# vypnutí běžícího jobu
curl http://localhost:6800/cancel.json -d project=<název projektu> -d job=<id jobu>
```

### Webové rozhraní

Scrapyd poslouchá na 127.0.0.1:6800. Reaguje jenom na požadavky z localhostu. Aby to fungovalo na remote serveru, musí se ve scrapyd.conf nastavit ```bind_address = 0.0.0.0```, ale to není vůbec bezpečné.

### ScrapydWeb

Existuje bezpečnější webové rozhraní od 3. strany.

#### Instalace

```shell
sudo pip3 install --upgrade git+https://github.com/my8100/logparser.git
pip3 install scrapydweb
scrapydweb
vim scrapydweb_settings*py

####
ENABLE_AUTH = True
USERNAME = 'petr'
PASSWORD = 'Sezameotevrise94'
SCRAPYD_SERVERS = [
    '127.0.0.1:6800'
]
LOCAL_SCRAPYD_SERVER = '127.0.0.1:6800'
LOCAL_SCRAPYD_LOGS_DIR = '/home/petr/scrapyd/logs'
ENABLE_LOGPARSER = True
####
```

 #### Systemd servisa

```
sudo vim /etc/systemd/system/scrapydweb.service
```

```properties
[Unit]
Description=ScrapydWeb service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=<zvolený domovský adresář pro scrapydweb>
ExecStart=/usr/local/bin/scrapydweb

[Install]
WantedBy=multi-user.target
```

```shell
systemctl enable scrapydweb.service
systemctl status scrapydweb.service
systemctl restart scrapydweb.service
systemctl stop scrapydweb.service
```

# TODO 19.4.

* hodit csfd_scrapera do githubu -> HOTOVO
* odepsat rauchovi
* hodit link jary vrany
* sepsat si postup pro scrapy cloud i scrapyd
* sepsat item pipelinu aby se mi to házelo do csv -> HOTOVO
* nahrát do google serveru -> HOTOVO
* scrapyd jako servisa -> HOTOVO
* hodit si klíč i z trask laptopu -> HOTOVO
* opravit rok, vsechny it veci -> HOTOVO
* item pipelina -> HOTOVO

git stash push --include-untracked

pip3 install cryptography==2.8
pip3 install setuptools
pip3 install scrapyd

# servisu nastavit s </home/petr>

# udelat </home/petr>/artifacts

python3 setup.py bdist_egg

curl http://localhost:6800/addversion.json -F project=csfd_scraper -F version=1 -F egg=@dist/project-1.0-py3.6.egg

curl http://localhost:6800/listprojects.json

curl http://localhost:6800/listversions.json?project=csfd_scraper

curl http://localhost:6800/listspiders.json?project=csfd_scraper

curl http://localhost:6800/schedule.json -d project=csfd_scraper -d spider=films

curl http://localhost:6800/listjobs.json?project=csfd_scraper

curl http://localhost:6800/cancel.json -d project=csfd_scraper -d job=a9b2f1dc823e11ea9d9942010a9c0002

LOG_LEVEL = 'INFO'

mkdir scrapydweb
cd scrapydweb


sudo pip3 install --upgrade git+https://github.com/my8100/logparser.git


pip3 install scrapydweb

scrapydweb
vim scrapydweb_settings*py
ENABLE_AUTH = True
USERNAME = 'petr'
PASSWORD = 'Sezameotevrise94'
SCRAPYD_SERVERS = [
    '127.0.0.1:6800'
]
LOCAL_SCRAPYD_SERVER = '127.0.0.1:6800'
LOCAL_SCRAPYD_LOGS_DIR = '/home/petr/scrapyd/logs'
ENABLE_LOGPARSER = True


scrapydweb
scrapydweb

https://pypi.org/project/scrapy-splash/


docker pull scrapinghub/splash

docker run -d -p 8050:8050 --rm scrapinghub/splash

