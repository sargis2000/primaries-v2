# primaries-v2
## manual Instalation 
### Step1:  
Install Git by running  on Debian-based distributions like Ubuntu
```bash
sudo apt install git
```
 or
 ```bash
sudo dnf install git
```
### Step2:
[Create githob account](https://www.google.com)
### Step3:
Add configs 
``` bash
git config --global user.name "YOUR NAME"
```
``` bash
git config --global user.email "YOUR EMAIL"
```
### Step4:
[Creat personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
### Step5:
Clone repositoy
``` bash
git clone github/repsitory/url
```
insted of password use your personal access token.
### Step6: 
Install python.\
Run the following commands as root or user with sudo access to update the packages list and install the prerequisites:
``` bash
sudo apt update
sudo apt install software-properties-common
```
Add the deadsnakes PPA to your system’s sources list:
``` bash
sudo add-apt-repository ppa:deadsnakes/ppa
```
When prompted press ```ENTER``` to continue:\
Once the repository is enabled, install Python 3.10 with:
``` bash
sudo apt install python3.10
```
Verify that the installation was successful by typing:
``` bash
python3.8 --version
```
### Step7:
Isntall pip
``` bash
sudo apt-get install python3-pip 
```

### Step8:
Install dependencies
``` bash
pip install -r requirements.txt
```

### Step9:
Apply migranions
``` bash
python manage.py makemigrations && python manage.py migrate
```

### Step10:
[Install ZAP](https://www.zaproxy.org/download/)

### Step11:
Create .env  and fill it  
SECRET_KEY=django secret key     
zap_api_key=zap api key
```bash 
touch .env

MAILGUN_KEY=****
ADMIN_EMAIL=****
EMAIL_FROM=****
APP_SECRET_KEY=****
DEPLOYMENT_MODE=boolean
EDP_REC_ACCOUNT=idram merchant account
SECRET_KEY=Idram secret
```
### Step12:
Run the server 
``` bash
python manage.py runserver
```
