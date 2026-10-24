import React, { useState } from 'react';
import { 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  Play, 
  ArrowRight, 
  Code2, 
  Sparkles, 
  Activity, 
  CornerDownRight, 
  Lock,
  GitBranch,
  RefreshCw,
  Terminal,
  Zap
} from 'lucide-react';

export default function HeroSection({ t, lang, onOpenDemoModal, onScrollToSection }) {
  const [activeStep, setActiveStep] = useState(3); // Default to Root Cause divergence step
  const [isReplaying, setIsReplaying] = useState(false);

  const heroSteps = [
    {
      id: 1,
      title: "1. Intent Parsing",
      tool: "intent_router",
      status: "PASS",
      statusColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
      time: "+0.00ms",
      details: "Intent: 'Reclaim unused storage on non-production clusters'",
      delta: "Aligned with user instruction (Drift: 0.0%)",
    },
    {
      id: 2,
      title: "2. Schema Query",
      tool: "pg_catalog_scan",
      status: "PASS",
      statusColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
      time: "+210ms",
      details: "Scan returned 18 schemas. Output includes 'core_ledger_v2'",
      delta: "Expected staging filtering, received unfiltered cluster scope",
    },
    {
      id: 3,
      title: "3. Plan Generation",
      tool: "query_planner_llm",
      status: "ROOT CAUSE",
      statusColor: "text-[#FF3E24] bg-[#FF3E24]/10 border-[#FF3E24]/40 font-bold",
      time: "+480ms",
      details: "Agent synthesized: DROP TABLE core_ledger_v2 CASCADE;",
      delta: "DIVERGENCE FOUND: Earliest point of failure. Failed to bind environment parameter.",
      highlight: true,
    },
    {
      id: 4,
      title: "4. Tool Invocation",
      tool: "pg_execute_destructive",
      status: "BLOCKED",
      statusColor: "text-red-400 bg-red-500/15 border-red-500/30 font-bold",
      time: "+512ms",
      details: "BIFURA Safety Policy #SEC-801: Non-staging DDL dropped.",
      delta: "Zero bytes written. Production database preserved.",
    },
    {
      id: 5,
      title: "5. Verified Fix",
      tool: "bifura_replay_test",
      status: "CERTIFIED",
      statusColor: "text-cyan-400 bg-cyan-500/10 border-cyan-500/30",
      time: "+890ms",
      details: "Synthetic prompt patch applied. 24 regression tests passed.",
      delta: "Deterministic replay harness sealed with SHA-256 fixture.",
    },
  ];

  const handleSimulateReplay = () => {
    setIsReplaying(true);
    let step = 1;
    const interval = setInterval(() => {
      setActiveStep(step);
      step++;
      if (step > 5) {
        clearInterval(interval);
        setIsReplaying(false);
      }
    }, 700);
  };

  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden bg-[#0B0C10] bg-grid-pattern">
      {/* Editorial Ambient Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[450px] bg-gradient-to-tr from-[#FF3E24]/10 via-[#1D4ED8]/10 to-transparent blur-[140px] pointer-events-none rounded-full" />
      <div className="absolute top-20 right-10 w-72 h-72 bg-[#FF3E24]/5 blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Header Tag / Pill */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#171922] border border-[#262833] text-xs font-mono tracking-wider uppercase text-gray-300 shadow-inner">
            <span className="w-2 h-2 rounded-full bg-[#FF3E24] animate-ping" />
            <span className="font-semibold text-white tracking-widest">{t.hero.badge}</span>
          </div>
          <div className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-900/20 border border-blue-500/30 text-[11px] font-mono text-cyan-400">
            <Lock className="w-3 h-3 text-cyan-400" />
            <span>ISO 27001 & SOC 2 COMPLIANT</span>
          </div>
        </div>

        {/* Massive Editorial Tagline */}
        <div className="text-center max-w-5xl mx-auto mb-8">
          <h1 className="font-display font-extrabold text-4xl sm:text-6xl md:text-7xl lg:text-8xl tracking-tight leading-[1.05] text-white">
            <span className="block text-white">{t.hero.titleLine1}</span>
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-gray-200 via-gray-400 to-gray-500">
              {t.hero.titleLine2}
            </span>
            <span className="block text-[#FF3E24] drop-shadow-[0_0_35px_rgba(255,62,36,0.25)]">
              {t.hero.titleLine3}
            </span>
          </h1>

          <p className="mt-8 text-lg sm:text-xl md:text-2xl text-gray-400 font-normal leading-relaxed max-w-3xl mx-auto">
            {t.hero.desc}
          </p>
        </div>

        {/* Primary Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <button
            onClick={onOpenDemoModal}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-4 rounded-full bg-[#FF3E24] text-white font-bold text-base hover:bg-[#E0341B] transition-all duration-200 shadow-xl shadow-[#FF3E24]/25 hover:shadow-[#FF3E24]/40 hover:-translate-y-0.5"
          >
            <Activity className="w-5 h-5" />
            <span>{t.hero.primaryCta}</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onScrollToSection('sandbox')}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-4 rounded-full bg-[#111216] border border-[#262833] text-white font-semibold text-base hover:bg-[#171922] hover:border-gray-600 transition-all duration-200 shadow-sm"
          >
            <Terminal className="w-4 h-4 text-[#00D2FF]" />
            <span>{t.hero.secondaryCta}</span>
          </button>
        </div>

        {/* Interactive Hero Debugger Showcase */}
        <div className="relative max-w-5xl mx-auto rounded-2xl bg-gradient-to-b from-[#171922] to-[#0E0F14] border border-[#262833] p-1 shadow-2xl overflow-hidden group">
          {/* Top Window Bar */}
          <div className="flex flex-wrap items-center justify-between px-5 py-3.5 bg-[#111216]/95 border-b border-[#262833] rounded-t-xl gap-3">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/80 border border-red-600/40" />
                <div className="w-3 h-3 rounded-full bg-amber-500/80 border border-amber-600/40" />
                <div className="w-3 h-3 rounded-full bg-emerald-500/80 border border-emerald-600/40" />
              </div>
              <div className="h-4 w-px bg-[#262833] mx-1" />
              <div className="flex items-center gap-2 font-mono text-xs text-gray-300">
                <span className="font-semibold text-white">{t.hero.demoTitle}</span>
                <span className="text-gray-500 hidden md:inline">• {t.hero.demoSubtitle}</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded text-[11px] font-mono bg-red-500/10 text-red-400 border border-red-500/30">
                <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
                ROOT CAUSE PINPOINTED
              </span>
              <button
                onClick={handleSimulateReplay}
                disabled={isReplaying}
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#FF3E24]/20 border border-[#FF3E24]/50 text-xs font-mono text-white hover:bg-[#FF3E24] transition-all disabled:opacity-50"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isReplaying ? 'animate-spin' : ''}`} />
                <span>{isReplaying ? 'Rejouer...' : 'Rejouer la trace'}</span>
              </button>
            </div>
          </div>

          {/* Stepper Timeline Navigation */}
          <div className="grid grid-cols-2 sm:grid-cols-5 bg-[#0D0E12] border-b border-[#262833] divide-y sm:divide-y-0 sm:divide-x divide-[#262833]">
            {heroSteps.map((s) => (
              <button
                key={s.id}
                onClick={() => setActiveStep(s.id)}
                className={`p-3.5 text-left transition-all ${
                  activeStep === s.id
                    ? 'bg-[#171922] border-b-2 border-b-[#FF3E24]'
                    : 'hover:bg-[#14151B] opacity-75 hover:opacity-100'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono text-[11px] text-gray-400">{s.time}</span>
                  <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${s.statusColor}`}>
                    {s.status}
                  </span>
                </div>
                <div className="text-xs font-semibold text-white truncate">{s.title}</div>
                <div className="text-[10px] font-mono text-gray-500 truncate">{s.tool}</div>
              </button>
            ))}
          </div>

          {/* Active Step Deep-Dive Inspector Panel */}
          {(() => {
            const current = heroSteps.find((s) => s.id === activeStep) || heroSteps[2];
            return (
              <div className="p-6 md:p-8 bg-[#0B0C10] grid grid-cols-1 lg:grid-cols-12 gap-6">
                
                {/* Left: Event Details & Counterfactual Analysis */}
                <div className="lg:col-span-7 space-y-5">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono uppercase px-2.5 py-1 rounded bg-[#171922] border border-[#262833] text-gray-300">
                      Step #{current.id} Inspector
                    </span>
                    <span className={`text-xs font-mono px-3 py-1 rounded-full border ${current.statusColor}`}>
                      {current.status}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">{current.title}</h3>
                    <p className="text-sm text-gray-300 font-mono bg-[#111216] border border-[#262833] p-3.5 rounded-xl leading-relaxed">
                      {current.details}
                    </p>
                  </div>

                  {/* Counterfactual Insight Callout */}
                  <div className={`p-4 rounded-xl border ${
                    current.id === 3 
                      ? 'bg-[#FF3E24]/10 border-[#FF3E24]/40 text-[#FF8573]' 
                      : current.id === 4
                      ? 'bg-red-500/10 border-red-500/30 text-red-300'
                      : 'bg-[#171922] border-[#262833] text-gray-300'
                  }`}>
                    <div className="flex items-start gap-3">
                      {current.id === 3 ? (
                        <AlertTriangle className="w-5 h-5 text-[#FF3E24] flex-shrink-0 mt-0.5" />
                      ) : current.id === 4 ? (
                        <ShieldAlert className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                      ) : (
                        <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                      )}
                      <div>
                        <div className="text-xs font-mono uppercase font-bold tracking-wider mb-1">
                          {current.id === 3 ? "BIFURA ROOT-CAUSE DIAGNOSIS" : current.id === 4 ? "SAFETY INTERCEPTION LOG" : "STATE VERIFICATION"}
                        </div>
                        <div className="text-sm font-medium text-white">{current.delta}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right: Code / Schema Trace Diff View */}
                <div className="lg:col-span-5 flex flex-col justify-between bg-[#111216] border border-[#262833] rounded-xl p-4 font-mono text-xs">
                  <div className="flex items-center justify-between pb-3 border-b border-[#262833] text-[11px] text-gray-400">
                    <span className="flex items-center gap-1.5 text-gray-300">
                      <Code2 className="w-3.5 h-3.5 text-[#00D2FF]" />
                      Trace Telemetry Diff
                    </span>
                    <span className="text-[#9CA3AF]">Memory Delta: +1.4MB</span>
                  </div>

                  <div className="py-4 space-y-2 text-gray-300 leading-relaxed overflow-x-auto">
                    {current.id === 3 ? (
                      <>
                        <div className="text-gray-500">// Expected instruction state:</div>
                        <div className="text-emerald-400 bg-emerald-950/30 p-1.5 rounded border border-emerald-800/40">
                          + target_scope: "staging_cluster_02"
                        </div>
                        <div className="text-gray-500 pt-1">// Actual hallucinated output:</div>
                        <div className="text-[#FF8573] bg-[#FF3E24]/15 p-1.5 rounded border border-[#FF3E24]/30">
                          - DDL: "DROP TABLE core_ledger_v2 CASCADE;"
                        </div>
                        <div className="text-xs text-amber-400 pt-1 flex items-center gap-1">
                          <Zap className="w-3 h-3" />
                          <span>Divergence certainty score: 99.82%</span>
                        </div>
                      </>
                    ) : current.id === 4 ? (
                      <>
                        <div className="text-gray-500">// Safety Policy Interceptor:</div>
                        <div className="text-red-400 bg-red-950/30 p-2 rounded border border-red-800/40">
                          [BLOCK] Action flagged: Unbounded DDL on production shard.
                        </div>
                        <div className="text-gray-400 pt-2">
                          Status: Tri-state gatekeeper returned <strong className="text-white">BLOCK</strong>.
                          Tool dispatch dropped before database connection opened.
                        </div>
                      </>
                    ) : current.id === 5 ? (
                      <>
                        <div className="text-emerald-400">// Deterministic Replay:</div>
                        <div className="text-emerald-300 bg-emerald-950/40 p-2 rounded border border-emerald-800/40">
                          ✓ 24/24 Regression test suites passed.
                          ✓ Zero production tables dropped.
                          ✓ Fix hash: 0x9f88c... sealed.
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="text-gray-400">Token payload: valid JSON schema</div>
                        <div className="text-gray-500">Latency: 210ms | Context window: 4,120 tokens</div>
                        <div className="text-emerald-400">Memory consistency verified.</div>
                      </>
                    )}
                  </div>

                  <div className="pt-3 border-t border-[#262833] flex items-center justify-between text-[11px] text-gray-500">
                    <span>Engine: Bifura v3.4</span>
                    <span className="text-[#00D2FF]">Veritas Certified</span>
                  </div>
                </div>

              </div>
            );
          })()}

        </div>

      </div>
    </section>
  );
}
