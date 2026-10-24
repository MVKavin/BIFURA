import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  GitBranch, 
  Network, 
  ShieldAlert, 
  CheckCircle2, 
  ArrowRight,
  Database,
  Lock,
  Layers,
  Terminal
} from 'lucide-react';

export default function ServiceTabSwitcher({ onOpenDemo }) {
  const [activeTab, setActiveTab] = useState('root-cause');

  const services = [
    {
      id: 'root-cause',
      label: 'Root-Cause Pinpointing',
      badge: 'Causal Backtracking',
      title: 'Isolating the spark before the fire',
      desc: 'Conventional APM loggers catch the terminal exception. BIFURA traverses the evidence graph backward to isolate the earliest divergence where intent drifted from specification.',
      stat: '5 Steps Earlier',
      statSub: 'Average detection advantage',
      preview: {
        type: 'timeline',
        headline: 'Trace Comparison #BF-8942',
        sub: 'Earliest divergence located at Step #3 (SQL Plan generation)',
        codeSnippet: `// BIFURA Causal Delta Analyzer:
Expected: { scope: "staging_cluster", ddl: "DRY_RUN" }
Observed: { scope: "unfiltered", ddl: "DROP CASCADE" }
Delta: Context parameter loss across recursive tool invocation.`
      }
    },
    {
      id: 'blast-radius',
      label: 'Blast Radius Mapping',
      badge: 'Directed Acyclic Graph',
      title: 'Real-time topological impact graph',
      desc: 'Visualizes the cascade of contaminated agent outputs across databases, microservices, external payment gateways, and client-facing webhooks before state commits are executed.',
      stat: 'Zero Mutations',
      statSub: 'Contained prior to corruption',
      preview: {
        type: 'dag',
        headline: 'DAG Ripple Containment',
        sub: '4 downstream touchpoints isolated',
        nodes: [
          { name: 'PostgreSQL: core_ledger_v2', status: 'SHIELDED', color: 'text-emerald-400 bg-emerald-950/40 border-emerald-800' },
          { name: 'Stripe Settlement Webhook', status: 'CONTAINED', color: 'text-cyan-400 bg-cyan-950/40 border-cyan-800' },
          { name: 'Kafka Event Dispatcher', status: 'INTERCEPTED', color: 'text-amber-400 bg-amber-950/40 border-amber-800' },
          { name: 'Slack DPO Incident Alert', status: 'DISPATCHED', color: 'text-blue-400 bg-blue-950/40 border-blue-800' }
        ]
      }
    },
    {
      id: 'safety-engine',
      label: 'Tri-State Safety Engine',
      badge: 'ALLOW / REVIEW / BLOCK',
      title: 'Active policy enforcement at runtime',
      desc: 'Tool executions pass through our sub-14ms edge gatekeeper. Non-destructive queries pass instantly, sensitive balance transfers trigger human sign-off, and destructive commands are blocked.',
      stat: '< 14ms',
      statSub: 'Edge evaluation latency',
      preview: {
        type: 'safety',
        headline: 'Active Policy Interceptor',
        sub: 'Deterministic tool-call classification',
        rules: [
          { verdict: 'ALLOW', text: 'Read-only catalog introspection', time: '1.2ms' },
          { verdict: 'REVIEW', text: 'Wire transfer exceeding €500 threshold', time: 'Pending Human Signature' },
          { verdict: 'BLOCK', text: 'Destructive DDL on production cluster', time: 'Zero Bytes Written' }
        ]
      }
    },
    {
      id: 'replay-cicd',
      label: 'Deterministic Replay CI/CD',
      badge: 'Regression Shield',
      title: 'Automated patch synthesis and test fixtures',
      desc: 'Generates targeted prompt and schema constraints to permanently seal the flaw. Executes regression test suites against frozen incident state fixtures before production redeployment.',
      stat: '100% Pass Rate',
      statSub: 'Certified zero-regression',
      preview: {
        type: 'replay',
        headline: 'Automated CI/CD Verification Harness',
        sub: '24/24 regression test fixtures passed',
        testLines: [
          '✓ replay_fixture_incident_8942.json ... PASSED (410ms)',
          '✓ regression_test_multi_shard.py ...... PASSED (380ms)',
          '✓ pydantic_schema_strict_bound ....... PASSED (120ms)',
          '✓ zero_regression_check .............. PASSED (90ms)'
        ]
      }
    }
  ];

  const currentService = services.find(s => s.id === activeTab) || services[0];

  return (
    <div className="rounded-apple-lg border border-[#e5e5ea] bg-[#ffffff] shadow-apple-product overflow-hidden p-6 sm:p-10 my-8">
      
      {/* Tab Switcher Bar with Framer Motion layoutId="activePill" */}
      <div className="flex flex-wrap items-center gap-2 p-1.5 rounded-apple-pill bg-[#f5f5f7] border border-[#e5e5ea] mb-8">
        {services.map((s) => {
          const isActive = activeTab === s.id;
          return (
            <button
              key={s.id}
              onClick={() => setActiveTab(s.id)}
              className={`relative px-4 py-2 rounded-apple-pill text-[13px] sm:text-[14px] font-medium transition-colors select-none z-10 ${
                isActive ? 'text-white' : 'text-[#86868b] hover:text-[#1d1d1f]'
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="activePill"
                  transition={{
                    type: "spring",
                    stiffness: 400,
                    damping: 35,
                  }}
                  className="absolute inset-0 rounded-apple-pill bg-[#FF3E24] shadow-sm z-[-1]"
                />
              )}
              <span>{s.label}</span>
            </button>
          );
        })}
      </div>

      {/* Grid: Left Description + Right Interactive Preview with Crossfade / Slide Wipe */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        
        {/* Left Column: Editorial Service Description */}
        <div className="lg:col-span-5 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-apple-pill bg-[#FF3E24]/10 text-[#FF3E24] text-[11px] font-mono font-bold uppercase tracking-wider">
            {currentService.badge}
          </div>

          <h3 className="text-[26px] sm:text-[32px] font-semibold text-[#1d1d1f] tracking-tight leading-[1.15]">
            {currentService.title}
          </h3>

          <p className="text-[15px] text-[#86868b] leading-relaxed">
            {currentService.desc}
          </p>

          <div className="pt-4 border-t border-[#f0f0f0] flex items-baseline gap-3">
            <span className="text-[36px] font-bold text-[#FF3E24] tracking-tight">
              {currentService.stat}
            </span>
            <span className="text-[13px] text-[#86868b]">
              {currentService.statSub}
            </span>
          </div>
        </div>

        {/* Right Column: Intentional Slide Wipe Crossfade (scale: 0.98 -> 1, opacity: 0 -> 1 over 400ms) */}
        <div className="lg:col-span-7">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, scale: 0.98, y: 12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: -12 }}
              transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
              className="p-6 sm:p-8 rounded-apple-lg bg-[#0B0C10] border border-[#262833] text-white shadow-2xl font-mono text-[13px]"
            >
              <div className="flex items-center justify-between pb-4 border-b border-[#262833] mb-5 text-[11px] text-[#a1a1a6]">
                <span className="font-semibold text-white">{currentService.preview.headline}</span>
                <span className="text-[#00D2FF]">{currentService.preview.sub}</span>
              </div>

              {/* Conditional preview payload based on active tab */}
              {currentService.preview.type === 'timeline' && (
                <div className="space-y-3">
                  <div className="p-3.5 rounded-apple-sm bg-[#171922] border border-[#262833] text-[#e0e0e0] leading-relaxed">
                    <pre className="whitespace-pre-wrap">{currentService.preview.codeSnippet}</pre>
                  </div>
                  <div className="text-[11px] text-[#34c759] flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-[#34c759]" />
                    Counterfactual divergence isolated at T+480ms.
                  </div>
                </div>
              )}

              {currentService.preview.type === 'dag' && (
                <div className="space-y-2.5">
                  {currentService.preview.nodes.map((node, i) => (
                    <div
                      key={i}
                      className="p-3 rounded-apple-sm bg-[#171922] border border-[#262833] flex items-center justify-between text-[12px]"
                    >
                      <span className="text-gray-200">{node.name}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${node.color}`}>
                        {node.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}

              {currentService.preview.type === 'safety' && (
                <div className="space-y-2.5">
                  {currentService.preview.rules.map((rule, i) => (
                    <div
                      key={i}
                      className="p-3 rounded-apple-sm bg-[#171922] border border-[#262833] flex items-center justify-between text-[12px]"
                    >
                      <div className="flex items-center gap-2.5">
                        <span className={`px-2 py-0.5 rounded font-bold text-[10px] ${
                          rule.verdict === 'ALLOW' ? 'bg-[#34c759]/20 text-[#34c759]' :
                          rule.verdict === 'REVIEW' ? 'bg-[#ff9f0a]/20 text-[#ff9f0a]' :
                          'bg-[#ff3b30]/20 text-[#ff3b30]'
                        }`}>
                          {rule.verdict}
                        </span>
                        <span className="text-gray-300">{rule.text}</span>
                      </div>
                      <span className="text-[11px] text-gray-500">{rule.time}</span>
                    </div>
                  ))}
                </div>
              )}

              {currentService.preview.type === 'replay' && (
                <div className="space-y-2 text-[#34c759] bg-[#14151B] p-4 rounded-apple-sm border border-[#262833] text-[12px]">
                  {currentService.preview.testLines.map((line, i) => (
                    <div key={i}>{line}</div>
                  ))}
                  <div className="pt-2 text-white font-semibold">
                    Hash 0x9f88c verified for deployment.
                  </div>
                </div>
              )}

              <div className="mt-5 pt-4 border-t border-[#262833] flex items-center justify-between text-[11px] text-gray-400">
                <span>Architecture BIFURA v3.4</span>
                <button
                  onClick={onOpenDemo}
                  className="text-[#FF3E24] hover:underline inline-flex items-center gap-1 font-semibold"
                >
                  Schedule Demo <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </motion.div>
          </AnimatePresence>
        </div>

      </div>

    </div>
  );
}
