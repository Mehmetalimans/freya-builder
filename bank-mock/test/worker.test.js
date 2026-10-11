import {test} from 'node:test';
import assert from 'node:assert/strict';
import dataset from '../test-customers.json' with {type: 'json'};
import worker from '../worker.js';

import {allCases} from '../contract-fixtures.js';

test('every supplied fixture returns the exact body and status, including the delayed response', async () => {
  let count = 0;
  for (const fixture of allCases()) {
    const started = Date.now();
    const response = await worker.fetch(new Request('https://mock.example' + fixture.path,
      {method: fixture.method, body: JSON.stringify(fixture.request_json)}));
    assert.equal(response.status, fixture.status, fixture.id);
    assert.deepEqual(await response.json(), fixture.response_json, fixture.id);
    if (fixture.delaySeconds) assert.ok(Date.now() - started >= fixture.delaySeconds * 1000 - 30);
    count++;
  }
  assert.equal(count, 617);
});

test('number customer identifiers match string identifiers', async () => {
  const first = dataset.customers[0];
  const response = await worker.fetch(new Request('https://mock.example/voice/v1/cards.list',
    {method:'POST',body:JSON.stringify({data:{customerNo:Number(first.customerNo)}})}));
  assert.deepEqual(await response.json(), first.services['cards.list'].response);
});

test('missing inputs and unknown records fail with documented code and no data', async () => {
  for (const [service,data,status,code] of [
    ['cards.balance',{},400,'INVALID_ARGUMENTS_ERROR'],
    ['cards.balance',{cardNumber:'unknown'},404,'FB_IVR_CHANNEL_120'],
    ['cards.list',{customerNo:'00000000'},404,'FB_IVR_CHANNEL_102'],
    ['statement.week.get',{cardNumber:'unknown'},404,'FB_IVR_CHANNEL_121'],
    ['statement.week.change',{cardNumber:'unknown',newStatementWeek:2,statementDay:5},400,'INVALID_ARGUMENTS_ERROR']]) {
    const response=await worker.fetch(new Request('https://mock.example/voice/v1/'+service,{method:'POST',body:JSON.stringify({data})}));
    const body=await response.json();assert.equal(response.status,status);assert.equal(body.result.returnCode,code);assert.equal(body.data,undefined);
  }
});
