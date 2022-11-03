#!/bin/bash
cd /home/eteillet/Documents/job_scraper_/ && \
/home/eteillet/miniconda3/bin/python3 scraper.py && \
/home/eteillet/miniconda3/bin/python3 sender.py && \
rm results.json