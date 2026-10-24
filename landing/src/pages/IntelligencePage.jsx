import React from 'react';
import { CausalTimelineRender, BlastRadiusTopologicalRender } from '../components/ProductRenders';
import { MotionSlideEntry, MotionStaggerContainer, MotionStaggerItem } from '../components/MotionScrollReveal';
import { ArrowRight, ChevronRight, ShieldCheck, Database, Network, Clock, GitCommit } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function IntelligencePage({ setActivePage, onOpenDemo }) {
  return (
    <div className="bg-[#061811] text-white select-none font-sans">
      
      {/* Tile 1: Hero Deep Dive */}
      <section className="bg-[#061811] py-16 sm:py-24 px-4 sm:px-8 text-center border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionStaggerContainer staggerDelay={0.08}>
            <MotionStaggerItem>
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-3 block">
                Incident Intelligence Platform
              </span>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <h1 className="text-[36px] sm:text-[48px] md:text-[56px] font-semibold tracking-[-0.035em] leading-[1.1] text-white mb-4">
                The anatomy of an agent failure.
              </h1>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <p className="text-[17px] sm:text-[20px] text-[#9bb0a5] font-light leading-relaxed max-w-2xl mx-auto mb-8">
                Most LLM monitoring tools log the crash. BIFURA isolates the subtle intent drift that caused it three steps prior.
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
                  <span>Launch Investigation Console</span>
                  <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
                </a>
                <button
                  onClick={() => setActivePage('safety')}
                  className="px-6 py-3 rounded-full bg-[#0a2318] border border-emerald-900/50 text-[#c2d7cd] text-[15px] font-normal hover:bg-[#0f2e20] hover:text-white transition-all"
                >
                  Explore Safety Engine
                </button>
              </div>
            </MotionStaggerItem>
          </MotionStaggerContainer>

          <MotionSlideEntry delay={0.15}>
            <CausalTimelineRender isDark={true} />
          </MotionSlideEntry>

        </div>
      </section>


      {/* Tile 2: Counterfactual Causal Graph */}
      <section className="bg-[#092218] py-16 sm:py-24 px-4 sm:px-8 border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionSlideEntry>
            <div className="text-center max-w-2xl mx-auto mb-14">
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
                Algorithmic Investigation
              </span>
              <h2 className="text-[30px] sm:text-[40px] font-semibold tracking-tight leading-tight text-white mb-3">
                Causal Backtracking vs. Naive Error Trapping.
              </h2>
              <p className="text-[15px] text-[#9bb0a5] leading-relaxed">
                When an agent executes an invalid query at Step 7, conventional debuggers inspect Step 7. BIFURA traverses the state transitions backward, identifying that an ambiguous parameter at Step 2 corrupted the agent's internal memory tree.
              </p>
            </div>
          </MotionSlideEntry>

          {/* 3 Architecture Pillars */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <MotionSlideEntry delay={0.05}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 flex flex-col justify-between h-full">
                <div>
                  <div className="text-[22px] font-semibold text-emerald-400 mb-1">01</div>
                  <div className="text-[17px] font-semibold text-white mb-2">Trace Capture</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Zero-latency OpenTelemetry instrumentation capturing prompt tokens, completions, JSON schema validations, and memory state diffs.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-emerald-900/40 text-[12px] font-mono text-emerald-400">
                  Overhead: &lt; 1.1ms
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.15}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 flex flex-col justify-between h-full">
                <div>
                  <div className="text-[22px] font-semibold text-amber-400 mb-1">02</div>
                  <div className="text-[17px] font-semibold text-white mb-2">Earliest Delta</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Cross-references observed execution steps against past incident catalogs and counterfactual specifications to isolate the exact point of divergence.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-emerald-900/40 text-[12px] font-mono text-amber-300">
                  99.82% Confidence
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.25}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 flex flex-col justify-between h-full">
                <div>
                  <div className="text-[22px] font-semibold text-teal-300 mb-1">03</div>
                  <div className="text-[17px] font-semibold text-white mb-2">Blast Containment</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Maps all downstream databases, payment APIs, and messaging hooks exposed to the flawed inference before state commits occur.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-emerald-900/40 text-[12px] font-mono text-teal-300">
                  DAG Topology
                </div>
              </div>
            </MotionSlideEntry>

          </div>

        </div>
      </section>


      {/* Tile 3: Topological Blast Radius */}
      <section className="bg-[#061811] py-16 sm:py-24 px-4 sm:px-8 border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto text-center">
          
          <MotionSlideEntry>
            <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
              Impact Mapping
            </span>

            <h2 className="text-[30px] sm:text-[40px] font-semibold tracking-tight text-white mb-3">
              Containing the domino effect.
            </h2>

            <p className="text-[15px] text-[#9bb0a5] leading-relaxed max-w-xl mx-auto mb-10">
              In multi-step systems, an early hallucination rarely remains isolated. BIFURA's blast radius engine models the ripple effect across your service mesh.
            </p>
          </MotionSlideEntry>

          <MotionSlideEntry delay={0.15}>
            <BlastRadiusTopologicalRender isDark={true} />
          </MotionSlideEntry>

          <MotionSlideEntry delay={0.2}>
            <div className="mt-10 flex justify-center">
              <button
                onClick={() => setActivePage('safety')}
                className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#154633] border border-emerald-400/30 text-white text-[15px] font-semibold hover:bg-[#1c5a42] transition-all shadow-lg shadow-emerald-950/40"
              >
                <span>Continue to Safety Engine</span>
                <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
              </button>
            </div>
          </MotionSlideEntry>

        </div>
      </section>

    </div>
  );
}