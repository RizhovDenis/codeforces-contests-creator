# Codeforces contests creator

### Requirements
* Python 3.8+
* PostgreSQL 10+

### 1. Create project directory
```bash
mkdir ~/CFCC && cd ~/CFCC
git clone https://github.com/RizhovDenis/codeforces-contests-creator.git cfcc
python3 -m venv cfcc_venv
source cfcc_venv/bin/activate && cd ~/CFCC/cfcc
pip install -r  requirements.txt
```

### 2. Prepare database
```bash
sudo -u postgres psql -c "create database codeforces;"
alembic upgrade head
```
### 3. Receive telegram token
Open BotFather in telegram and generate a bot. After all set your telegram_token into settings.py 

### 4. Run project
```bash
python manager.py parser parse-codeforces
python manager.py parser telegram-bot
```
