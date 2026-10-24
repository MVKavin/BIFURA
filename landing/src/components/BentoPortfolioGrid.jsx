import React, { useState } from 'react';
import { 
  GitCommit, 
  Share2, 
  ShieldCheck, 
  CheckCircle, 
  AlertOctagon, 
  Clock, 
  ArrowUpRight, 
  Network, 
  Database, 
  Layers, 
  Sliders, 
  TerminalSquare,
  Sparkles,
  Zap,
  Check
} from 'lucide-react';

export default function BentoPortfolioGrid({ t, onOpenDemoModal }) {
  const [safetyFilter, setSafetyFilter] = useState('ALL');
  const [activeTabDAG, setActiveTabDAG] = useState('all');

  return (
    <section id="capabilities" className="py-24 md:py-32 bg-[#FFFFFF] text-[#111827] relative overflow-hidden bg-grid-light border-b border-[#E5E7EB]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header with French Corporate Authority */}
        <div className="max-w-3xl mb-16 md:mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FF3E24]/10 border border-[#FF3E24]/20 text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-4">
            <span>{t.bento.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-[#111827] leading-[1.1]">
            {t.bento.title}
          </h2>
          <p className="mt-5 text-lg sm:text-xl text-[#4B5563] leading-relaxed">
            {t.bento.subtitle}
          </p>
        </div>

        {/* 4-Card Bento Portfolio Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
          
          {/* Card 1: Root-Cause Pinpointing (Span 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#FF3E24]/40 p-8 flex flex-col justify-between transition-all duration-500 ease-out hover:scale-[1.01] hover:shadow-xl group">
            <div>
              <div className="flex items-center justify-between mb-6">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E5E7EB] text-xs font-mono font-bold text-[#111827] shadow-sm">
                  {t.bento.card1.tag}
                </span>
                <span className="text-xs font-mono text-[#6B7280] flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-[#FF3E24]" />
                  Microsecond Resolution
                </span>
              </div>

              <h3 className="font-display font-bold text-2xl sm:text-3xl text-[#111827] mb-3 group-hover:text-[#FF3E24] transition-colors">
                {t.bento.card1.title}
              </h3>
              <p className="text-[#4B5563] text-base leading-relaxed mb-8">
                {t.bento.card1.desc}
              </p>
            </div>

            {/* Visual 16:9 Timeline Trace Mockup */}
            <div className="rounded-2xl bg-[#0B0C10] p-5 border border-[#262833] text-white font-mono shadow-inner">
              <div className="flex items-center justify-between text-xs text-gray-400 pb-3 border-b border-[#262833] mb-4">
                <span>EXECUTION TIMELINE vs EXPECTED SPEC</span>
                <span className="text-[#FF3E24] font-bold">DELTA PINPOINTED AT T+480ms</span>
              </div>

              {/* Trajectory comparison visualization */}
              <div className="space-y-3 text-xs">
                {/* Expected Track */}
                <div className="flex items-center gap-3">
                  <span className="w-20 text-emerald-400 font-bold">ATTENDU :</span>
                  <div className="flex-1 flex items-center gap-1">
                    <span className="px-2 py-1 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800">Prompt</span>
                    <span className="text-gray-600">→</span>
                    <span className="px-2 py-1 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800">Scan</span>
                    <span className="text-gray-600">→</span>
                    <span className="px-2 py-1 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800 font-semibold">Dry-Run Target</span>
                    <span className="text-gray-600">→</span>
                    <span className="px-2 py-1 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800">Safe Drop</span>
                  </div>
                </div>

                {/* Actual Track */}
                <div className="flex items-center gap-3">
                  <span className="w-20 text-[#FF8573] font-bold">RÉEL :</span>
                  <div className="flex-1 flex items-center gap-1">
                    <span className="px-2 py-1 rounded bg-[#171922] text-gray-300">Prompt</span>
                    <span className="text-gray-600">→</span>
                    <span className="px-2 py-1 rounded bg-[#171922] text-gray-300">Scan</span>
                    <span className="text-gray-600">→</span>
                    {/* The Divergence Point */}
                    <span className="relative px-2.5 py-1 rounded bg-[#FF3E24] text-white font-extrabold shadow-lg shadow-[#FF3E24]/30 animate-pulse">
                      DIVERGENCE #3
                      <span className="absolute -top-2.5 -right-2 px-1.5 py-0.2 rounded-full bg-white text-[#FF3E24] text-[9px] font-black">
                        ROOT
                      </span>
                    </span>
                    <span className="text-red-500">→</span>
                    <span className="px-2 py-1 rounded bg-red-950/70 text-red-400 border border-red-800/60 line-through">
                      CRASH #8
                    </span>
                  </div>
                </div>
              </div>

              {/* Stat footer */}
              <div className="mt-4 pt-3 border-t border-[#262833] flex items-center justify-between text-xs">
                <span className="text-gray-400">Earliest point vs Crash site:</span>
                <span className="text-emerald-400 font-semibold">Économie de 5 étapes d'investigation</span>
              </div>
            </div>

            {/* Bottom Key Metric */}
            <div className="mt-6 flex items-baseline gap-3 pt-4 border-t border-[#E5E7EB]">
              <span className="font-display font-black text-4xl text-[#FF3E24]">
                {t.bento.card1.statVal}
              </span>
              <div>
                <span className="text-sm font-bold text-[#111827] block">{t.bento.card1.stat}</span>
                <span className="text-xs text-[#6B7280]">{t.bento.card1.statSub}</span>
              </div>
            </div>
          </div>

          {/* Card 2: Impact Visualization / Blast Radius DAG (Span 5) */}
          <div className="md:col-span-5 rounded-3xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#FF3E24]/40 p-8 flex flex-col justify-between transition-all duration-500 ease-out hover:scale-[1.01] hover:shadow-xl group">
            <div>
              <div className="flex items-center justify-between mb-6">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E5E7EB] text-xs font-mono font-bold text-[#111827] shadow-sm">
                  {t.bento.card2.tag}
                </span>
                <span className="text-xs font-mono text-[#1D4ED8] font-bold">
                  Directed Acyclic Graph
                </span>
              </div>

              <h3 className="font-display font-bold text-2xl sm:text-3xl text-[#111827] mb-3 group-hover:text-[#FF3E24] transition-colors">
                {t.bento.card2.title}
              </h3>
              <p className="text-[#4B5563] text-base leading-relaxed mb-6">
                {t.bento.card2.desc}
              </p>
            </div>

            {/* Interactive DAG Ripple Simulation */}
            <div className="rounded-2xl bg-[#0B0C10] p-5 border border-[#262833] text-white font-mono shadow-inner">
              <div className="text-xs text-gray-400 mb-3 flex items-center justify-between">
                <span>RIPPLE EFFECT (BLAST RADIUS)</span>
                <span className="text-emerald-400 font-bold">CONTAINED</span>
              </div>

              {/* Node Graph Mockup */}
              <div className="space-y-2 text-xs">
                <div className="flex items-center justify-between p-2 rounded-lg bg-[#171922] border border-red-500/30">
                  <div className="flex items-center gap-2">
                    <Database className="w-4 h-4 text-red-400" />
                    <span>PostgreSQL (core_ledger)</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-[10px] font-bold">PROTECTED</span>
                </div>

                <div className="flex items-center justify-between p-2 rounded-lg bg-[#171922] border border-[#262833]">
                  <div className="flex items-center gap-2">
                    <Network className="w-4 h-4 text-amber-400" />
                    <span>Stripe Settlement API</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 text-[10px] font-bold">UNMUTATED</span>
                </div>

                <div className="flex items-center justify-between p-2 rounded-lg bg-[#171922] border border-[#262833]">
                  <div className="flex items-center gap-2">
                    <Share2 className="w-4 h-4 text-blue-400" />
                    <span>Slack Webhook Broadcast</span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 text-[10px] font-bold">CANCELLED</span>
                </div>
              </div>
            </div>

            {/* Bottom Key Metric */}
            <div className="mt-6 flex items-baseline gap-3 pt-4 border-t border-[#E5E7EB]">
              <span className="font-display font-black text-4xl text-[#FF3E24]">
                {t.bento.card2.statVal}
              </span>
              <div>
                <span className="text-sm font-bold text-[#111827] block">{t.bento.card2.stat}</span>
                <span className="text-xs text-[#6B7280]">{t.bento.card2.statSub}</span>
              </div>
            </div>
          </div>

          {/* Card 3: Safety Enforcement Triad (Span 5) */}
          <div id="safety" className="md:col-span-5 rounded-3xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#FF3E24]/40 p-8 flex flex-col justify-between transition-all duration-500 ease-out hover:scale-[1.01] hover:shadow-xl group">
            <div>
              <div className="flex items-center justify-between mb-6">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E5E7EB] text-xs font-mono font-bold text-[#111827] shadow-sm">
                  {t.bento.card3.tag}
                </span>
                <span className="text-xs font-mono text-emerald-600 font-bold">
                  Zero False-Negatives
                </span>
              </div>

              <h3 className="font-display font-bold text-2xl sm:text-3xl text-[#111827] mb-3 group-hover:text-[#FF3E24] transition-colors">
                {t.bento.card3.title}
              </h3>
              <p className="text-[#4B5563] text-base leading-relaxed mb-6">
                {t.bento.card3.desc}
              </p>
            </div>

            {/* Interactive Safety Triad Badge Selector */}
            <div className="rounded-2xl bg-[#0B0C10] p-5 border border-[#262833] text-white font-mono shadow-inner">
              <div className="text-xs text-gray-400 mb-3 flex items-center justify-between">
                <span>TRI-STATE GATEKEEPER</span>
                <span className="text-cyan-400 text-[11px]">&lt; 14ms Latency</span>
              </div>

              <div className="grid grid-cols-3 gap-2 text-center text-xs">
                <button
                  type="button"
                  onClick={() => setSafetyFilter('ALLOW')}
                  className={`p-2.5 rounded-xl border transition-all ${
                    safetyFilter === 'ALLOW' || safetyFilter === 'ALL'
                      ? 'bg-emerald-500/20 border-emerald-500/60 text-emerald-300 font-bold'
                      : 'bg-[#171922] border-[#262833] text-gray-400'
                  }`}
                >
                  <div className="text-sm font-extrabold text-emerald-400">ALLOW</div>
                  <div className="text-[10px] text-gray-300 font-normal">Lectures & scans</div>
                </button>

                <button
                  type="button"
                  onClick={() => setSafetyFilter('REVIEW')}
                  className={`p-2.5 rounded-xl border transition-all ${
                    safetyFilter === 'REVIEW' || safetyFilter === 'ALL'
                      ? 'bg-amber-500/20 border-amber-500/60 text-amber-300 font-bold'
                      : 'bg-[#171922] border-[#262833] text-gray-400'
                  }`}
                >
                  <div className="text-sm font-extrabold text-amber-400">REVIEW</div>
                  <div className="text-[10px] text-gray-300 font-normal">Validation humaine</div>
                </button>

                <button
                  type="button"
                  onClick={() => setSafetyFilter('BLOCK')}
                  className={`p-2.5 rounded-xl border transition-all ${
                    safetyFilter === 'BLOCK' || safetyFilter === 'ALL'
                      ? 'bg-red-500/20 border-red-500/60 text-red-300 font-bold'
                      : 'bg-[#171922] border-[#262833] text-gray-400'
                  }`}
                >
                  <div className="text-sm font-extrabold text-red-400">BLOCK</div>
                  <div className="text-[10px] text-gray-300 font-normal">Action destructrice</div>
                </button>
              </div>

              <div className="mt-3 text-[11px] text-gray-400 text-center bg-[#171922] py-1.5 rounded-lg border border-[#262833]">
                Interception avant appel réseau : <strong>0 risque pour la prod</strong>
              </div>
            </div>

            {/* Bottom Key Metric */}
            <div className="mt-6 flex items-baseline gap-3 pt-4 border-t border-[#E5E7EB]">
              <span className="font-display font-black text-4xl text-[#FF3E24]">
                {t.bento.card3.statVal}
              </span>
              <div>
                <span className="text-sm font-bold text-[#111827] block">{t.bento.card3.stat}</span>
                <span className="text-xs text-[#6B7280]">{t.bento.card3.statSub}</span>
              </div>
            </div>
          </div>

          {/* Card 4: Verified Replay & Auto-Fix Synthesis (Span 7) */}
          <div className="md:col-span-7 rounded-3xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#FF3E24]/40 p-8 flex flex-col justify-between transition-all duration-500 ease-out hover:scale-[1.01] hover:shadow-xl group">
            <div>
              <div className="flex items-center justify-between mb-6">
                <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E5E7EB] text-xs font-mono font-bold text-[#111827] shadow-sm">
                  {t.bento.card4.tag}
                </span>
                <span className="text-xs font-mono text-emerald-600 font-bold flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                  CI/CD Ready
                </span>
              </div>

              <h3 className="font-display font-bold text-2xl sm:text-3xl text-[#111827] mb-3 group-hover:text-[#FF3E24] transition-colors">
                {t.bento.card4.title}
              </h3>
              <p className="text-[#4B5563] text-base leading-relaxed mb-6">
                {t.bento.card4.desc}
              </p>
            </div>

            {/* Code Diff Preview */}
            <div className="rounded-2xl bg-[#0B0C10] p-5 border border-[#262833] text-white font-mono shadow-inner text-xs">
              <div className="flex items-center justify-between pb-3 border-b border-[#262833] text-gray-400 mb-3">
                <span>SYNTHESIZED PROMPT & SCHEMA FIX</span>
                <span className="text-emerald-400">24/24 REPLAY TESTS GREEN</span>
              </div>

              <div className="space-y-2 bg-[#111216] p-3 rounded-xl border border-[#262833] overflow-x-auto">
                <div className="text-gray-500">// Bifura Auto-Constraint Injection:</div>
                <div className="text-emerald-400 font-semibold">
                  + STRICT_CONSTRAINT: environment.match('staging')
                </div>
                <div className="text-emerald-400 font-semibold">
                  + SCHEMA_VALIDATOR: PydanticModel.require_signed_token()
                </div>
                <div className="text-gray-400 pt-1">
                  Deterministic Replay Hash: <span className="text-white">sha256:4a88f7b...</span>
                </div>
              </div>
            </div>

            {/* Bottom Key Metric */}
            <div className="mt-6 flex items-baseline gap-3 pt-4 border-t border-[#E5E7EB]">
              <span className="font-display font-black text-4xl text-[#FF3E24]">
                {t.bento.card4.statVal}
              </span>
              <div>
                <span className="text-sm font-bold text-[#111827] block">{t.bento.card4.stat}</span>
                <span className="text-xs text-[#6B7280]">{t.bento.card4.statSub}</span>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
