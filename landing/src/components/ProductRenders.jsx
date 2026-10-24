import React from 'react';

/**
 * Museum-grade product renders that rest on surface tiles
 * with the signature Apple product drop shadow: rgba(0, 0, 0, 0.22) 3px 5px 30px 0
 */

export function BifuraCoreEngineRender({ isDark = false }) {
  return (
    <div className="relative mx-auto max-w-4xl w-full px-4 my-8">
      {/* Product Display Surface with Apple Signature Drop Shadow */}
      <div className={`relative rounded-apple-lg border ${
        isDark ? 'bg-[#18181a] border-[#333336]' : 'bg-[#ffffff] border-[#e0e0e0]'
      } shadow-apple-product overflow-hidden transition-all duration-500`}>
        
        {/* Subtle top bezel / status header */}
        <div className={`flex items-center justify-between px-6 py-4 border-b ${
          isDark ? 'bg-[#141416] border-[#2c2c30]' : 'bg-[#fbfbfd] border-[#ebebef]'
        }`}>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[#1d1d1f]/40 dark:bg-white/40" />
              <span className="w-2.5 h-2.5 rounded-full bg-[#1d1d1f]/40 dark:bg-white/40" />
              <span className="w-2.5 h-2.5 rounded-full bg-[#1d1d1f]/40 dark:bg-white/40" />
            </div>
            <span className={`text-[12px] font-mono tracking-tight ${isDark ? 'text-[#86868b]' : 'text-[#86868b]'}`}>
              BIFURA REASONING ENGINE // TRACE BUFFER #BF-9042
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-[12px] font-mono text-[#0066cc] dark:text-[#2997ff] font-medium">
              100% DETERMINISTIC REPLAY CAPABLE
            </span>
          </div>
        </div>

        {/* Interior Product View: The 5-Step Incident Resolution Workflow */}
        <div className="p-8 sm:p-12">
          {/* Main Hero Architecture Graphic */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center">
            
            {/* Step 1 */}
            <div className={`p-5 rounded-apple-sm border ${
              isDark ? 'bg-[#202023] border-[#333336]' : 'bg-[#f5f5f7] border-[#e5e5ea]'
            }`}>
              <div className="text-[11px] font-mono text-[#86868b] uppercase mb-1">Step 01</div>
              <div className={`text-[15px] font-semibold mb-2 ${isDark ? 'text-white' : 'text-[#1d1d1f]'}`}>
                User Prompt
              </div>
              <div className="text-[12px] text-[#86868b] leading-snug">
                "Reclaim test storage across staging cluster"
              </div>
              <div className="mt-3 flex items-center gap-1.5 text-[11px] font-mono text-[#34c759]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#34c759]" />
                Intent Verified
              </div>
            </div>

            {/* Step 2 */}
            <div className={`p-5 rounded-apple-sm border ${
              isDark ? 'bg-[#202023] border-[#333336]' : 'bg-[#f5f5f7] border-[#e5e5ea]'
            }`}>
              <div className="text-[11px] font-mono text-[#86868b] uppercase mb-1">Step 02</div>
              <div className={`text-[15px] font-semibold mb-2 ${isDark ? 'text-white' : 'text-[#1d1d1f]'}`}>
                Catalog Scan
              </div>
              <div className="text-[12px] text-[#86868b] leading-snug">
                18 database tables returned via read-only introspection
              </div>
              <div className="mt-3 flex items-center gap-1.5 text-[11px] font-mono text-[#34c759]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#34c759]" />
                ALLOW: Read
              </div>
            </div>

            {/* Step 3 - THE CRUCIAL ROOT CAUSE PINPOINT */}
            <div className={`p-5 rounded-apple-sm border relative ring-2 ${
              isDark ? 'bg-[#281b1d] border-[#ff453a]/60 ring-[#ff453a]/30' : 'bg-[#fff5f5] border-[#ff3b30]/50 ring-[#ff3b30]/20'
            }`}>
              <div className="absolute -top-3 left-4 px-2 py-0.5 rounded-full bg-[#ff3b30] text-white text-[9px] font-mono font-bold uppercase tracking-wider">
                Root Cause
              </div>
              <div className="text-[11px] font-mono text-[#ff3b30] uppercase mb-1">Step 03</div>
              <div className={`text-[15px] font-semibold mb-2 ${isDark ? 'text-white' : 'text-[#1d1d1f]'}`}>
                Plan Drift
              </div>
              <div className="text-[12px] text-[#ff3b30] dark:text-[#ff8573] leading-snug font-mono">
                DROP TABLE core_ledger;
              </div>
              <div className="mt-3 text-[11px] font-mono font-semibold text-[#ff3b30]">
                Earliest Divergence
              </div>
            </div>

            {/* Step 4 - THE SAFETY SENTINEL */}
            <div className={`p-5 rounded-apple-sm border ${
              isDark ? 'bg-[#1b2533] border-[#0066cc]/50' : 'bg-[#f0f7ff] border-[#0066cc]/40'
            }`}>
              <div className="text-[11px] font-mono text-[#0066cc] dark:text-[#2997ff] uppercase mb-1">Step 04</div>
              <div className={`text-[15px] font-semibold mb-2 ${isDark ? 'text-white' : 'text-[#1d1d1f]'}`}>
                Safety Intercept
              </div>
              <div className="text-[12px] text-[#86868b] leading-snug">
                Destructive DDL caught before socket transmission
              </div>
              <div className="mt-3 flex items-center gap-1.5 text-[11px] font-mono text-[#ff3b30] font-semibold">
                <span className="w-1.5 h-1.5 rounded-full bg-[#ff3b30]" />
                BLOCK: Zero Bytes
              </div>
            </div>

            {/* Step 5 - THE VERIFIED FIX */}
            <div className={`p-5 rounded-apple-sm border ${
              isDark ? 'bg-[#1c2921] border-[#30d158]/50' : 'bg-[#f2faf4] border-[#34c759]/40'
            }`}>
              <div className="text-[11px] font-mono text-[#30d158] uppercase mb-1">Step 05</div>
              <div className={`text-[15px] font-semibold mb-2 ${isDark ? 'text-white' : 'text-[#1d1d1f]'}`}>
                Verified Fix
              </div>
              <div className="text-[12px] text-[#86868b] leading-snug">
                Pydantic parameter bound + 24/24 replay tests green
              </div>
              <div className="mt-3 flex items-center gap-1.5 text-[11px] font-mono text-[#34c759] font-bold">
                ✓ Sealed in CI/CD
              </div>
            </div>

          </div>

          {/* Micro Telemetry Bar */}
          <div className={`mt-8 pt-6 border-t flex flex-wrap items-center justify-between text-[12px] font-mono ${
            isDark ? 'border-[#2c2c30] text-[#86868b]' : 'border-[#ebebef] text-[#86868b]'
          }`}>
            <div>Counterfactual Causal Inference: <strong className={isDark ? 'text-white' : 'text-[#1d1d1f]'}>Active</strong></div>
            <div>Blast Radius DAG: <strong className={isDark ? 'text-white' : 'text-[#1d1d1f]'}>Contained (4 nodes)</strong></div>
            <div>Telemetry Overhead: <strong className="text-[#0066cc] dark:text-[#2997ff]">11.4 ms</strong></div>
          </div>
        </div>

      </div>
    </div>
  );
}

/**
 * Shared look for the dark product cards, matched to the forest-green pages
 * (page #061811, cards #0a241a, emerald borders, sage text #9bb0a5).
 * Classes are chosen explicitly from `isDark`, so the cards never depend on the
 * visitor's operating-system dark-mode setting.
 */
function cardTheme(isDark) {
  return isDark
    ? {
        card: 'bg-[#0a241a] border-emerald-800/30 shadow-[0_24px_60px_-20px_rgba(0,0,0,0.6)]',
        divider: 'border-emerald-900/50',
        kicker: 'text-emerald-400',
        title: 'text-white',
        muted: 'text-[#9bb0a5]',
        pill: 'bg-emerald-950/70 border border-emerald-800/40 text-emerald-300',
        lane: 'bg-[#061811] border border-emerald-900/50',
        chip: 'bg-[#0d2c20] border border-emerald-900/60 text-[#d6e7de]',
        chipMuted: 'bg-[#0d2c20] border border-emerald-900/40 text-[#7f988b]',
        arrow: 'text-emerald-700',
        tile: 'bg-[#061811] border-emerald-900/50',
        highlight: 'text-emerald-300',
      }
    : {
        card: 'bg-[#ffffff] border-[#e0e0e0] shadow-apple-product',
        divider: 'border-[#e5e5ea]',
        kicker: 'text-[#047857]',
        title: 'text-[#1d1d1f]',
        muted: 'text-[#6e6e73]',
        pill: 'bg-[#f2faf4] border border-[#047857]/20 text-[#047857]',
        lane: 'bg-[#f5f5f7] border border-[#e5e5ea]',
        chip: 'bg-[#ffffff] border border-[#e5e5ea] text-[#1d1d1f]',
        chipMuted: 'bg-[#ffffff] border border-[#e5e5ea] text-[#86868b]',
        arrow: 'text-[#86868b]',
        tile: 'bg-[#f5f5f7] border-[#e5e5ea]',
        highlight: 'text-[#047857]',
      };
}

function CardHeader({ t, kicker, title, badge, badgeClass }) {
  return (
    <div className={`flex flex-wrap items-center justify-between gap-3 pb-6 border-b ${t.divider} mb-6 text-left`}>
      <div>
        <span className={`text-[12px] font-mono uppercase font-bold tracking-wider ${t.kicker}`}>{kicker}</span>
        <h4 className={`text-[20px] font-semibold mt-0.5 ${t.title}`}>{title}</h4>
      </div>
      <span className={`px-3 py-1 rounded-apple-pill text-[12px] font-mono font-medium ${badgeClass || t.pill}`}>
        {badge}
      </span>
    </div>
  );
}

export function CausalTimelineRender({ isDark = false }) {
  const t = cardTheme(isDark);
  const chip = `px-2.5 py-1 rounded-md ${t.chip}`;
  const chipMuted = `px-2.5 py-1 rounded-md ${t.chipMuted}`;
  const arrow = <span className={t.arrow}>→</span>;
  return (
    <div className="relative mx-auto max-w-4xl w-full px-4 my-8">
      <div className={`relative rounded-apple-lg border ${t.card} overflow-hidden p-8 sm:p-10`}>

        <CardHeader t={t} kicker="Comparative State Evaluation"
                    title="Expected Trajectory vs. Observed Execution Trace" badge="Microsecond Precision" />

        {/* Split comparison lanes */}
        <div className="space-y-4 font-mono text-[13px]">
          <div className="flex items-center gap-3">
            <span className="w-24 shrink-0 text-left text-emerald-400 font-semibold text-[11px] uppercase tracking-wider">Expected</span>
            <div className={`flex-1 flex flex-wrap items-center gap-2 p-3 rounded-apple-sm ${t.lane}`}>
              <span className={chip}>Parse</span>{arrow}
              <span className={chip}>Catalog</span>{arrow}
              <span className={chip}>Dry-Run Target</span>{arrow}
              <span className={chip}>Drop Temp Only</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className={`w-24 shrink-0 text-left font-semibold text-[11px] uppercase tracking-wider ${isDark ? 'text-rose-400' : 'text-[#d70015]'}`}>Observed</span>
            <div className={`flex-1 flex flex-wrap items-center gap-2 p-3 rounded-apple-sm border ${
              isDark ? 'bg-[#1d1414]/60 border-rose-900/40' : 'bg-[#fff5f5] border-[#ffd6d6]'
            }`}>
              <span className={chipMuted}>Parse</span>{arrow}
              <span className={chipMuted}>Catalog</span>{arrow}
              <span className={`px-3 py-1 rounded-apple-pill font-bold text-[12px] ${
                isDark ? 'bg-rose-500/90 text-white shadow-[0_6px_18px_-6px_rgba(244,63,94,0.6)]' : 'bg-[#ff3b30] text-white'
              }`}>
                Delta Pinpointed (Step 3)
              </span>{arrow}
              <span className={`px-2.5 py-1 rounded-md line-through ${
                isDark ? 'bg-[#0d2c20] border border-rose-900/40 text-rose-300/80' : 'bg-white border border-[#ffd6d6] text-[#ff3b30]'
              }`}>
                Fatal Crash (Step 8)
              </span>
            </div>
          </div>
        </div>

        <div className={`mt-6 pt-5 border-t ${t.divider} flex flex-wrap items-center justify-between gap-2 text-[13px] ${t.muted}`}>
          <span>Traditional loggers alert at Step 8.</span>
          <span className={`font-medium ${t.highlight}`}>BIFURA isolates the root cause 5 steps earlier.</span>
        </div>

      </div>
    </div>
  );
}

export function BlastRadiusTopologicalRender({ isDark = false }) {
  const t = cardTheme(isDark);
  const assets = [
    ['Database Asset', 'SHIELDED', 'PostgreSQL core_ledger_v2', 'Prevented accidental cascading drop of 4.2M transactional ledgers.'],
    ['Financial Webhook', 'CONTAINED', 'Stripe Settlement Worker', 'Halted exponential retry storm and downstream merchant disputes.'],
    ['Internal Messaging', 'SANITIZED', 'Slack DPO & Engineering', 'Broadcast suppressed prior to unauthorized PII exposure.'],
    ['In-Memory Cache', 'PURGED', 'Redis Session State', 'Poison-pill key invalidations halted before downstream ingestion.'],
  ];
  return (
    <div className="relative mx-auto max-w-4xl w-full px-4 my-8">
      <div className={`relative rounded-apple-lg border ${t.card} overflow-hidden p-8 sm:p-10`}>

        <CardHeader t={t} kicker="Topological Impact Graph" title="Downstream Blast Radius Mapping (DAG)"
                    badge="Zero Unintended Mutations" />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
          {assets.map(([kind, badge, name, text]) => (
            <div key={name} className={`p-4 rounded-apple-sm border ${t.tile}`}>
              <div className="flex items-center justify-between mb-2">
                <span className={`text-[11px] font-mono uppercase ${t.muted}`}>{kind}</span>
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                  isDark ? 'text-emerald-300 bg-emerald-400/10 border border-emerald-700/40' : 'text-[#047857] bg-[#047857]/10'
                }`}>{badge}</span>
              </div>
              <div className={`text-[15px] font-semibold ${t.title}`}>{name}</div>
              <p className={`text-[12px] mt-1 ${t.muted}`}>{text}</p>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

export function SafetyMatrixRender({ isDark = false }) {
  const t = cardTheme(isDark);
  const pillars = isDark
    ? [
        ['ALLOW', 'Pass-Through', 'Idempotent reads, schema queries, read-only analytics, and non-destructive transformations.',
         'Overhead: 1.2ms', 'bg-emerald-950/40 border-emerald-600/35', 'text-emerald-300'],
        ['REVIEW', 'Human-in-the-Loop', 'Ambiguous parameters, financial transactions above €500, or cross-tenant context merges.',
         'Slack & Webhook Dispatch', 'bg-amber-950/25 border-amber-600/30', 'text-amber-300'],
        ['BLOCK', 'Zero Execution', 'Destructive DDL, unmasked PII transmission, infinite recursions, and unverified privilege escalations.',
         'Zero Bytes Altered', 'bg-rose-950/25 border-rose-700/35', 'text-rose-300'],
      ]
    : [
        ['ALLOW', 'Pass-Through', 'Idempotent reads, schema queries, read-only analytics, and non-destructive transformations.',
         'Overhead: 1.2ms', 'bg-[#f0faf2] border-[#34c759]/30', 'text-[#248a3d]'],
        ['REVIEW', 'Human-in-the-Loop', 'Ambiguous parameters, financial transactions above €500, or cross-tenant context merges.',
         'Slack & Webhook Dispatch', 'bg-[#fffbf0] border-[#ff9f0a]/30', 'text-[#b45309]'],
        ['BLOCK', 'Zero Execution', 'Destructive DDL, unmasked PII transmission, infinite recursions, and unverified privilege escalations.',
         'Zero Bytes Altered', 'bg-[#fff5f5] border-[#ff3b30]/30', 'text-[#d70015]'],
      ];
  return (
    <div className="relative mx-auto max-w-4xl w-full px-4 my-8">
      <div className={`relative rounded-apple-lg border ${t.card} overflow-hidden p-8 sm:p-10`}>

        <CardHeader t={t} kicker="Active Enforcement Gatekeeper" title="Tri-State Action Classification Engine"
                    badge="Latency < 14ms" />

        {/* 3 Pillars: ALLOW, REVIEW, BLOCK */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {pillars.map(([name, mode, text, foot, box, accent]) => (
            <div key={name} className={`p-5 rounded-apple-sm border ${box}`}>
              <div className="flex items-center justify-between mb-3">
                <span className={`text-[18px] font-bold ${accent}`}>{name}</span>
                <span className={`text-[11px] font-mono ${accent} opacity-80`}>{mode}</span>
              </div>
              <p className={`text-[13px] leading-relaxed mb-4 ${t.muted}`}>{text}</p>
              <div className={`text-[11px] font-mono font-medium ${accent}`}>{foot}</div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
