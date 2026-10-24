import React from 'react';
import BifuraPortal from '@/components/ui/demo';
import { ArrowRight, ArrowUpRight, ShieldCheck, CheckCircle2, Zap } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function OverviewPage({ setActivePage, onOpenDemo }) {
  return (
    <div className="select-none font-sans">
      
      {/* ============================================================ */}
      {/* 1. SCROLL-DRIVEN GLYPH PORTAL ENTRY ANIMATION                 */}
      {/* White opening canvas -> Camera zooms through BIFURA letter    */}
      {/* ============================================================ */}
      <BifuraPortal onOpenDemo={onOpenDemo}>
        
        {/* ============================================================ */}
        {/* 2. REVEALED WEBSITE WORLD                                    */}
        {/* Slowly transitions from deep letter green into Mint Green    */}
        {/* ============================================================ */}
        <div
          className="w-full relative overflow-hidden"
          style={{
            background: `linear-gradient(
              180deg,
              #0b3b2a 0%,
              #124935 80px,
              #1c5f44 180px,
              #2e7c58 300px,
              #49a374 440px,
              #6ec797 600px,
              #8be4b2 740px,
              #98FF98 860px,
              #98FF98 100%
            )`,
            color: '#0c1c13',
          }}
        >
          <div className="max-w-5xl mx-auto pt-24 pb-20 px-6 sm:px-10">
            
            {/* ============================================================ */}
            {/* HERO SECTION: MINIMAL, CLEAN, WITH MATCHING TEXT COLORS      */}
            {/* ============================================================ */}
            <div className="max-w-4xl mb-24">
              
              {/* Minimalist Pill Badge */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-black/10 border border-black/15 text-xs font-mono font-semibold tracking-wider uppercase text-[#0c1c13] mb-8">
                <span className="w-2 h-2 rounded-full bg-[#047857] animate-pulse" />
                <span>AI-Agent Incident Intelligence</span>
              </div>

              {/* Tagline: Matching Deep Colors Against Mint */}
              <h1 className="text-[40px] sm:text-[56px] md:text-[68px] lg:text-[76px] font-bold tracking-[-0.035em] leading-[1.04] text-[#0c1c13] mb-8">
                One mistake.<br />
                <span className="text-[#255239]">Many consequences.</span><br />
                <span className="text-[#047857]">One verified fix.</span>
              </h1>

              {/* Clear, Authoritative Product Statement */}
              <p className="text-[19px] sm:text-[22px] md:text-[24px] text-[#123623] leading-[1.38] font-light max-w-2xl mb-10">
                BIFURA is an AI-agent debugging and incident intelligence platform that helps developers understand why multi-step AI agents fail, identify the root cause, and verify a fix.
              </p>

              {/* Minimal Action CTAs */}
              <div className="flex flex-wrap items-center gap-4">
                <a
                  href={APP_CONFIG.appUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2.5 px-8 py-4 rounded-full bg-[#0c1c13] text-[#98FF98] text-[15px] font-semibold hover:bg-black transition-all shadow-xl shadow-black/15"
                >
                  <span className="w-2 h-2 rounded-full bg-[#047857] animate-pulse" />
                  <span>Launch Bifura Console</span>
                  <ArrowUpRight className="w-4 h-4 text-[#98FF98] transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                </a>

                <button
                  onClick={() => setActivePage('intelligence')}
                  className="px-7 py-4 rounded-full border border-black/25 text-[#0c1c13] text-[15px] font-medium hover:bg-black/5 transition-all"
                >
                  Explore Architecture
                </button>
              </div>
            </div>

            {/* ============================================================ */}
            {/* 3-PILLAR EDITORIAL ARCHITECTURE (CLEAN & NON-GENERIC)        */}
            {/* ============================================================ */}
            <div className="py-16 border-t border-black/15 grid grid-cols-1 md:grid-cols-3 gap-10">
              
              <div className="flex flex-col justify-between">
                <div>
                  <div className="text-[12px] font-mono font-bold uppercase tracking-wider text-[#047857] mb-3">
                    01 / Root-Cause Pinpointing
                  </div>
                  <h3 className="text-[22px] font-semibold text-[#0c1c13] mb-3 tracking-tight">
                    Earliest Point of Divergence
                  </h3>
                  <p className="text-[15px] text-[#1e442f] leading-relaxed">
                    Investigates counterfactual execution evidence backward to isolate the exact microsecond where execution separated from prompt intent — long before the fatal crash occurs downstream.
                  </p>
                </div>
              </div>

              <div className="flex flex-col justify-between">
                <div>
                  <div className="text-[12px] font-mono font-bold uppercase tracking-wider text-[#b45309] mb-3">
                    02 / Safety Guardrails
                  </div>
                  <h3 className="text-[22px] font-semibold text-[#0c1c13] mb-3 tracking-tight">
                    ALLOW · REVIEW · BLOCK
                  </h3>
                  <p className="text-[15px] text-[#1e442f] leading-relaxed">
                    Evaluates tool calls in real time to prevent destructive operations. Halts unauthorized API executions, schema mutations, and unvalidated payments before they hit the wire.
                  </p>
                </div>
              </div>

              <div className="flex flex-col justify-between">
                <div>
                  <div className="text-[12px] font-mono font-bold uppercase tracking-wider text-[#0e7490] mb-3">
                    03 / Verified Resolution
                  </div>
                  <h3 className="text-[22px] font-semibold text-[#0c1c13] mb-3 tracking-tight">
                    Deterministic CI/CD Replay
                  </h3>
                  <p className="text-[15px] text-[#1e442f] leading-relaxed">
                    Synthesizes targeted constraints and validates results against frozen incident fixtures in automated regression test suites with guaranteed zero regressions.
                  </p>
                </div>
              </div>

            </div>

            {/* ============================================================ */}
            {/* AUDITED RELIABILITY METRICS (FLOATING CLEANLY, NO HEAVY BOX)  */}
            {/* ============================================================ */}
            <div className="my-20 pt-16 border-t border-black/15">
              <div className="mb-12">
                <span className="text-[12px] font-mono font-bold uppercase tracking-wider text-[#047857] mb-2 block">
                  Audited Enterprise Reliability
                </span>
                <h2 className="text-[28px] sm:text-[36px] font-semibold text-[#0c1c13] tracking-tight">
                  Proven across 14,000,000 production traces.
                </h2>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
                <div>
                  <div className="text-[48px] sm:text-[56px] font-bold text-[#0c1c13] tracking-tight leading-none mb-2">
                    0
                  </div>
                  <div className="text-[14px] text-[#1e442f] font-medium">Undetected Regressions</div>
                </div>

                <div>
                  <div className="text-[48px] sm:text-[56px] font-bold text-[#0c1c13] tracking-tight leading-none mb-2">
                    89%
                  </div>
                  <div className="text-[14px] text-[#1e442f] font-medium">Faster Mean Time to Detect</div>
                </div>

                <div>
                  <div className="text-[48px] sm:text-[56px] font-bold text-[#0c1c13] tracking-tight leading-none mb-2">
                    100%
                  </div>
                  <div className="text-[14px] text-[#1e442f] font-medium">Dangerous Actions Blocked</div>
                </div>

                <div>
                  <div className="text-[48px] sm:text-[56px] font-bold text-[#047857] tracking-tight leading-none mb-2">
                    &lt; 14ms
                  </div>
                  <div className="text-[14px] text-[#1e442f] font-medium">Edge Telemetry Overhead</div>
                </div>
              </div>
            </div>

            {/* ============================================================ */}
            {/* MINIMAL CLOSING CTA                                          */}
            {/* ============================================================ */}
            <div className="py-20 text-center border-t border-black/15">
              <h2 className="text-[32px] sm:text-[44px] font-semibold text-[#0c1c13] tracking-tight mb-4">
                Move beyond detecting errors.
              </h2>
              <p className="text-[16px] sm:text-[18px] text-[#1e442f] max-w-xl mx-auto mb-8 font-light">
                Complete workflow from failure detection to root-cause analysis, impact visualization, and verified resolution.
              </p>
              <a
                href={APP_CONFIG.appUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-center gap-2.5 px-8 py-4 rounded-full bg-[#0c1c13] text-[#98FF98] text-[15px] font-semibold hover:bg-black transition-all shadow-xl shadow-black/15"
              >
                <span className="w-2 h-2 rounded-full bg-[#047857] animate-pulse" />
                <span>Open Live Console (localhost:8501)</span>
                <ArrowRight className="w-4 h-4 text-[#98FF98] transition-transform duration-200 group-hover:translate-x-1" />
              </a>
            </div>

          </div>
        </div>

      </BifuraPortal>

    </div>
  );
}