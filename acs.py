from datamodel import send_kafka_message
"""
acs
~~~~~~~~~~~~~~~~~
This module contains specific functions for the auto-configuration for devices including ingestion of devices
"""

async def ingest_device(parsed_inform: dict) -> bool:
    # TODO: do some validation of data keys
    parsed_inform['serialnumber']
    await send_kafka_message("acs_devices", parsed_inform, parsed_inform['serialnumber'])

