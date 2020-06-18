### Setup Python Virtual Environment
```buildoutcfg
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Create secrets.json file
Example `secrets.json`
```json
{
  "username": "exampleusername",
  "password": "myP@ssword123"
}
```

### RUN SCRIPT
```buildoutcfg
python3 checkio.py
```
