// Mock only: task-specific contract and synthetic fixtures belong here, never in the builder.
import dataset from './test-customers.json' with { type: 'json' };

const customers = new Map(dataset.customers.map(c => [String(c.customerNo), c]));
const cards = new Map();
for (const customer of dataset.customers) {
  for (const card of Object.keys(customer.services['cards.balance'] || {})) {
    if (cards.has(card)) throw new Error('Fixture card lookup is ambiguous');
    cards.set(card, customer);
  }
}
const required = {
  'cards.list': ['customerNo'],
  'cards.balance': ['cardNumber'],
  'statement.week.get': ['cardNumber'],
  'statement.week.decide': ['cardNumber', 'newStatementWeek', 'statementDay'],
  'statement.week.change': ['cardNumber', 'newStatementWeek', 'statementDay'],
  'contact.email.get': ['customerNo', 'intAddressInfoType'],
  'statement.pdf.send': ['customerNo', 'cardNumber', 'currencyType', 'statementDate', 'emailAddress']
};
const missingCodes = {
  'cards.list': ['FB_IVR_CHANNEL_102', 'Müşteriye ait geçerli kart bilgisi bulunamadı.'],
  'cards.balance': ['FB_IVR_CHANNEL_120', 'Kart bakiye servisi hatası: kart bulunamadı'],
  'statement.week.get': ['FB_IVR_CHANNEL_121', 'Kart bulunamadı'],
  'statement.pdf.send': ['FB_IVR_CHANNEL_107', 'Pdf dokümanı bulunamadı']
};

function json(value, status = 200) {
  return new Response(JSON.stringify(value), {status, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store'}});
}

function error(code, message, status = 400, type = 'ERROR') {
  const guid = crypto.randomUUID().replaceAll('-', '');
  return json({result: {guid, returnCode: code, messageText: message, code, message, type,
    details: {guid, rootCause: status === 404 ? 'NotFoundException' : 'InvalidArguments', errorOrigin: 'mock-test'}}}, status);
}

export function selectFixture(service, data) {
  const byCustomer = ['cards.list', 'contact.email.get', 'statement.pdf.send'].includes(service);
  const customer = byCustomer ? customers.get(String(data.customerNo)) : cards.get(data.cardNumber);
  if (!customer) return undefined;
  const entry = customer.services[service];
  if (byCustomer) return entry;
  if (service === 'statement.week.decide' || service === 'statement.week.change') {
    return entry?.[data.cardNumber]?.[String(data.newStatementWeek)];
  }
  return entry?.[data.cardNumber];
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method === 'GET' && url.pathname === '/health') {
      return json({status: 'ok', customers: customers.size, version: '1.0.0'});
    }
    const service = url.pathname.startsWith('/voice/v1/') ? url.pathname.slice('/voice/v1/'.length) : '';
    if (!Object.hasOwn(required, service)) return error('INVALID_ARGUMENTS_ERROR', 'Unknown service', 404);
    if (request.method !== 'POST') return error('INVALID_ARGUMENTS_ERROR', 'POST required', 405);
    let payload;
    try { payload = await request.json(); } catch { return error('INVALID_ARGUMENTS_ERROR', 'JSON body required'); }
    const data = payload?.data;
    if (!data || typeof data !== 'object' || Array.isArray(data)) return error('INVALID_ARGUMENTS_ERROR', 'data cannot be empty');
    for (const field of required[service]) {
      if (data[field] === undefined || data[field] === null || String(data[field]).trim() === '') {
        return error('INVALID_ARGUMENTS_ERROR', `${field} cannot be empty`);
      }
    }
    const fixture = selectFixture(service, data);
    if (!fixture) {
      const known = missingCodes[service];
      return known ? error(known[0], known[1], 404, 'WARNING')
        : error('INVALID_ARGUMENTS_ERROR', 'Requested test record not found');
    }
    if (fixture.delaySeconds) await new Promise(resolve => setTimeout(resolve, fixture.delaySeconds * 1000));
    // Return the supplied body unchanged, including result fields, nulls and expected failures.
    return json(fixture.response, fixture.http);
  }
};
