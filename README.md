# Mikrotik Dropbox Backup Uploader

This script read the config.json file and then export the configuration of given Mikrotik routers to a dropbox account associated by the given key.

This script is being used in production with RouterOS 6x by the time of upload.

## Package requirements

All the dependencies can by installed via pip.

* Paramiko
* Dropbox

## How to use this script

* Get a Dropbox API key
* Populate the config.json file as the example
* Optionally you can use a cron job to run this script