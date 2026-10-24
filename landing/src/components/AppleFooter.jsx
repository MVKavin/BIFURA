import React from 'react';
import { APP_CONFIG } from '../config/appConfig';

export default function AppleFooter({ setActivePage }) {
  return (
    <footer className="bg-[#04110c] text-[#8ea398] border-t border-emerald-900/40 pt-16 pb-12 px-4 sm:px-8 select-none text-[12px] font-normal leading-normal font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Footnotes / Disclaimers */}
        <div className="pb-8 border-b border-emerald-900/30 space-y-2 text-[#6b8478] text-[11px] leading-[1.43]">
          <p>
            1. Earliest divergence detection benchmarks calculated across 14,000,000 production traces spanning LangGraph, CrewAI, AutoGen, and custom multi-agent loops. Average MTTD reduction of 89% observed versus standard post-mortem exception handlers.
          </p>
          <p>
            2. Safety policy evaluation latency (&lt; 14ms) tested on dual-redundant European edge nodes and private AWS/GCP enclaves. Pass-through actions (ALLOW) complete within 1.2ms without inference blocking.
          </p>
          <p>
            3. Deterministic replay harnesses require state snapshots and frozen mock fixtures. Available for self-hosted sovereign clouds, private VPCs, and air-gapped defense enclaves.
          </p>
        </div>

        {/* 5-Column Directory */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-8 py-10 border-b border-emerald-900/30">
          
          {/* Col 1 */}
          <div>
            <h5 className="font-semibold text-white text-[12px] mb-2.5">Explore BIFURA</h5>
            <ul className="space-y-2 text-[#8ea398]">
              <li><button onClick={() => setActivePage('overview')} className="hover:text-white transition-colors">BIFURA Platform</button></li>
              <li><button onClick={() => setActivePage('intelligence')} className="hover:text-white transition-colors">Root-Cause Pinpointing</button></li>
              <li><button onClick={() => setActivePage('intelligence')} className="hover:text-white transition-colors">Blast Radius Mapping</button></li>
              <li><button onClick={() => setActivePage('safety')} className="hover:text-white transition-colors">Safety Engine</button></li>
              <li><button onClick={() => setActivePage('replay')} className="hover:text-white transition-colors">Deterministic Replay</button></li>
              <li><button onClick={() => setActivePage('buy')} className="hover:text-white transition-colors">Enterprise Spec</button></li>
            </ul>
          </div>

          {/* Col 2 */}
          <div>
            <h5 className="font-semibold text-white text-[12px] mb-2.5">Safety & Policy</h5>
            <ul className="space-y-2 text-[#8ea398]">
              <li><button onClick={() => setActivePage('safety')} className="hover:text-white transition-colors">Tri-State Gatekeeper</button></li>
              <li><button onClick={() => setActivePage('safety')} className="hover:text-white transition-colors">ALLOW / REVIEW / BLOCK</button></li>
              <li><button onClick={() => setActivePage('safety')} className="hover:text-white transition-colors">EU AI Act (Art. 14)</button></li>
              <li><button onClick={() => setActivePage('safety')} className="hover:text-white transition-colors">Zero-Data Corruption</button></li>
              <li><button onClick={() => setActivePage('enterprise')} className="hover:text-white transition-colors">GDPR & PII Sanitization</button></li>
            </ul>
          </div>

          {/* Col 3 */}
          <div>
            <h5 className="font-semibold text-white text-[12px] mb-2.5">Verification & CI/CD</h5>
            <ul className="space-y-2 text-[#8ea398]">
              <li><button onClick={() => setActivePage('replay')} className="hover:text-white transition-colors">Automated Patch Synthesis</button></li>
              <li><button onClick={() => setActivePage('replay')} className="hover:text-white transition-colors">Regression Test Harness</button></li>
              <li><button onClick={() => setActivePage('replay')} className="hover:text-white transition-colors">Synthetic Mock Fixtures</button></li>
              <li><button onClick={() => setActivePage('replay')} className="hover:text-white transition-colors">OpenTelemetry SDK</button></li>
              <li><button onClick={() => setActivePage('buy')} className="hover:text-white transition-colors">Developer Quickstart</button></li>
            </ul>
          </div>

          {/* Col 4 */}
          <div>
            <h5 className="font-semibold text-white text-[12px] mb-2.5">Enterprise & Trust</h5>
            <ul className="space-y-2 text-[#8ea398]">
              <li><button onClick={() => setActivePage('enterprise')} className="hover:text-white transition-colors">Security Whitepaper</button></li>
              <li><button onClick={() => setActivePage('enterprise')} className="hover:text-white transition-colors">SOC 2 Type II Certification</button></li>
              <li><button onClick={() => setActivePage('enterprise')} className="hover:text-white transition-colors">ISO 27001:2022 Audit</button></li>
              <li><button onClick={() => setActivePage('buy')} className="hover:text-white transition-colors">Air-Gapped Enclaves</button></li>
              <li><button onClick={() => setActivePage('buy')} className="hover:text-white transition-colors">SLA Guarantees (99.99%)</button></li>
            </ul>
          </div>

          {/* Col 5 */}
          <div>
            <h5 className="font-semibold text-white text-[12px] mb-2.5">About BIFURA</h5>
            <ul className="space-y-2 text-[#8ea398]">
              <li><span className="text-[#6b8478]">Paris & Frankfurt R&amp;D</span></li>
              <li><span className="text-[#6b8478]">Autonomous Agent Research</span></li>
              <li><span className="text-[#6b8478]">Counterfactual Reasoning</span></li>
              <li><span className="text-[#6b8478]">Contact Security Team</span></li>
              <li><span className="text-[#6b8478]">Status: All Systems Normal</span></li>
              <li>
                <a
                  href={APP_CONFIG.appUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-emerald-400 hover:text-white transition-colors font-mono"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Console: localhost:{APP_CONFIG.port} ↗</span>
                </a>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Baseline Copyright & Legal */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-[#6b8478] text-[11px]">
          <div>
            Copyright © {new Date().getFullYear()} BIFURA Inc. All rights reserved. One mistake. Many consequences. One verified fix.
          </div>
          <div className="flex items-center gap-4">
            <span className="hover:text-[#8ea398] cursor-pointer">Privacy Policy</span>
            <span>•</span>
            <span className="hover:text-[#8ea398] cursor-pointer">Terms of Service</span>
            <span>•</span>
            <span className="hover:text-[#8ea398] cursor-pointer">EU AI Compliance</span>
          </div>
        </div>

      </div>
    </footer>
  );
}