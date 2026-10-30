'use strict';

const VENDORS = ['aws', 'gcp', 'azure', 'oci'];
const DAY = 86400000;
function iso(date) { return new Date(date).toISOString().slice(0, 10); }
function dateValue(s) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s) || iso(`${s}T00:00:00Z`) !== s) throw new Error('invalid progress date');
  return Date.parse(`${s}T00:00:00Z`);
}
function initialize(today, existing) {
  dateValue(today);
  if (existing) { validate(existing); return structuredClone(existing); }
  // The first monitored interval begins on the first day of the previous month;
  // anything earlier remains explicitly unknown, never inferred current.
  const d = new Date(`${today}T00:00:00Z`);
  return {version:1, started_on:iso(Date.UTC(d.getUTCFullYear(),d.getUTCMonth()-1,1)), before_start:'unverified', days:{}, attempted:{}};
}
function validate(progress) {
  if (!progress || progress.version !== 1 || progress.before_start !== 'unverified' || !progress.days || typeof progress.days !== 'object' || Array.isArray(progress.days)) throw new Error('invalid news progress');
  dateValue(progress.started_on);
  for (const [day, vendors] of Object.entries(progress.days)) {
    dateValue(day);
    if (!vendors || typeof vendors !== 'object' || Array.isArray(vendors)) throw new Error('invalid vendor progress');
    for (const [vendor, state] of Object.entries(vendors)) if (!VENDORS.includes(vendor) || !['complete','failed','provisional'].includes(state)) throw new Error('invalid vendor state');
  }
  if (progress.attempted !== undefined) {
    if (!progress.attempted || typeof progress.attempted !== 'object' || Array.isArray(progress.attempted)) throw new Error('invalid attempt history');
    for (const [day, vendors] of Object.entries(progress.attempted)) {
      dateValue(day);
      if (!vendors || typeof vendors !== 'object' || Array.isArray(vendors)) throw new Error('invalid attempt history');
      for (const [vendor, timestamp] of Object.entries(vendors)) if (!VENDORS.includes(vendor) || typeof timestamp !== 'string' || !Number.isFinite(Date.parse(timestamp))) throw new Error('invalid attempt timestamp');
    }
  }
}
function plan(progress, today, backlogLimit = 2) {
  validate(progress);
  const end = dateValue(today), start = dateValue(progress.started_on);
  if (start > end || backlogLimit < 0 || backlogLimit > 10) throw new Error('invalid news range');
  const dates = [];
  for (let t = start; t <= end; t += DAY) dates.push(iso(t));
  const recent = dates.slice(-2);
  const result = {};
  for (const vendor of VENDORS) {
    const backlog = dates.slice(0,-2).filter(day => progress.days[day]?.[vendor] !== 'complete');
    const order = (a,b) => (progress.attempted?.[a]?.[vendor] || '').localeCompare(progress.attempted?.[b]?.[vendor] || '') || a.localeCompare(b);
    const provisional = backlog.filter(day => progress.days[day]?.[vendor] === 'provisional').sort(order);
    const other = backlog.filter(day => progress.days[day]?.[vendor] !== 'provisional').sort(order);
    const selected = [];
    // Reserve capacity for both late-arrival rechecks and older outage recovery.
    if (backlogLimit && provisional.length) selected.push(provisional.shift());
    if (selected.length < backlogLimit && other.length) selected.push(other.shift());
    while (selected.length < backlogLimit && (provisional.length || other.length)) selected.push(provisional.length ? provisional.shift() : other.shift());
    result[vendor] = [...new Set([...selected, ...recent])];
  }
  return result;
}
function apply(progress, attempts, checkedAt = new Date().toISOString()) {
  const result = structuredClone(progress); validate(result);
  if (!Number.isFinite(Date.parse(checkedAt))) throw new Error('invalid checked time');
  result.attempted ||= {};
  for (const attempt of attempts) {
    dateValue(attempt.date);
    if (!VENDORS.includes(attempt.vendor) || !['complete','failed','provisional'].includes(attempt.state)) throw new Error('invalid attempt');
    result.days[attempt.date] ||= {};
    result.attempted[attempt.date] ||= {};
    result.attempted[attempt.date][attempt.vendor] = checkedAt;
    // A failed refresh means late-arriving releases may still be missing.
    result.days[attempt.date][attempt.vendor] = attempt.state;
  }
  return result;
}
function pending(progress, today) {
  validate(progress);
  let count = 0;
  for (let t = dateValue(progress.started_on); t <= dateValue(today); t += DAY) for (const v of VENDORS) if (progress.days[iso(t)]?.[v] !== 'complete') count++;
  return count;
}
function stateFor(day, today, truncated = false) {
  const age = (dateValue(today) - dateValue(day)) / DAY;
  if (age < 0) throw new Error('future source date');
  return truncated ? 'failed' : age < 7 ? 'provisional' : 'complete';
}
function parseResponse(data, limit) {
  if (data?.error || data?.result?.isError) throw new Error('MCP tool reported an error');
  const text = data?.result?.content?.[0]?.text;
  if (typeof text !== 'string') throw new Error('MCP response missing result text');
  const match = text.match(/\[[\s\S]*\]/);
  if (!match) throw new Error('MCP response missing JSON array');
  const rows = JSON.parse(match[0]);
  if (!Array.isArray(rows)) throw new Error('MCP result is not an array');
  const count = text.match(/(\d+)\s*건\s*중\s*(\d+)\s*건/);
  if (rows.length >= limit || (count && Number(count[1]) > Number(count[2]))) {
    const error = new Error('MCP result may be truncated; date remains unverified');
    error.partialRows = rows;
    throw error;
  }
  return rows;
}
module.exports = {VENDORS, initialize, validate, plan, apply, pending, parseResponse, stateFor};
