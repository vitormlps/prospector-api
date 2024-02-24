#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from multiprocessing import Process

# ### Third-party deps
# ### Local deps
from .manager import ReceitaFederalDataManager


def run_rf_data_collection(settings):
    manager = ReceitaFederalDataManager()
    runner = Process(target=manager.start, args=(settings))
    
    runner.start()
    return runner.join()