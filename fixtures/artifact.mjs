// ReleaseOrigin release helper v1.0.0. ASCII-only canonical JSON for receipt hashing.
import {createHash} from 'node:crypto';
export function canonical(value) {
  const sort = v => Array.isArray(v) ? v.map(sort) : v && typeof v === 'object'
    ? Object.fromEntries(Object.keys(v).sort().map(k => [k, sort(v[k])])) : v;
  return JSON.stringify(sort(value)).replace(/[\u007f-\uffff]/g,
    c => '\\u' + c.charCodeAt(0).toString(16).padStart(4,'0'));
}
export const digest = value => createHash('sha256').update(canonical(value)).digest('hex');
