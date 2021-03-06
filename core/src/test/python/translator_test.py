"""
Copyright (c) 2017, 2018, Oracle and/or its affiliates. All rights reserved.
The Universal Permissive License (UPL), Version 1.0
"""
import javaos as os
import unittest

from wlsdeploy.util.model_translator import FileToPython, PythonToFile

class TranslatorTestCase(unittest.TestCase):
    _execution_dir = '../../unit-tests/'
    _resources_dir = '../../test-classes/'

    _src_json_file = os.path.join(_resources_dir, 'quote-test.json')
    _src_yaml_file = os.path.join(_resources_dir, 'quote-test.yaml')

    _target_json_file = os.path.join(_execution_dir, 'quote-test.json')
    _target_yaml_file = os.path.join(_execution_dir, 'quote-test.yaml')

    def setUp(self):
        self.name = 'TranslatorTestCase'
        if not os.path.exists(self._execution_dir):
            os.makedirs(self._execution_dir)

    def testJsonToPython(self):
        translator = FileToPython(self._src_json_file, use_ordering=True)
        pythonDict = translator.parse()

        self.assertNotEqual(pythonDict, None)
        self.assertEqual(len(pythonDict), 2)

        quotedValue = pythonDict['foo']
        self.assertEqual(quotedValue, 'this is a "legal" JSON value')

        self.assertEqual('keys "can" have quotes too' in pythonDict, True)
        quotedKeyValue = pythonDict['keys "can" have quotes too']
        self.assertEqual(quotedKeyValue, 123)

    def testPythonToJson(self):
        pythonDict = dict()
        pythonDict['foo'] = 'this is a "legal" JSON value'
        pythonDict['keys "can" have quotes too'] = 123

        translator = PythonToFile(pythonDict)
        translator.write_to_file(self._target_json_file)

        translator = FileToPython(self._target_json_file)
        newPythonDict = translator.parse()

        self.assertEqual('foo' in newPythonDict, True)
        self.assertEqual('keys "can" have quotes too' in newPythonDict, True)
        self.assertEqual(newPythonDict['foo'], 'this is a "legal" JSON value')
        self.assertEqual(newPythonDict['keys "can" have quotes too'], 123)

    def testYamlToPython(self):
        translator = FileToPython(self._src_yaml_file, use_ordering=True)
        pythonDict = translator.parse()

        self.assertNotEqual(pythonDict, None)
        self.assertEqual(len(pythonDict), 3)

        quotedValue = pythonDict['foo']
        self.assertEqual(quotedValue, 'test \'legal\' yaml')

        quotedValue = pythonDict['bar']
        self.assertEqual(quotedValue, 'test "legal" yaml')

        quotedValue = pythonDict['baz']
        self.assertEqual(quotedValue, 'test \'legal\' yaml')

    def testPythonToYaml(self):
        pythonDict = dict()
        pythonDict['foo'] = 'test \'legal\' yaml'
        pythonDict['bar'] = 'test "legal" yaml'
        pythonDict['baz'] = 'test \'legal\' yaml'

        translator = PythonToFile(pythonDict)
        translator.write_to_file(self._target_yaml_file)

        translator = FileToPython(self._target_yaml_file, use_ordering=True)
        newPythonDict = translator.parse()

        self.assertEqual('foo' in newPythonDict, True)
        self.assertEqual('bar' in newPythonDict, True)
        self.assertEqual('baz' in newPythonDict, True)

        quotedValue = newPythonDict['foo']
        self.assertEqual(quotedValue, 'test \'legal\' yaml')
        quotedValue = newPythonDict['bar']
        self.assertEqual(quotedValue, 'test "legal" yaml')
        quotedValue = newPythonDict['baz']
        self.assertEqual(quotedValue, 'test \'legal\' yaml')
