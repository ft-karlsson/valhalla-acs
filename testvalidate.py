import json

class ValidateData:
    def __init__(self, validation_func):
        self.validation_func = validation_func

    def __call__(self, cls):
        setattr(cls, 'validate_data', self.validation_func)
        return cls


def validate_devices_data(cls, data):
    # Perform your validation logic here
    if "event" not in data or data["event"] != "0 BOOTSTRAP":
        raise ValueError("Invalid device data: missing or incorrect 'event' field")

    if "manufacturer" not in data:
        raise ValueError("Invalid device data: missing 'manufacturer' field")

    # Add more validation rules as needed


@ValidateData(validate_devices_data)
class Device:
    def __init__(self, data):
        self.validate_data(data)
        self.data = data

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __str__(self):
        return str(self.data)


device = Device.from_json('{"event":"0 BOOTSTRAP","manufacturer":"Techsome","oui":"6C0E01","parameters":{"Device.DeviceInfo.HardwareVersion":"3.0","Device.DeviceInfo.ProvisioningCode":"SE1936018000231","Device.DeviceInfo.SoftwareVersion":"ROUTERV3_NICEVERSION-FW-RDK_2.2.2","Device.DeviceSummary":"coaxdevice","Device.IP.Interface.1.IPv4Address.1.IPAddress":"10.0.1.8","Device.ManagementServer.AliasBasedAddressing":"0","Device.ManagementServer.ConnectionRequestURL":"http://10.0.0.8:7547/","Device.ManagementServer.ParameterKey":"1S4s32211235409811231566"},"product_class":"ROUTERV3","serialnumber":"SE1936018000231"}')

# Trying to create an instance with invalid data will raise a ValueError
device_invalid = Device.from_json('{"manufacturer":"Techsome","oui":"6C0E01"}')

# This will raise a ValueError: "Invalid device data: missing or incorrect 'event' field"
