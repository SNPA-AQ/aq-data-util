# arpalazio-asi-ispra-qa-api-dwl
This software is designed to help ASI ISPRA project users automate the download of air quality datasets from project's repository. This software will keep in sync all configured package dataset from repository to you machine.

## License

This project is licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2 - see the [LICENSE](LICENSE) file for details

## Getting started
These instructions will get you a copy of the project up and running on your local machine. Software was tested on Centos, Ubuntu server and MacOS.
Please update pip to the latest version and use a virtual environment to wrap all your libraries.

### Prerequisites
* Python 2.7

A virtual environment is not a prerequisite, but I strongly suggest to create and use one with the right python version. You can find installation instruction for virtualenv on [the official documentation](https://virtualenv.pypa.io/en/latest/).

All library requirements are documented in requirements.txt 
To install cd to the directory where requirements.txt is located, activate your virtualenv if you have one, run the following command:
```
pip install -r requirements.txt
```

### Installing
* Check out a clone of this repo to a location of your choice, such as
   `git clone --depth=1 https://github.com/matteomorelli/arpalazio-asi-ispra-qa-api-dwl.git` or make a copy of all the files including `LICENSE` files
* Copy and rename `sample.ini`, edit it accordingly to your environment

### Configuration file
This file contains location of every file needed for a successfull execution.
You must configure it accordingly to your environment.
```
[api]
url="https://asi-ispra-qa.arpae.it/api/3/action/"
user="YOUR USERNAME"
password="YOUR PASSWORD"
package="PACKAGE NAME FROM PROJECT WEBSITE"

[path]
saveIn="/path/to/data/folder/data/"
logDirectory="/path/to/log/folder/log/"
```
## Usage
### Running
To start data download 
```
$ python handler.py configuration_file.ini
```
If you want to download two or more package configure an ini file for every package and launch handler.py with that configuration file. 
Run handler.py with -h option to receive instruction
```
$ python handler.py -h

usage: handler.py [-h] ini_file

positional arguments:
  ini_file    Location of configuration file

optional arguments:
  -h, --help  show this help message and exit
```

### Database reset
Software keep trace of every downloaded files in a simple text file, those files are located in log directory (you must configure this parameter in your configuration file). If you want to download an already existent file, open the right txt in file on log folder, look for filename and erase that line.
Filename is based on package name.

### Automation
You can schedule this software to run in an autonomous way by adding it to crontab or windows task scheduler.
Below an example of crontab scheduling to run every hour at minute 5:
```
5 * * * * /path/to/arpalazio-asi-ispra-qa-api-dwl/handler.py /path/to/arpalazio-asi-ispra-qa-api-dwl/sample.ini > /path/to/arpalazio-asi-ispra-qa-api-dwl/lastrun.log
```
Configure it accordingly to your needs.

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Matteo Morelli** - *Initial work* - [matteomorelli](https://github.com/matteomorelli)

See also the list of [contributors](https://github.com/matteomorelli/arpalazio-climate-service-wrapper/contributors) who participated in this project.

* **Andrea Bolignano** - [andrea-bolignano](https://github.com/andrea-bolignano)

