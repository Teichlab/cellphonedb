#!/bin/bash

exec uwsgi --ini cellphonedb.ini --log-master
