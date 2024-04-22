#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    # ### Built-in deps
    # ### Third-party deps
    import uvicorn

    # ### Local deps
    from app.config import get_app_config
    from app.middleware.rf_data_manager.run import run_rf_data_management
    from app.helpers import parse_arguments


    args = parse_arguments()
    settings = get_app_config()

    run_rf_data_management(settings)

    uvicorn.run("app.setup:app", host=args.host, port=args.port, reload=args.reload)
