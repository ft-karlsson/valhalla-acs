import unittest

from cwmp_lib.soap import parse_inform

class TestStringMethods(unittest.TestCase):
    def test_parse(self):
        
        # Read SOAP XML from file
        with open('tests/device_soap_inform.xml', 'r') as file:
            xml_string = file.read()
        
        parsed_data = parse_inform(xml_string)

        self.assertEqual(parsed_data['manufacturer'], 'Techsome')
        self.assertEqual(parsed_data['oui'], '6C0E01')
        self.assertEqual(parsed_data['product_class'], 'ROUTERV3')
        self.assertEqual(parsed_data['serialnumber'], 'SE1936018000231')

    def test_parse_paramer(self):       
        with open('tests/device_soap_inform.xml', 'r') as file:
            xml_string = file.read()

        parsed_data = parse_inform(xml_string)
        self.assertEqual(parsed_data['parameters']['Device.DeviceInfo.SoftwareVersion'], "ROUTERV3_NICEVERSION-FW-RDK_2.2.2")

if __name__ == '__main__':
    unittest.main()
