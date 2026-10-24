import React from 'react';
import { SafetyMatrixRender } from '../components/ProductRenders';
import { MotionSlideEntry, MotionStaggerContainer, MotionStaggerItem } from '../components/MotionScrollReveal';
import { ShieldCheck, Check, Lock, ChevronRight, AlertOctagon, ArrowRight } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function SafetyPage({ setActivePage, onOpenDemo }) {
  return (
    <div className="bg-[#061811] text-white select-none font-sans">
      
      {/* Tile 1: Hero Presentation */}
      <section className="bg-[#061811] py-16 sm:py-24 px-4 sm:px-8 text-center border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionStaggerContainer staggerDelay={0.08}>
            <MotionStaggerItem>
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-3 block">
                Real-Time Safety Enforcement
              </span>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <h1 className="text-[36px] sm:text-[48px] md:text-[56px] font-semibold tracking-[-0.035em] leading-[1.1] text-white mb-4">
                Active enforcement. Not passive logging.
              </h1>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <p className="text-[17px] sm:text-[20px] text-[#9bb0a5] font-light leading-relaxed max-w-2xl mx-auto mb-8">
                An alert sent after a database is dropped is useless. BIFURA classifies tool calls in-flight and halts destructive operations before they hit the wire.
              </p>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <div className="flex flex-wrap items-center justify-center gap-3.5 mb-12">
                <a
                  href={APP_CONFIG.appUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#154633] border border-emerald-400/30 text-white text-[15px] font-semibold hover:bg-[#1c5a42] transition-all shadow-lg shadow-emerald-950/40"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Launch Safety Dashboard</span>
                  <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
                </a>
                <button
                  onClick={() => setActivePage('replay')}
                  className="px-6 py-3 rounded-full bg-[#0a2318] border border-emerald-900/50 text-[#c2d7cd] text-[15px] font-normal hover:bg-[#0f2e20] hover:text-white transition-all"
                >
                  Explore Replay CI/CD
                </button>
              </div>
            </MotionStaggerItem>
          </MotionStaggerContainer>

          <MotionSlideEntry delay={0.15}>
            <SafetyMatrixRender isDark={true} />
          </MotionSlideEntry>

        </div>
      </section>


      {/* Tile 2: Tri-State Policy Deep Dive */}
      <section className="bg-[#092218] py-16 sm:py-24 px-4 sm:px-8 border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionSlideEntry>
            <div className="text-center max-w-2xl mx-auto mb-14">
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
                Tri-State Architecture
              </span>
              <h2 className="text-[30px] sm:text-[40px] font-semibold tracking-tight text-white mb-3">
                Three verdicts. Zero ambiguity.
              </h2>
              <p className="text-[15px] text-[#9bb0a5] leading-relaxed">
                Rather than binary blocklists that break developer workflows, BIFURA implements a nuanced tri-state policy engine tailored for autonomous multi-step reasoning.
              </p>
            </div>
          </MotionSlideEntry>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <MotionSlideEntry delay={0.05}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-500/25 flex flex-col justify-between h-full">
                <div>
                  <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-mono font-bold uppercase">
                    Verdict 01
                  </span>
                  <h3 className="text-[22px] font-semibold text-white mt-4 mb-2">ALLOW</h3>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Harmless read-only operations, metadata scans, idempotent schema queries, and authorized data transformations pass immediately with &lt; 1.2ms latency.
                  </p>
                </div>
                <div className="mt-8 pt-4 border-t border-emerald-900/40 text-[12px] font-mono text-emerald-400">
                  Zero Developer Friction
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.15}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-amber-500/25 flex flex-col justify-between h-full">
                <div>
                  <span className="px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-300 text-[11px] font-mono font-bold uppercase">
                    Verdict 02
                  </span>
                  <h3 className="text-[22px] font-semibold text-white mt-4 mb-2">REVIEW</h3>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    High-value transactions, cross-border settlements, customer refund anomalies, or ambiguous prompts pause execution and trigger Slack/Webhook human verification.
                  </p>
                </div>
                <div className="mt-8 pt-4 border-t border-emerald-900/40 text-[12px] font-mono text-amber-300">
                  Human-in-the-Loop (Art. 14)
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.25}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-rose-500/25 flex flex-col justify-between h-full">
                <div>
                  <span className="px-2.5 py-1 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-[11px] font-mono font-bold uppercase">
                    Verdict 03
                  </span>
                  <h3 className="text-[22px] font-semibold text-white mt-4 mb-2">BLOCK</h3>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Arbitrary code execution, DROP TABLE statements, unauthorized credential dumping, and untrusted network egress are immediately severed in-memory.
                  </p>
                </div>
                <div className="mt-8 pt-4 border-t border-emerald-900/40 text-[12px] font-mono text-rose-400">
                  Zero-Tolerance Containment
                </div>
              </div>
            </MotionSlideEntry>

          </div>

        </div>
      </section>

    </div>
  );
}