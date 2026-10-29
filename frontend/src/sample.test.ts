import {describe,it,expect} from 'vitest';
import {sampleSources,sampleDraft} from './sample';
describe('reproducible editorial handoff',()=>{
 it('includes three distinct attributed demo sources',()=>{expect(sampleSources).toHaveLength(3);expect(new Set(sampleSources.map(s=>s.url)).size).toBe(3);expect(sampleSources.every(s=>s.content.startsWith('FICTIONAL DEMO SOURCE.'))).toBe(true);});
 it('supplies a 300–500 word draft and all three writing check candidates',()=>{const words=sampleDraft.trim().split(/\s+/).length;expect(words).toBeGreaterThanOrEqual(300);expect(words).toBeLessThanOrEqual(500);expect(sampleDraft).toContain('in order to');expect(sampleDraft).toContain('was conducted');expect(sampleDraft).toContain('fictional');});
});
