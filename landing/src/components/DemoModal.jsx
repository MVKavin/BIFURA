import React, { useState } from 'react';
import { X, CheckCircle2, ShieldCheck, Terminal, ArrowRight, Copy, Check } from 'lucide-react';

export default function DemoModal({ isOpen, onClose, lang }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    company: '',
    framework: 'LangGraph',
    painPoint: 'root_cause',
    fleetSize: '10-50',
  });
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopy = (code) => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const codeSnippet = `pip install bifura-sdk
export BIFURA_API_KEY="bf_live_${Math.random().toString(36).substring(2, 10)}"

# In your agent entrypoint:
from bifura import BifuraTraceInterceptor

tracer = BifuraTraceInterceptor(
    project_id="prod-fleet-01",
    safety_mode="ACTIVE_ENFORCE"  # ALLOW, REVIEW, BLOCK
)
agent = tracer.wrap(my_agent_loop)`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-2xl bg-[#0E0F14] border border-[#262833] rounded-3xl p-6 sm:p-8 shadow-2xl text-white font-sans overflow-hidden">
        
        {/* Subtle Ambient Glow */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-[#FF3E24]/10 blur-[80px] pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full bg-[#171922] border border-[#262833] text-gray-400 hover:text-white transition-colors"
          aria-label="Fermer"
        >
          <X className="w-5 h-5" />
        </button>

        {step === 1 ? (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="px-2.5 py-1 rounded-full bg-[#FF3E24]/10 border border-[#FF3E24]/30 text-[10px] font-mono font-bold uppercase text-[#FF3E24]">
                {lang === 'fr' ? 'ACCÈS AUDIT PRIORITAIRE' : 'PRIORITY AUDIT ACCESS'}
              </span>
              <span className="text-xs font-mono text-gray-400">SOC 2 TYPE II VERIFIED</span>
            </div>

            <h3 className="font-display font-extrabold text-2xl sm:text-3xl text-white mb-2">
              {lang === 'fr' 
                ? 'Démarrez l’audit certifié de vos agents IA'
                : 'Start Your Certified AI Agent Audit'}
            </h3>
            <p className="text-sm text-gray-400 mb-6 font-normal">
              {lang === 'fr'
                ? 'Configurez votre environnement d’investigation d’incident en moins de 2 minutes.'
                : 'Configure your incident intelligence environment in less than 2 minutes.'}
            </p>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                setStep(2);
              }}
              className="space-y-4"
            >
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-gray-300 uppercase mb-1.5">
                    {lang === 'fr' ? 'Email Professionnel' : 'Work Email'}
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="ingenieur@entreprise.com"
                    className="w-full px-4 py-3 rounded-xl bg-[#171922] border border-[#262833] text-white text-sm focus:outline-none focus:border-[#FF3E24] font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-mono text-gray-300 uppercase mb-1.5">
                    {lang === 'fr' ? 'Entreprise / Organisation' : 'Company'}
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                    placeholder="Qonto, Mistral, Scale AI..."
                    className="w-full px-4 py-3 rounded-xl bg-[#171922] border border-[#262833] text-white text-sm focus:outline-none focus:border-[#FF3E24]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono text-gray-300 uppercase mb-1.5">
                    {lang === 'fr' ? 'Framework Agent Utilisé' : 'Agent Framework'}
                  </label>
                  <select
                    value={formData.framework}
                    onChange={(e) => setFormData({ ...formData, framework: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-[#171922] border border-[#262833] text-white text-sm focus:outline-none focus:border-[#FF3E24]"
                  >
                    <option value="LangGraph">LangGraph / LangChain</option>
                    <option value="CrewAI">CrewAI Multi-Agent</option>
                    <option value="AutoGen">Microsoft AutoGen</option>
                    <option value="OpenAI">OpenAI Assistants / Swarm</option>
                    <option value="Custom">Custom In-House Architecture</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-mono text-gray-300 uppercase mb-1.5">
                    {lang === 'fr' ? 'Taille de la flotte en prod' : 'Production Fleet Size'}
                  </label>
                  <select
                    value={formData.fleetSize}
                    onChange={(e) => setFormData({ ...formData, fleetSize: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-[#171922] border border-[#262833] text-white text-sm focus:outline-none focus:border-[#FF3E24]"
                  >
                    <option value="1-10">1 à 10 agents critiques</option>
                    <option value="10-50">10 à 50 agents critiques</option>
                    <option value="50+">+50 agents en production</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono text-gray-300 uppercase mb-1.5">
                  {lang === 'fr' ? 'Priorité Immédiate' : 'Primary Priority'}
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {[
                    { id: 'root_cause', label: lang === 'fr' ? 'Identifier la cause racine' : 'Pinpoint root cause' },
                    { id: 'safety', label: lang === 'fr' ? 'Bloquer les actions à risque (Safety)' : 'Block unsafe tool calls' },
                    { id: 'blast', label: lang === 'fr' ? 'Graphe de Blast Radius' : 'Blast radius mapping' },
                    { id: 'replay', label: lang === 'fr' ? 'Replay & Non-régression CI' : 'Deterministic CI replay' },
                  ].map((p) => (
                    <button
                      key={p.id}
                      type="button"
                      onClick={() => setFormData({ ...formData, painPoint: p.id })}
                      className={`p-2.5 rounded-xl text-left border transition-all ${
                        formData.painPoint === p.id
                          ? 'bg-[#FF3E24]/15 border-[#FF3E24] text-white font-bold'
                          : 'bg-[#171922] border-[#262833] text-gray-400'
                      }`}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full py-4 rounded-full bg-[#FF3E24] text-white font-bold text-sm hover:bg-[#E0341B] transition-all flex items-center justify-center gap-2 shadow-lg shadow-[#FF3E24]/20"
                >
                  <span>{lang === 'fr' ? 'Générer mes identifiants de télémétrie' : 'Generate Telemetry Credentials'}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
              <span className="font-display font-bold text-2xl text-white">
                {lang === 'fr' ? 'Clé de Télémétrie Générée' : 'Telemetry Key Generated'}
              </span>
            </div>

            <p className="text-sm text-gray-300">
              {lang === 'fr'
                ? `Félicitations. Vos identifiants sandbox pour ${formData.company || 'votre équipe'} ont été initialisés avec succès.`
                : `Success. Your sandbox credentials for ${formData.company || 'your team'} have been initialized.`}
            </p>

            <div className="relative rounded-2xl bg-[#0B0C10] border border-[#262833] p-4 font-mono text-xs text-gray-200">
              <div className="flex items-center justify-between pb-3 border-b border-[#262833] mb-3 text-gray-400">
                <span className="flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-[#00D2FF]" />
                  SDK Quickstart ({formData.framework})
                </span>
                <button
                  type="button"
                  onClick={() => handleCopy(codeSnippet)}
                  className="inline-flex items-center gap-1 text-[#FF3E24] hover:text-[#FF8573]"
                >
                  {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? 'Copié !' : 'Copier'}</span>
                </button>
              </div>

              <pre className="overflow-x-auto whitespace-pre leading-relaxed text-emerald-300">
                {codeSnippet}
              </pre>
            </div>

            <div className="p-4 rounded-xl bg-blue-950/20 border border-blue-500/30 text-xs text-cyan-300 flex items-center justify-between">
              <span>Un ingénieur dédié vous assistera sur Slack / Teams pour le premier audit.</span>
              <ShieldCheck className="w-4 h-4 text-cyan-400 flex-shrink-0" />
            </div>

            <button
              type="button"
              onClick={onClose}
              className="w-full py-3.5 rounded-full bg-[#171922] border border-[#262833] text-white font-semibold text-sm hover:bg-[#1E202B] transition-colors"
            >
              {lang === 'fr' ? 'Fermer et retourner au site' : 'Close and return to site'}
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
