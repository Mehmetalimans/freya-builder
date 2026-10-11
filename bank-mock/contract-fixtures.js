import dataset from './test-customers.json' with {type: 'json'};
export function allCases() {
  const cases = [];
  for (const customer of dataset.customers) {
    for (const [service, entries] of Object.entries(customer.services)) {
      const push = (data, fixture, label) => cases.push({id: `${customer.customerNo}/${service}/${label}`,
        path: `/voice/v1/${service}`, method: 'POST', source: 'test-environment/test-customers.json',
        request_json: {data, call: {lang: 'tr'}}, status: fixture.http, response_json: fixture.response,
        delaySeconds: fixture.delaySeconds || 0});
      if (['cards.list', 'contact.email.get', 'statement.pdf.send'].includes(service)) {
        const card = Object.keys(customer.services['cards.balance'] || {})[0] || 'unavailable';
        const balance = customer.services['cards.balance']?.[card]?.response?.data;
        push({customerNo: customer.customerNo, aiFlow: 'CardOps', intAddressInfoType: 'E', cardNumber: card,
          currencyType: 'TL', statementDate: balance?.statementDate || '01.10.2026',
          emailAddress: customer.services['contact.email.get']?.response?.data?.ibanEmail || 'missing@example.invalid'}, entries, 'customer');
      } else {
        for (const [cardNumber, entry] of Object.entries(entries)) {
          if (service === 'statement.week.decide' || service === 'statement.week.change') {
            const statementDay = customer.services['statement.week.get']?.[cardNumber]?.response?.data?.statementDay || 1;
            for (const [week, fixture] of Object.entries(entry)) push({cardNumber, newStatementWeek: Number(week), statementDay}, fixture, `${cardNumber}/${week}`);
          } else push({cardNumber}, entry, cardNumber);
        }
      }
    }
  }
  return cases;
}
