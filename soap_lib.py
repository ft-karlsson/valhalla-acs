from lxml import etree



def parse_inform(xml_string):
    # Parse the SOAP XML
    root = etree.fromstring(xml_string)

    # Define namespaces
    namespaces = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'soap-enc': 'http://schemas.xmlsoap.org/soap/encoding/',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsd': 'http://www.w3.org/2001/XMLSchema',
        'cwmp': 'urn:dslforum-org:cwmp-1-0'
    }

    # Extract values with modified XPath expressions
    manufacturer_elem = root.find('.//DeviceId/Manufacturer')
    manufacturer = manufacturer_elem.text if manufacturer_elem is not None else None

    oui_elem = root.find('.//DeviceId/OUI')
    oui = oui_elem.text if oui_elem is not None else None

    product_class_elem = root.find('.//DeviceId/ProductClass')
    product_class = product_class_elem.text if product_class_elem is not None else None

    serial_number_elem = root.find('.//DeviceId/SerialNumber')
    serial_number = serial_number_elem.text if serial_number_elem is not None else None

    event_elem = root.find('.//Event/EventStruct/EventCode')
    event = event_elem.text if event_elem is not None else None

    parameter_list = root.xpath('//ParameterList/ParameterValueStruct', namespaces=namespaces)

    parameters = {}
    for param in parameter_list:
        name = param.findtext('Name', namespaces=namespaces)
        value = param.findtext('Value', namespaces=namespaces)
        parameters[name] = value

    # Return the data in a dict
    return {
        'manufacturer': manufacturer,
        'oui': oui,
        'product_class': product_class,
        'serialnumber': serial_number,
        'event': event,
        "parameters": parameters
    }
