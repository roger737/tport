from flask import Flask

# Import all lab modules here and expose helper functions
from . import (
    broken_access_control,
    cryptographic_failures,
    injection,
    insecure_design,
    security_misconfiguration,
    vulnerable_components,
    identification_authentication_failures,
    data_integrity_failures,
    logging_monitoring_failures,
    ssrf,
)

ALL_LABS = [
    broken_access_control,
    cryptographic_failures,
    injection,
    insecure_design,
    security_misconfiguration,
    vulnerable_components,
    identification_authentication_failures,
    data_integrity_failures,
    logging_monitoring_failures,
    ssrf,
]

def register_all(app: Flask):
    for module in ALL_LABS:
        app.register_blueprint(module.bp)


def get_lab_info():
    return [module.metadata for module in ALL_LABS]
