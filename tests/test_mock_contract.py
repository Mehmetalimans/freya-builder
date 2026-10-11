import io
import unittest
import urllib.error
from scripts.check_mock import run_checks, validate_fixture
from builder.core import ContractError


class Response(io.BytesIO):
    status = 200


class FakeOpener:
    def __init__(self, response): self.response = response
    def open(self, req, timeout):
        if isinstance(self.response, Exception): raise self.response
        return Response(self.response)


class MockContractTests(unittest.TestCase):
    def fixture(self):
        return {'id':'lookup','source':'service.md section 2','method':'POST','path':'/items',
                'request_json':{'item':'book'},'response_json':{'available':False},'status':200}

    def test_exact_response_not_truthiness(self):
        self.assertTrue(run_checks('https://library.example',[self.fixture()],FakeOpener(b'{"available":false}'))[0]['pass'])
        self.assertFalse(run_checks('https://library.example',[self.fixture()],FakeOpener(b'{"available":true}'))[0]['pass'])

    def test_error_status_is_part_of_contract(self):
        fixture=self.fixture(); fixture.update(status=404,response_json={'error':'missing'})
        error=urllib.error.HTTPError('https://library.example/items',404,'missing',{},io.BytesIO(b'{"error":"missing"}'))
        self.assertTrue(run_checks('https://library.example',[fixture],FakeOpener(error))[0]['pass'])

    def test_external_path_is_rejected(self):
        fixture=self.fixture();fixture['path']='//other.example/items'
        with self.assertRaises(ContractError): validate_fixture(fixture)


if __name__ == '__main__': unittest.main()
