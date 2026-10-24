import React, { useState } from 'react';
import { 
  GitBranch, 
  Terminal, 
  Network, 
  ShieldCheck, 
  RefreshCw, 
  ArrowRight, 
  Cpu, 
  Layers, 
  CheckCircle2, 
  Check, 
  Flame,
  Binary
} from 'lucide-react';

export default function WorkflowAccordion({ t, onOpenDemoModal }) {
  const [activeStage, setActiveStage] = useState(0);

  const stageDemos = [
    {
      title: "OpenTelemetry SDK Ingestion Hook",
      badge: "LATENCY < 1.2ms",
      badgeColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
      content: `import { BifuraTracer } from "@bifura/sdk";

// Initialize zero-overhead telemetry tracer
const tracer = new BifuraTracer({
  apiKey: process.env.BIFURA_API_KEY,
  captureStateSnapshots: true,
  streamTelemetry: true,
  interceptionMode: "ACTIVE_ENFORCEMENT"
});

// Automatic wrapper for LangGraph / CrewAI
export const agent = tracer.wrapAgent(myMultiStepAgent);`,
      footer: "Compatible avec Python 3.10+, TypeScript 5+, Go 1.22+",
    },
    {
      title: "Counterfactual State Divergence Engine",
      badge: "ROOT CAUSE CONFIDENCE: 99.8%",
      badgeColor: "bg-[#FF3E24]/20 text-[#FF8573] border-[#FF3E24]/40",
      content: `[BIFURA-ANALYZER] Comparing execution against expected schema...
Step 1: parse_intent -> MATCH (deviation: 0.00)
Step 2: query_catalog -> MATCH (deviation: 0.02)
Step 3: plan_migration -> CRITICAL DIVERGENCE DETECTED
  Expected: { target: "staging_cluster_02", action: "DRY_RUN" }
  Observed: { target: "production_master", ddl: "DROP CASCADE" }
  Cause: Context parameter loss across recursive tool call #3.`,
      footer: "Bifura isole la dérive 5 étapes avant le crash effectif.",
    },
    {
      title: "Real-Time Blast Radius DAG Computation",
      badge: "AFFECTED NODES: 4 ISOLATED",
      badgeColor: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
      content: `GRAPH_TOPOLOGY = {
  "root_event": "hallucinated_sql_ddl_v2",
  "threat_propagation": [
    { "target": "db.core_ledger", "type": "WRITE_CORRUPTION", "status": "SHIELDED" },
    { "target": "api.stripe_webhook", "type": "RETRY_STORM", "status": "CONTAINED" },
    { "target": "queue.kafka_events", "type": "POISON_PILL", "status": "INTERCEPTED" },
    { "target": "channel.slack_dpo", "type": "INCIDENT_DISPATCH", "status": "NOTIFIED" }
  ]
}`,
      footer: "Graphe de causalité calculé en temps réel en moins de 6ms.",
    },
    {
      title: "Tri-State Safety Interceptor Evaluation",
      badge: "POLICY VERDICT: BLOCK",
      badgeColor: "bg-red-500/20 text-red-400 border-red-500/40",
      content: `// Safety Policy Evaluation Rulebook
MATCH tool_execution.type:
  CASE "read_only" => ALLOW (execute immediately)
  CASE "mutation_reversible" AND amount < 500 => ALLOW
  CASE "mutation_sensitive" => REVIEW (require OTP / Slack approval)
  CASE "destructive_ddl" OR "pii_leak" => BLOCK
    
[ACTION] Execution blocked on thread #T-4819.
[METRIC] Production downtime avoided: 100%.`,
      footer: "Aucune action destructive ne touche l'infrastructure.",
    },
    {
      title: "Deterministic Replay & Regression Harness",
      badge: "REPLAY PASS RATE: 100%",
      badgeColor: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
      content: `Running Bifura Deterministic Replay Suite...
  ✓ replay_fixture_incident_8942.json ... PASSED (410ms)
  ✓ replay_fixture_incident_8943.json ... PASSED (380ms)
  ✓ schema_strict_bound_test.py ...... PASSED (120ms)
  ✓ zero_regression_check ........... PASSED (90ms)

All 24/24 replay fixtures validated against frozen LLM states.
Fix hash 0x7b19a ready for zero-downtime hot reload.`,
      footer: "Certification absolue avant réintégration au cluster live.",
    },
  ];

  return (
    <section id="workflow" className="py-24 md:py-32 bg-[#0B0C10] text-white relative overflow-hidden bg-grid-pattern border-b border-[#262833]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mb-16 md:mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#171922] border border-[#262833] text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-4">
            <span>{t.workflow.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-white leading-[1.1]">
            {t.workflow.title}
          </h2>
          <p className="mt-5 text-lg sm:text-xl text-gray-400 leading-relaxed">
            {t.workflow.subtitle}
          </p>
        </div>

        {/* 5-Stage Interactive Tabs & Dynamic Preview */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Left Column: 5 Stage Selectors */}
          <div className="lg:col-span-5 space-y-3">
            {t.workflow.steps.map((st, idx) => {
              const isActive = idx === activeStage;
              return (
                <button
                  key={idx}
                  onClick={() => setActiveStage(idx)}
                  className={`w-full p-5 rounded-2xl text-left border transition-all duration-300 relative group ${
                    isActive
                      ? 'bg-[#171922] border-[#FF3E24] shadow-xl shadow-[#FF3E24]/10'
                      : 'bg-[#111216] border-[#262833] hover:border-gray-600 hover:bg-[#14151B]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${
                      isActive ? 'bg-[#FF3E24] text-white' : 'bg-[#1C1E27] text-gray-400'
                    }`}>
                      ÉTAPE {st.step}
                    </span>
                    <span className="text-[11px] font-mono text-gray-400 group-hover:text-gray-200">
                      {st.badge}
                    </span>
                  </div>

                  <h3 className={`font-display font-bold text-lg mb-1.5 transition-colors ${
                    isActive ? 'text-white' : 'text-gray-300 group-hover:text-white'
                  }`}>
                    {st.name}
                  </h3>

                  <p className="text-xs text-gray-400 leading-relaxed line-clamp-2 font-sans">
                    {st.short}
                  </p>

                  {/* Active indicator bar */}
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-10 bg-[#FF3E24] rounded-r" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Right Column: Dynamic Stage Inspection Window */}
          <div className="lg:col-span-7 bg-[#111216] border border-[#262833] rounded-3xl p-6 md:p-8 flex flex-col justify-between shadow-2xl relative sticky top-28">
            <div>
              {/* Window Header */}
              <div className="flex flex-wrap items-center justify-between pb-4 border-b border-[#262833] gap-3 mb-6">
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                    <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="font-display font-bold text-sm text-white">
                    {stageDemos[activeStage].title}
                  </span>
                </div>

                <span className={`text-[11px] font-mono px-2.5 py-1 rounded-full border ${stageDemos[activeStage].badgeColor} font-bold`}>
                  {stageDemos[activeStage].badge}
                </span>
              </div>

              {/* Stage Description Expanded */}
              <div className="mb-6 p-4 rounded-xl bg-[#0B0C10] border border-[#262833]">
                <div className="text-xs font-mono text-[#FF3E24] font-bold uppercase mb-1">
                  Explication Opérationnelle :
                </div>
                <div className="text-sm text-gray-300 leading-relaxed font-sans">
                  {t.workflow.steps[activeStage].detail}
                </div>
              </div>

              {/* Code / Visual Terminal */}
              <div className="bg-[#0B0C10] rounded-2xl border border-[#262833] p-5 font-mono text-xs overflow-x-auto shadow-inner text-gray-200 leading-relaxed">
                <pre className="whitespace-pre-wrap">{stageDemos[activeStage].content}</pre>
              </div>
            </div>

            {/* Bottom Panel */}
            <div className="pt-6 mt-6 border-t border-[#262833] flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs text-gray-400">
              <span className="text-gray-400">
                {stageDemos[activeStage].footer}
              </span>
              <button
                onClick={onOpenDemoModal}
                className="inline-flex items-center gap-1.5 text-[#FF3E24] hover:text-[#FF8573] font-bold transition-colors"
              >
                Intégrer ce protocole <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
