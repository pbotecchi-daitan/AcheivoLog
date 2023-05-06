# AchievoLog
Script that handle the process of logging hours on Achievo's website

# Recommended Python Version
```v3.7.13+```

# Install
```pip install -r requirements.txt```

# Requirements
To make sure the script will run as expected you need to be connected on the company's VPN

# Environment variables

| Key  | Value |
| ------------- | ------------- |
| URL_PATH  | Achievo's URL that will start the Selenium automation |
| EMAIL  | Your accont EMAIL used on ACHIEVO website |
| PASSWORD | Your account PASSWORD used on ACHIEVO website |
| BROWSER | Chrome or Firefox for now|
|ENTRY_HOUR | Default entry hour to use as base when generating the desired hours |
| LUNCH_BREAK | Default lunch break to use when generating the desired |

# Running

After connected to the VPN run:
```python main.py {week number}```
