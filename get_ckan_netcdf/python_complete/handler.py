# Copyright (c) 2018 ARPA Lazio <craria@arpalazio.it>
# SPDX-License-Identifier: EUPL-1.2

# Author: Matteo Morelli <matteo.morelli@gmail.com>

import logging
import logging.config
import argparse
import ConfigParser
import requests
import sys
from libs import utils_os
from libs import utils

# Script version
VERSION = "1.0.0"

# initialize basic logger
logger = logging.getLogger(__name__)
# Open logger configuration file
logger_file = utils_os.read_local_json("ini/logger.json")
logging.config.dictConfig(logger_file)


def main():
    # Initialize value
    conf_file = None
    # Endpoint action as described from ckan platform docs
    # https://docs.ckan.org/en/2.8/api/index.html
    pack_action = "package_show"
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    in_value = _define_check_args(parser)
    logger.debug("Passed arguments: %s", in_value)
    if utils_os.simple_file_read(in_value["ini_file"]):
        conf_file = _parse_configuration_value(in_value["ini_file"])
    if conf_file is None:
        logger.error("sys.exiting with error, check you logs")
        sys.exit(1)
    logger.debug("Configuration values: %s", conf_file)
    # Mapping some value
    url = conf_file["api"]["url"]
    usr = conf_file["api"]["usr"]
    psw = conf_file["api"]["psw"]
    pack = conf_file["api"]["package"]
    save_dir = conf_file["path"]["saveIn"]
    log_dir = conf_file["path"]["logDirectory"]
    history_file = log_dir + pack + ".log"
    # Output some variable
    logger.info("API url: %s", url)
    logger.info("Download Package: %s", pack)
    logger.info("Saving data in folder: %s", save_dir)
    logger.info("Log folder: %s", log_dir)

    # Config value validation
    logger.warning("Validating user defined folders")
    if not utils.validate_path(conf_file["path"], "dir"):
        sys.exit(1)
    # If history file exist read it and store data in list
    data_files = []
    if utils_os.simple_file_read(history_file):
        logger.info("Datastore file exist reading archive")
        with open(history_file, 'r') as f:
            # TODO: Use json format to store/read more information
            # like download date
            data_files = f.read().splitlines()
            logger.debug("Stored data files: %s", data_files)
            f.close()

    # Getting resource information
    payload = {"id": pack}
    end_point = url + pack_action
    try:
        response = requests.get(
            end_point, auth=(usr, psw), params=payload, timeout=5)
    except Exception as e:
        logger.error("Download error: %s", e, exc_info=True)
        logger.error("No download performed")
        exit(1)
    if response.status_code != 200:
        logger.error("Unable to connect API endpoint: %s", end_point)
        logger.error("Status code: %s", response.status_code)
        sys.exit(1)
    data = response.json()
    logger.debug("JSON data: %s", data)

    resources = data["result"]["resources"]
    if utils.is_empty(resources):
        logger.info("No resource available for download")
        sys.exit(0)

    for res in resources:
        # Check if file is present in data_files (aka already downloaded)
        if res["name"] in data_files:
            logger.warning("Skipping file: %s", res["name"])
            continue
        logger.info("Downloading file: %s", res["name"])
        logger.debug("Download url: %s", res["url"])
        try:
            response = requests.get(
                res["url"], auth=(usr, psw), stream=True, timeout=5)
            dwl_file = save_dir + res["name"]
            handle = open(dwl_file, "wb")
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)
        except Exception as e:
            logger.error("Download error: %s", e, exc_info=True)
            logger.error("Download failed: %s", res["name"])
            continue
        # Updating log
        logger.debug("Appending file to log")
        # Open history file in append mode
        fh = open(history_file, "a")
        fh.write(res["name"] + "\n")
        # Closing history file
        fh.close()
    logger.info("All operation completed")
    sys.exit(0)


def _define_check_args(parser):
    ##############################################
    # This function parse argument variable, check format
    # and set default value.
    # Arguments:
    #   a parser from argparse module
    # Returns:
    #   a tuple
    ##############################################
    parser.add_argument("ini_file", help="Location of configuration file")
    args = parser.parse_args()

    args_value = {
        "ini_file": args.ini_file
    }
    return args_value


def _parse_configuration_value(ini_path):
    cfg = ConfigParser.SafeConfigParser()
    try:
        logger.info("Reading INI file: %s", ini_path)
        cfg.read(ini_path)
        logger.debug("Parsing INI values...")
        # Build dict from configuration file
        api = {
            'url': cfg.get("api", "url").strip("\""),
            'usr': cfg.get("api", "user").strip("\""),
            'psw': cfg.get("api", "password").strip("\""),
            'package': cfg.get("api", "package").strip("\"")
        }
        path = {
            'saveIn': cfg.get("path", "saveIn").strip("\""),
            'logDirectory': cfg.get("path", "logDirectory").strip("\"")
        }

    except ConfigParser.NoOptionError as err:
        # TODO: output with a logger handler
        logger.error("Missing option in INI file: %s", err)
        sys.exit(1)
    except ConfigParser.ParsingError as err:
        # TODO: output with a logger handler
        logger.error("Error parsing INI file: %s", err)
        sys.exit(1)

    logger.debug("All INI values acquired")
    config = {
        "api": api,
        "path": path
    }
    # Empty value are not allowed
    if utils.empty_value_in_dict(config):
        logger.error("There is an empty parameter in INI file")
        sys.exit(1)
    return config


if __name__ == ("__main__"):
    main()
