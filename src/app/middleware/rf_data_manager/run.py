#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from threading import Thread

# ### Third-party deps
# ### Local deps
from app.setup import setup_database, setup_helpers
from .manager import ReceitaFederalDataManager


def run_rf_data_management(settings):
    setup_helpers(settings)
    setup_database(settings)

    manager = ReceitaFederalDataManager()
    runner = Thread(target=manager.start, args=([settings]))
    
    runner.start()
    runner.join()
