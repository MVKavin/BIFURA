import React from 'react';
import { MotionSlideEntry, MotionStaggerContainer, MotionStaggerItem } from '../components/MotionScrollReveal';
import { CheckCircle2, RefreshCw, Terminal, ArrowRight, ShieldCheck, FileCheck } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function ReplayPage({ setActivePage, onOpenDemo }) {
  return (
    <div className="bg-[#061811] text-white select-none font-sans">
      
      {/* Tile 1: Hero Presentation */}
      <section className="bg-[#061811] py-16 sm:py-24 px-4 sm:px-8 text-center border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionStaggerContainer staggerDelay={0.08}>
            <MotionStaggerItem>
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-3 block">
                Automated Patch Verification
              </span>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <h1 className="text-[36px] sm:text-[48px] md:text-[56px] font-semibold tracking-[-0.035em] leading-[1.1] text-white mb-4">
                Deterministic replay.
              </h1>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <p className="text-[17px] sm:text-[20px] text-[#9bb0a5] font-light leading-relaxed max-w-2xl mx-auto mb-8">
                Move beyond simply detecting errors. Close the loop with targeted patch synthesis and automated replay tests that guarantee zero regressions.
              </p>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <div className="flex flex-wrap items-center justify-center gap-3.5 mb-14">
                <a
                  href={APP_CONFIG.appUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#154633] border border-emerald-400/30 text-white text-[15px] font-semibold hover:bg-[#1c5a42] transition-all shadow-lg shadow-emerald-950/40"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Launch Replay Environment</span>
                  <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
                </a>
                <button
                  onClick={() => setActivePage('buy')}
                  className="px-6 py-3 rounded-full bg-[#0a2318] border border-emerald-900/50 text-[#c2d7cd] text-[15px] font-normal hover:bg-[#0f2e20] hover:text-white transition-all"
                >
                  View Integration Specs
                </button>
              </div>
            </MotionStaggerItem>
          </MotionStaggerContainer>

          {/* Replay Code Fixture Mockup Resting on Canvas */}
          <MotionSlideEntry delay={0.15}>
            <div className="relative mx-auto max-w-3xl w-full text-left">
              <div className="rounded-2xl border border-emerald-800/30 bg-[#092218] shadow-2xl overflow-hidden">
                <div className="flex items-center justify-between px-6 py-3.5 bg-[#061811] border-b border-emerald-900/40">
                  <div className="flex items-center gap-2 text-[12px] font-mono text-[#9bb0a5]">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400/60" />
                    <span>BIFURA DETERMINISTIC REPLAY HARNESS // FIXTURE #BF-8942</span>
                  </div>
                  <span className="text-[12px] font-mono text-emerald-400 font-bold">
                    24/24 REPLAY TESTS GREEN
                  </span>
                </div>

                <div className="p-6 font-mono text-[13px] leading-relaxed text-[#c2d7cd] bg-[#092218] space-y-3">
                  <div className="text-[#889990]">// 1. Synthesizing surgical prompt constraint:</div>
                  <div className="p-3.5 rounded-xl bg-[#061811] text-emerald-300 border border-emerald-500/30">
                    + STRICT_CONSTRAINT: environment.match('staging')
                    <br />
                    + SCHEMA_VALIDATOR: PydanticModel.require_signed_token()
                  </div>

                  <div className="text-[#889990] pt-2">// 2. Deterministic execution against frozen incident snapshot:</div>
                  <div className="p-3.5 rounded-xl bg-[#061811] text-[#9bb0a5] border border-emerald-900/40">
                    ✓ replay_incident_8942_step3.json ............. <span className="text-emerald-400">PASSED</span> (410ms)
                    <br />
                    ✓ regression_test_multi_shard.py .............. <span className="text-emerald-400">PASSED</span> (380ms)
                    <br />
                    ✓ zero_data_loss_verification ................. <span className="text-emerald-400">PASSED</span> (90ms)
                  </div>

                  <div className="pt-2 text-[12px] text-[#889990] flex items-center justify-between">
                    <span>Cryptographic patch hash: sha256:0x89fcb...</span>
                    <span className="text-emerald-400 font-semibold">Certified Non-Regression</span>
                  </div>
                </div>
              </div>
            </div>
          </MotionSlideEntry>

        </div>
      </section>


      {/* Tile 2: Synthetic Fixtures & Mocks */}
      <section className="bg-[#092218] py-16 sm:py-24 px-4 sm:px-8 border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionSlideEntry>
            <div className="text-center max-w-2xl mx-auto mb-14">
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
                Test Harness Architecture
              </span>
              <h2 className="text-[30px] sm:text-[40px] font-semibold tracking-tight text-white mb-3">
                Replay reality without mutating live systems.
              </h2>
              <p className="text-[15px] text-[#9bb0a5] leading-relaxed">
                How do you test an agent fix without re-calling live payment accounts or re-querying production databases? BIFURA freezes model and network fixtures for 100% deterministic local replay.
              </p>
            </div>
          </MotionSlideEntry>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <MotionSlideEntry delay={0.05}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 h-full flex flex-col justify-between">
                <div>
                  <div className="text-[17px] font-semibold text-white mb-2">Frozen Fixtures</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Captures exact input tokens, tool outputs, and timestamped network packets so replay tests run identically every single time.
                  </p>
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.15}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 h-full flex flex-col justify-between">
                <div>
                  <div className="text-[17px] font-semibold text-white mb-2">Targeted Patches</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Generates minimal, surgical changes to prompts or Pydantic schemas without broad hallucination side effects on unrelated tasks.
                  </p>
                </div>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.25}>
              <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 h-full flex flex-col justify-between">
                <div>
                  <div className="text-[17px] font-semibold text-white mb-2">CI/CD Gatekeeper</div>
                  <p className="text-[14px] text-[#9bb0a5] leading-relaxed">
                    Integrates directly into GitHub Actions, GitLab, and Argo workflows to block untested agent code from shipping to staging.
                  </p>
                </div>
              </div>
            </MotionSlideEntry>

          </div>

        </div>
      </section>

    </div>
  );
}