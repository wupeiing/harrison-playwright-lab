# Playwright Lab
All step and tests are based from this website:
https://automationexercise.com/test_cases

## How to run this code?

### Pre-request
Playwright
Anaconda
Required packages

### Install anaconda (Sample with Macbook Air M4 chip)
* Download the anaconda
```
$ curl -O https://repo.anaconda.com/archive/Anaconda3-2025.12-2-MacOSX-arm64.sh
```

* Install the package
```
$ bash ~/Anaconda3-2025.12-2-MacOSX-arm64.sh
```

* Ensure the installation is done

```
$ conda list
```
Open your terminal application and run conda list. If conda has been installed correctly, a list of installed packages appears.

* Setup an env for playwright
```
$ conda create -n playwright-env python=3.10 -y
$ conda activate playwright-env
```
if you see your terminal start with (playwright-env) xxxxxx %, then means it works


### Install packages, Python + Playwright
* Run `pip install -r requirements.txt` to install all the required

* Run this command to install playwright and chrome related dependency.
```
playwright install --with-deps chromium
```