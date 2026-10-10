"""Input-derived calendar arithmetic for an explicitly recognized policy definition."""
import json
import re
from datetime import date


MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def parse_iso_and_natural_dates(text):
    dates = set(re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", text))
    for y, m, d in re.findall(r"\b(\d{4})[./](\d{1,2})[./](\d{1,2})\b", text):
        try:
            dates.add(f"{int(y):04d}-{int(m):02d}-{int(d):02d}")
        except ValueError:
            pass
    for m, d, y in re.findall(r"\b([A-Za-z]{3,9})\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s*|\s+)(\d{4})\b", text):
        month = MONTH_MAP.get(m.lower())
        if month:
            try:
                dates.add(f"{int(y):04d}-{month:02d}-{int(d):02d}")
            except ValueError:
                pass
    for d, m, y in re.findall(r"\b(\d{1,2})(?:st|nd|rd|th)?(?:\s+of)?\s+([A-Za-z]{3,9})(?:,?\s*|\s+)(\d{4})\b", text):
        month = MONTH_MAP.get(m.lower())
        if month:
            try:
                dates.add(f"{int(y):04d}-{month:02d}-{int(d):02d}")
            except ValueError:
                pass
    valid = []
    for s in dates:
        try:
            valid.append(date.fromisoformat(s).isoformat())
        except ValueError:
            pass
    return sorted(set(valid))


def calendar_spec(briefs):
    # Conservative grammar: do not guess a calendar from examples or customer cases.
    pattern = r"Business days are Monday\s*(?:to|through|-)\s*Friday,?\s*(?:except|excluding)\s*[^\n:]*holidays?:\s*([^\n]+)"
    matches = [m for _, text in briefs for m in re.finditer(pattern, text, re.I)]
    if not matches:
        pattern_fallback = r"(?:bank|public)\s+holidays?(?:\s+to\s+skip)?(?:\s+are)?:\s*([^\n]+)"
        matches = [m for _, text in briefs for m in re.finditer(pattern_fallback, text, re.I)]
    if not matches:
        holiday_lines = [line for _, text in briefs for line in text.splitlines() if re.search(r"\bholiday", line, re.I)]
        holidays = parse_iso_and_natural_dates("\n".join(holiday_lines))
        if holidays:
            return {"holidays": holidays, "source": "extracted_holidays", "horizon_days": 90}
        return None
    holidays = parse_iso_and_natural_dates(matches[-1].group(1))
    if not holidays:
        return None
    return {"holidays": holidays, "source": matches[-1].group(0), "horizon_days": 90}


def calendar_code(spec):
    return '''import datetime
try:
    today = datetime.date.fromisoformat(str(vars.get('now', ''))[:10])
    holidays = set(HOLIDAY_LIST)
    monday = today - datetime.timedelta(days=today.weekday())
    lines = ['CALL TODAY: ' + today.isoformat() + ' ' + today.strftime('%A')]
    for week, offset in [('THIS calendar week', 0), ('NEXT calendar week', 7)]:
        lines.append(week + ': ' + ', '.join((monday + datetime.timedelta(days=offset+i)).strftime('%A %Y-%m-%d') for i in range(7)))
    ordinal = 0
    for offset in range(91):
        day = today + datetime.timedelta(days=offset)
        business = day.weekday() < 5 and day.isoformat() not in holidays
        if business and offset > 0:
            ordinal += 1
        label = ('business day AFTER today #' + str(ordinal)) if business and offset > 0 else ('TODAY business day' if business else 'NON-BUSINESS DAY')
        if not business:
            successor = day + datetime.timedelta(days=1)
            while successor.weekday() >= 5 or successor.isoformat() in holidays:
                successor += datetime.timedelta(days=1)
            label += '; NEXT BUSINESS DAY = ' + successor.isoformat() + ' ' + successor.strftime('%A')
        lines.append(day.isoformat() + ' ' + day.strftime('%A') + ' | ' + label)
    vars['calendar_facts'] = '\\n'.join(lines)
except Exception:
    vars['calendar_facts'] = 'Calendar calculation unavailable. Use only call now and supplied policy; never the real clock.'
'''.replace('HOLIDAY_LIST', json.dumps(spec['holidays']))


def calendar_node(spec, target):
    return {"name": "calendar_setup", "node_type": "code", "passthrough": True,
            "passthrough_default_transition": target, "on_enter": {"type": "silent"},
            "pre_actions": [{"type": "function", "function": {"name": "code_exec",
                "handler": "__function__:code_exec", "description": "", "parameters": {"type": "object", "properties": {
                    "code": {"type": "string", "default": calendar_code(spec)},
                    "timeout_ms": {"type": "number", "default": 10000}}}}}],
            "transitions": [{"target_node": target, "description": "Calendar facts prepared",
                             "condition": {"operator": "always", "mode": "exact"}}]}


def deadline_bands(briefs):
    rows = {}
    for _, text in briefs:
        for low, high, count in re.findall(r"\|\s*(\d+)\s*(?:to|-)\s*(\d+)\s*\|[^|\n]+\|\s*(?:the\s+|within\s+)?(\d+)(?:st|nd|rd|th)?\s+(?:business|working)\s+days?(?:\s+after\s+(?:today|call\s+date|now))?\s*\|", text, re.I):
            low, high, count = int(low), int(high), int(count)
            if not 0 <= low <= high or not 1 <= count <= 60:
                return None
            rows[(low, high)] = count
    bands = [[low, high, count] for (low, high), count in sorted(rows.items())]
    if not bands or any(a[1] >= b[0] for a, b in zip(bands, bands[1:])):
        return None
    return bands


def offer_code(spec, bands):
    return '''import datetime
try:
    vars['payment_offer_action'] = 'none'
    today = datetime.date.fromisoformat(str(vars.get('now', ''))[:10])
    offered = datetime.date.fromisoformat(str(vars.get('payment_offer_date', ''))[:10])
    holidays = set(HOLIDAY_LIST)
    bands = BAND_LIST
    def business(day):
        return day.weekday() < 5 and day.isoformat() not in holidays
    shifted = offered
    while not business(shifted):
        shifted += datetime.timedelta(days=1)
    lines = ['EXACT CUSTOMER OFFER: ' + offered.isoformat() + ' ' + offered.strftime('%A'),
             'OFFER IS BUSINESS DAY: ' + str(business(offered)),
             'NEXT VALID BUSINESS DATE ON OR AFTER OFFER: ' + shifted.isoformat() + ' ' + shifted.strftime('%A')]
    products = []
    raw_prods = vars.get('get_account_response.data.products')
    if isinstance(raw_prods, list):
        for p in raw_prods:
            if isinstance(p, dict) and 'product_id' in p:
                products.append((p.get('product_id'), p.get('days_late', 0)))
    if not products:
        for i in range(200):
            p_id = vars.get('get_account_response.data.products.' + str(i) + '.product_id')
            if p_id is None:
                break
            d_late = vars.get('get_account_response.data.products.' + str(i) + '.days_late', 0)
            products.append((p_id, d_late))
    for product, late_val in products:
        late = int(late_val)
        counts = [count for low, high, count in bands if low <= late <= high]
        if len(counts) != 1:
            lines.append('PRODUCT ' + str(product) + ': deadline not computed; consult policy.')
            continue
        deadline, count = today, 0
        while count < counts[0]:
            deadline += datetime.timedelta(days=1)
            count += int(business(deadline))
        within = today <= offered <= deadline
        usable = within and shifted <= deadline
        lines.append('PRODUCT ' + str(product) + ': days_late=' + str(late) + '; DEADLINE=' + deadline.isoformat() + '; OFFER_WITHIN_WINDOW=' + str(within) + '; SHIFTED_WITHIN_WINDOW=' + str(usable))
        if usable:
            lines.append('DATE TO OFFER FOR THIS PRODUCT: ' + shifted.isoformat() + ' ' + shifted.strftime('%A') + '. This preserves the customer offer with any required business-day adjustment. Do not substitute the deadline.')
        else:
            lines.append('The customer offer is outside the allowed window. Policy deadline option: ' + deadline.isoformat() + ' ' + deadline.strftime('%A') + '. Apply the supplied refusal or multi-product rule.')
    vars['payment_date_facts'] = '\\n'.join(lines)
except Exception:
    vars['payment_offer_action'] = 'none'
    vars['payment_date_facts'] = 'Exact date calculation unavailable; ask the customer to clarify rather than inventing a date.'
'''.replace('HOLIDAY_LIST', json.dumps(spec['holidays'])).replace('BAND_LIST', json.dumps(bands))


def offer_node(spec, bands):
    node = calendar_node(spec, 'date_reply')
    node['name'] = 'date_offer'
    node['pre_actions'][0]['function']['parameters']['properties']['code']['default'] = offer_code(spec, bands)
    return node


def offer_extraction():
    prompt = ("{{extractor.type_preamble}}\nCALL NOW is {{now}}. Use only that date as the anchor, never the real date. "
              "Extract a specific PAYMENT date from the latest customer utterance and recent dialogue. "
              "If it is a day of month without a month, use the month indicated by call now and the dialogue. "
              "Next weekday means the following calendar week. Vague periods like next week are NOT exact dates. "
              "Set payment_offer_action to resolve only for an explicit payment date or corrected date. "
              "For yes/no, unrelated dates, identity details or vague periods set payment_offer_action to none. "
              "Do not extract dates merely quoted by the assistant unless the customer explicitly changes them. "
              "Latest speech: {{extractor.speech}}\nRecent dialogue: {{extractor.conversation.last-10}}\n"
              "Variables: {{extractor.variables_list}}")
    return [{"name": "payment_offer_date", "type": "date", "min_confidence": 0.5,
             "description": "Exact date explicitly proposed by the customer for payment, anchored to call now.",
             "extraction_prompt": prompt},
            {"name": "payment_offer_action", "type": "string", "min_confidence": 0.5,
             "enum_values": ["resolve", "none"], "description": "resolve only if latest customer utterance explicitly proposes or corrects an exact payment date; otherwise none."}]
