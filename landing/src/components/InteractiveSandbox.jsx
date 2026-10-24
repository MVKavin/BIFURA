import React, { useState } from 'react';
import { incidentScenarios } from '../data/incidentScenarios';
import { 
  Terminal, 
  AlertTriangle, 
  ShieldAlert, 
  CheckCircle2, 
  GitBranch, 
  Network, 
  Cpu, 
  ArrowRight, 
  RefreshCw, 
  Lock, 
  Flame, 
  Code2, 
  Database, 
  Play, 
  FileCode2,
  SlidersHorizontal,
  ChevronRight
} from 'lucide-react';

export default function InteractiveSandbox({ t, onOpenDemoModal }) {
  const [activeScenarioId, setActiveScenarioId] = useState('sql');
  const [activeViewTab, setActiveViewTab] = useState('trace'); // trace, blast, safety, fix
  const [selectedStepIndex, setSelectedStepIndex] = useState(2); // Step 3 (0-indexed: 2)

  const scenario = incidentScenarios[activeScenarioId];

  return (
    <section id="sandbox" className="py-24 md:py-32 bg-[#0B0C10] text-white relative overflow-hidden bg-grid-pattern border-b border-[#262833]">
      {/* Editorial Ambient Glow */}
      <div className="absolute top-1/2 right-1/4 w-[500px] h-[500px] bg-[#FF3E24]/5 blur-[160px] pointer-events-none rounded-full" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Section Header */}
        <div className="max-w-3xl mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#171922] border border-[#262833] text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-4">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF3E24] animate-pulse" />
            <span>{t.sandbox.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-white leading-[1.1]">
            {t.sandbox.title}
          </h2>
          <p className="mt-4 text-lg text-gray-400 leading-relaxed">
            {t.sandbox.subtitle}
          </p>
        </div>

        {/* Scenario Selection Tabs */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {t.sandbox.scenarios.map((sc) => {
            const isSelected = sc.id === activeScenarioId;
            return (
              <button
                key={sc.id}
                onClick={() => {
                  setActiveScenarioId(sc.id);
                  setSelectedStepIndex(1); // Reset selected step
                }}
                className={`p-5 rounded-2xl text-left border transition-all duration-300 relative ${
                  isSelected
                    ? 'bg-[#171922] border-[#FF3E24] shadow-xl shadow-[#FF3E24]/10 ring-1 ring-[#FF3E24]/50'
                    : 'bg-[#111216] border-[#262833] hover:border-gray-600 hover:bg-[#14151B]'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase ${
                    sc.severity === 'CRITICAL'
                      ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                      : sc.severity === 'HIGH'
                      ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                      : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                  }`}>
                    {sc.severity}
                  </span>
                  <span className="text-xs font-mono text-gray-400">{sc.category}</span>
                </div>

                <div className="font-display font-bold text-base text-white mb-1.5 flex items-center justify-between">
                  <span>{sc.name}</span>
                  {isSelected && <span className="w-2 h-2 rounded-full bg-[#FF3E24]" />}
                </div>

                <p className="text-xs text-gray-400 line-clamp-2 leading-relaxed">
                  {sc.desc}
                </p>
              </button>
            );
          })}
        </div>

        {/* Interactive Debugger Workbench Window */}
        <div className="rounded-2xl bg-[#111216] border border-[#262833] overflow-hidden shadow-2xl">
          
          {/* Workbench Top Bar & View Tabs */}
          <div className="flex flex-wrap items-center justify-between px-6 py-4 bg-[#14161E] border-b border-[#262833] gap-4">
            <div className="flex items-center gap-3">
              <span className="px-2.5 py-1 rounded bg-[#1C1E27] border border-[#262833] font-mono text-xs text-gray-300">
                Agent: <strong className="text-white">{scenario.agentName}</strong>
              </span>
              <span className="font-mono text-xs text-gray-400 hidden sm:inline">
                Framework: {scenario.framework}
              </span>
              <span className="text-xs font-mono text-emerald-400 hidden md:inline">
                Detected in: {scenario.detectedInMs}ms
              </span>
            </div>

            {/* View Sub-Tabs */}
            <div className="flex items-center bg-[#0B0C10] border border-[#262833] rounded-full p-1 text-xs font-mono">
              <button
                type="button"
                onClick={() => setActiveViewTab('trace')}
                className={`px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5 ${
                  activeViewTab === 'trace'
                    ? 'bg-[#FF3E24] text-white font-bold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <GitBranch className="w-3.5 h-3.5" />
                <span>{t.sandbox.tabs.trace}</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveViewTab('blast')}
                className={`px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5 ${
                  activeViewTab === 'blast'
                    ? 'bg-[#FF3E24] text-white font-bold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <Network className="w-3.5 h-3.5" />
                <span>{t.sandbox.tabs.blast}</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveViewTab('safety')}
                className={`px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5 ${
                  activeViewTab === 'safety'
                    ? 'bg-[#FF3E24] text-white font-bold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <ShieldAlert className="w-3.5 h-3.5" />
                <span>{t.sandbox.tabs.safety}</span>
              </button>

              <button
                type="button"
                onClick={() => setActiveViewTab('fix')}
                className={`px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5 ${
                  activeViewTab === 'fix'
                    ? 'bg-[#FF3E24] text-white font-bold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{t.sandbox.tabs.fix}</span>
              </button>
            </div>
          </div>

          {/* Workbench Body Content */}
          <div className="p-6 md:p-8">
            
            {/* View Tab 1: Trace & Earliest Divergence */}
            {activeViewTab === 'trace' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                {/* Left: Step Trace List */}
                <div className="lg:col-span-5 space-y-3">
                  <div className="text-xs font-mono text-gray-400 uppercase tracking-wider mb-2 flex items-center justify-between">
                    <span>Trace Call Graph</span>
                    <span>5 Steps</span>
                  </div>

                  {scenario.steps.map((st, idx) => {
                    const isSelected = idx === selectedStepIndex;
                    const isRoot = st.status === 'divergence';
                    const isBlocked = st.status === 'blocked';
                    const isVerified = st.status === 'verified';

                    return (
                      <button
                        key={st.step}
                        onClick={() => setSelectedStepIndex(idx)}
                        className={`w-full p-4 rounded-xl text-left border transition-all ${
                          isSelected
                            ? 'bg-[#1C1E27] border-[#FF3E24] shadow-lg'
                            : 'bg-[#14151B] border-[#262833] hover:border-gray-600'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="font-mono text-xs text-gray-400">{st.time}</span>
                          <span className={`text-[10px] font-mono px-2 py-0.5 rounded border font-bold ${
                            isRoot
                              ? 'bg-[#FF3E24]/20 text-[#FF8573] border-[#FF3E24]/40'
                              : isBlocked
                              ? 'bg-red-500/20 text-red-400 border-red-500/30'
                              : isVerified
                              ? 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30'
                              : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          }`}>
                            {st.statusLabel}
                          </span>
                        </div>

                        <div className="font-semibold text-sm text-white flex items-center gap-2">
                          <span>{st.step}. {st.name}</span>
                          {isRoot && <Flame className="w-4 h-4 text-[#FF3E24] animate-pulse" />}
                        </div>
                        <div className="font-mono text-xs text-gray-400 truncate mt-0.5">
                          Tool: <span className="text-gray-300">{st.tool}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Right: Selected Step Inspector & Counterfactual Diff */}
                {(() => {
                  const curr = scenario.steps[selectedStepIndex] || scenario.steps[0];
                  return (
                    <div className="lg:col-span-7 bg-[#0B0C10] border border-[#262833] rounded-2xl p-6 flex flex-col justify-between font-mono">
                      <div>
                        <div className="flex items-center justify-between pb-4 border-b border-[#262833] mb-5">
                          <div className="flex items-center gap-2">
                            <span className="px-2.5 py-1 rounded bg-[#171922] text-xs text-gray-300">
                              Inspection Étape #{curr.step}
                            </span>
                            <span className="text-xs text-gray-400">{curr.tool}</span>
                          </div>
                          <span className="text-xs text-[#00D2FF]">
                            {curr.tokens} tokens consommés
                          </span>
                        </div>

                        <div className="space-y-4">
                          <div>
                            <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Description de l'action :</div>
                            <div className="text-sm text-white font-sans bg-[#111216] p-3 rounded-xl border border-[#262833]">
                              {curr.description}
                            </div>
                          </div>

                          {/* Expected vs Actual Diff */}
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                            <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-800/40">
                              <div className="text-[11px] text-emerald-400 font-bold uppercase mb-1">
                                ✓ Comportement Attendu
                              </div>
                              <div className="text-xs text-emerald-200/90 leading-relaxed font-sans">
                                {curr.expected || "Exécution nominale de la politique."}
                              </div>
                            </div>

                            <div className={`p-3.5 rounded-xl border ${
                              curr.status === 'divergence' 
                                ? 'bg-[#FF3E24]/10 border-[#FF3E24]/40 text-[#FF8573]'
                                : curr.status === 'blocked'
                                ? 'bg-red-950/30 border-red-800/40 text-red-300'
                                : 'bg-[#171922] border-[#262833] text-gray-300'
                            }`}>
                              <div className="text-[11px] font-bold uppercase mb-1">
                                ⚠ Comportement Réel Observé
                              </div>
                              <div className="text-xs leading-relaxed font-sans">
                                {curr.actual || curr.actionTaken}
                              </div>
                            </div>
                          </div>

                          {curr.delta && (
                            <div className="p-3.5 rounded-xl bg-[#FF3E24]/15 border border-[#FF3E24]/40 text-[#FF8573] text-xs">
                              <div className="font-bold flex items-center gap-1.5 uppercase mb-1">
                                <AlertTriangle className="w-4 h-4 text-[#FF3E24]" />
                                Diagnostic d'Origine (Root Cause Delta) :
                              </div>
                              <div className="font-sans text-white text-xs">{curr.delta}</div>
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="pt-5 mt-6 border-t border-[#262833] flex items-center justify-between text-xs text-gray-400">
                        <span>Isolation contrefactuelle : Active</span>
                        <button
                          onClick={() => setActiveViewTab('blast')}
                          className="inline-flex items-center gap-1 text-[#FF3E24] hover:underline font-semibold"
                        >
                          Voir l'impact en aval (Blast Radius) <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  );
                })()}

              </div>
            )}

            {/* View Tab 2: Downstream Blast Radius DAG */}
            {activeViewTab === 'blast' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-display font-bold text-xl text-white">
                      Arborescence de Propagation des Effets de Bord (Blast Radius)
                    </h3>
                    <p className="text-sm text-gray-400 mt-1">
                      Visualisation des services, bases de données et webhooks exposés à l'hallucination de l'étape #{scenario.earliestDivergenceStep}.
                    </p>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                    Zero Data Corruption
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {scenario.blastRadius.map((node) => (
                    <div
                      key={node.id}
                      className="p-5 rounded-2xl bg-[#0B0C10] border border-[#262833] flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-[10px] font-mono text-gray-500 uppercase">{node.type}</span>
                          <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                            node.status === 'PROTECTED'
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              : node.status === 'SAVED_FROM_FAILURE'
                              ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                              : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                          }`}>
                            {node.status}
                          </span>
                        </div>
                        <div className="font-bold text-base text-white mb-2">{node.name}</div>
                        <p className="text-xs text-gray-400 leading-relaxed font-sans">{node.detail}</p>
                      </div>

                      <div className="mt-4 pt-3 border-t border-[#262833] flex items-center justify-between text-[11px] font-mono text-gray-500">
                        <span>Isolation BIFURA</span>
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="p-4 rounded-xl bg-[#14161E] border border-[#262833] flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs">
                  <div className="text-gray-300">
                    Conclusion d'Impact : <strong className="text-white">L'erreur a été neutralisée à l'étape #{scenario.crashStep} avant propagation sur les 4 nœuds aval.</strong>
                  </div>
                  <button
                    onClick={() => setActiveViewTab('safety')}
                    className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-[#FF3E24] text-white font-semibold hover:bg-[#E0341B] transition-colors"
                  >
                    Examiner les règles Safety <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            )}

            {/* View Tab 3: Safety Enforcement Engine */}
            {activeViewTab === 'safety' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <div className="lg:col-span-6 space-y-5">
                  <div>
                    <h3 className="font-display font-bold text-xl text-white mb-2">
                      Safety Gatekeeper // Matrice Tri-State
                    </h3>
                    <p className="text-sm text-gray-400 leading-relaxed">
                      Chaque appel d'outil est évalué contre les politiques de sécurité avant transmission à l'environnement d'exécution.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#0B0C10] border border-[#262833] font-mono text-xs space-y-3">
                    <div className="text-gray-500">// Action interceptée par le proxy :</div>
                    <div className="text-red-400 bg-red-950/30 p-3 rounded-lg border border-red-800/40 break-all font-semibold">
                      {scenario.safetyClassification.actionAttempted}
                    </div>

                    <div className="flex items-center justify-between pt-2">
                      <span className="text-gray-400">Verdict de l'intercepteur :</span>
                      <span className="px-3 py-1 rounded bg-red-500 text-white font-black tracking-widest text-xs">
                        {scenario.safetyClassification.verdict}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Indice de confiance certifié :</span>
                      <span className="text-emerald-400 font-bold">{scenario.safetyClassification.confidence}</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="text-xs font-mono text-gray-400 uppercase tracking-wider">
                      Règles de sécurité enfreintes :
                    </div>
                    {scenario.safetyClassification.triggeredRules.map((r, i) => (
                      <div key={i} className="p-3 rounded-xl bg-[#14161E] border border-red-500/30 flex items-center justify-between text-xs">
                        <div className="flex items-center gap-2">
                          <ShieldAlert className="w-4 h-4 text-red-400 flex-shrink-0" />
                          <span className="text-gray-300 font-mono"><strong className="text-white">{r.code}:</strong> {r.name}</span>
                        </div>
                        <span className="text-[10px] font-mono text-red-400 px-2 py-0.5 rounded bg-red-500/10 font-bold">
                          {r.risk}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Right: Policy Rulebook Matrix */}
                <div className="lg:col-span-6 bg-[#0B0C10] border border-[#262833] rounded-2xl p-6 flex flex-col justify-between font-mono">
                  <div>
                    <div className="text-xs text-gray-400 uppercase tracking-wider mb-4 pb-3 border-b border-[#262833]">
                      Matrice de Triage Temps Réel
                    </div>

                    <div className="space-y-3 text-xs">
                      <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-800/40 flex items-center justify-between">
                        <div>
                          <span className="text-emerald-400 font-bold block">ALLOW</span>
                          <span className="text-gray-400 text-[11px] font-sans">Opérations idemptotentes, lecture seule, scan de métadonnées</span>
                        </div>
                        <span className="text-[10px] text-emerald-400 font-bold">Auto-Pass (&lt; 2ms)</span>
                      </div>

                      <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-800/40 flex items-center justify-between">
                        <div>
                          <span className="text-amber-400 font-bold block">REVIEW</span>
                          <span className="text-gray-400 text-[11px] font-sans">Virements &gt; 500€, modification de tables de test, envoi de mails</span>
                        </div>
                        <span className="text-[10px] text-amber-400 font-bold">Human-in-the-Loop</span>
                      </div>

                      <div className="p-3 rounded-xl bg-red-950/30 border border-red-800/50 flex items-center justify-between">
                        <div>
                          <span className="text-red-400 font-bold block">BLOCK</span>
                          <span className="text-gray-400 text-[11px] font-sans">DROP/TRUNCATE production, fuite PII, boucle d'appels anormale</span>
                        </div>
                        <span className="text-[10px] text-red-400 font-bold">Gel Immédiat</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 mt-6 border-t border-[#262833] flex items-center justify-between text-xs text-gray-400">
                    <span>Zéro friction développeur</span>
                    <button
                      onClick={() => setActiveViewTab('fix')}
                      className="inline-flex items-center gap-1 text-[#FF3E24] hover:underline font-semibold"
                    >
                      Voir le correctif généré <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* View Tab 4: Verified Fix & Deterministic Replay */}
            {activeViewTab === 'fix' && (
              <div className="space-y-6">
                <div>
                  <h3 className="font-display font-bold text-xl text-white">
                    Génération de Patch Ciblé & Replay Déterministe
                  </h3>
                  <p className="text-sm text-gray-400 mt-1">
                    BIFURA synthétise la contrainte exacte à intégrer dans le prompt ou le validateur Pydantic de l'agent, puis certifie sa non-régression.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
                  {/* Before Diff */}
                  <div className="p-5 rounded-2xl bg-[#0B0C10] border border-red-500/30">
                    <div className="flex items-center justify-between text-red-400 pb-3 border-b border-[#262833] mb-3">
                      <span className="font-bold flex items-center gap-1.5">
                        <Flame className="w-4 h-4 text-red-400" />
                        Code / Prompt Vulnérable (Avant)
                      </span>
                      <span className="text-gray-500">Non contraint</span>
                    </div>
                    <pre className="text-red-200/90 whitespace-pre-wrap leading-relaxed overflow-x-auto bg-[#14151B] p-3 rounded-xl border border-red-950">
                      {scenario.verifiedFix.diffBefore}
                    </pre>
                  </div>

                  {/* After Diff */}
                  <div className="p-5 rounded-2xl bg-[#0B0C10] border border-emerald-500/40 shadow-lg shadow-emerald-500/5">
                    <div className="flex items-center justify-between text-emerald-400 pb-3 border-b border-[#262833] mb-3">
                      <span className="font-bold flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                        Patch Certifié BIFURA (Après)
                      </span>
                      <span className="text-cyan-400 font-bold">100% Sûr</span>
                    </div>
                    <pre className="text-emerald-300 whitespace-pre-wrap leading-relaxed overflow-x-auto bg-[#14151B] p-3 rounded-xl border border-emerald-950">
                      {scenario.verifiedFix.diffAfter}
                    </pre>
                  </div>
                </div>

                {/* Replay Test Runner Suite */}
                <div className="p-5 rounded-2xl bg-[#14161E] border border-[#262833] flex flex-col sm:flex-row items-center justify-between gap-4 font-mono text-xs">
                  <div className="flex flex-wrap items-center gap-6">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                      <span className="text-white font-bold">
                        {scenario.verifiedFix.replayStats.testsRun} Tests de Replay Passés
                      </span>
                    </div>
                    <div className="text-gray-400">
                      Régression : <strong className="text-emerald-400">{scenario.verifiedFix.replayStats.regressionsFound}</strong>
                    </div>
                    <div className="text-gray-400">
                      Durée d'exécution : <strong className="text-cyan-400">{scenario.verifiedFix.replayStats.replayDuration}</strong>
                    </div>
                  </div>

                  <button
                    onClick={onOpenDemoModal}
                    className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#FF3E24] text-white font-bold hover:bg-[#E0341B] transition-all shadow-md shadow-[#FF3E24]/20"
                  >
                    <span>Auditer vos propres agents</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

          </div>

        </div>

      </div>
    </section>
  );
}
