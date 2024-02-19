#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
import argparse

# ### Third-party deps
# ### Local deps


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='output',
        description="Pix Quality's API for receiving internal data and distributing externally.",
        allow_abbrev=True
    )
    parser = add_arguments(parser)

    return parser.parse_args()


def add_arguments(parser):
    parser.add_argument(
        "-cf", "--cert-file",
        help="SSL certificate file (for HTTPS)"
    )
    parser.add_argument(
        "-kf", "--key-file", 
        help="SSL key file (for HTTPS)"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "-p", "--port", 
        type=int, 
        default=8000, 
        help="Port for HTTP server (default: 8000)"
    )
    parser.add_argument(
        '--reload',
        default=True,
        help='Sets Uvicorn to reload on changes',
    )

    return parser