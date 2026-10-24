import React, { useState } from 'react';
import { ArrowRight, Sparkles, CheckCircle2, ShieldCheck, Mail, Send, Terminal } from 'lucide-react';

export default function ClosingCTA({ t, onOpenDemoModal }) {
  const [emailInput, setEmailInput] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailInput.trim()) {
      setSubmitted(true);
    }
  };

  return (
    <section className="py-24 md:py-32 bg-[#FFFFFF] text-[#111827] relative border-b border-[#E5E7EB] overflow-hidden bg-grid-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Massive High-Impact Closing Container */}
        <div className="rounded-3xl bg-[#0B0C10] border border-[#262833] text-white p-8 sm:p-12 md:p-16 relative overflow-hidden shadow-2xl">
          {/* Subtle Ambient Radial Glow */}
          <div className="absolute top-0 right-0 w-[450px] h-[450px] bg-gradient-to-br from-[#FF3E24]/20 via-[#1D4ED8]/10 to-transparent blur-[120px] pointer-events-none" />

          <div className="max-w-3xl relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#171922] border border-[#262833] text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-6">
              <span>{t.cta.tag}</span>
            </div>

            <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-white leading-[1.1] mb-6">
              {t.cta.title}
            </h2>

            <p className="text-lg sm:text-xl text-gray-400 leading-relaxed mb-10">
              {t.cta.desc}
            </p>

            {/* Quick Email Audit Box or Demo Trigger */}
            {submitted ? (
              <div className="p-6 rounded-2xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-300 font-mono text-sm flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
                <div>
                  <div className="font-bold text-white">Demande d'audit transmise avec succès.</div>
                  <div className="text-xs text-gray-300 mt-0.5">
                    Notre équipe d'ingénierie fiabilité vous contactera sous 2 heures avec vos accès sandbox.
                  </div>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-xl mb-6">
                <input
                  type="email"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                  placeholder="votre.nom@entreprise.com"
                  required
                  className="flex-1 px-5 py-4 rounded-full bg-[#171922] border border-[#262833] text-white placeholder-gray-500 text-sm focus:outline-none focus:border-[#FF3E24] font-mono"
                />
                <button
                  type="submit"
                  className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-[#FF3E24] text-white font-bold text-sm hover:bg-[#E0341B] transition-all duration-200 shadow-xl shadow-[#FF3E24]/20 hover:shadow-[#FF3E24]/40 hover:-translate-y-0.5 whitespace-nowrap"
                >
                  <span>Démarrer l'Audit</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            )}

            <div className="flex flex-wrap items-center gap-6 text-xs font-mono text-gray-400 pt-2">
              <span className="flex items-center gap-1.5 text-gray-300">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                {t.cta.statsPill}
              </span>
              <span className="flex items-center gap-1.5 text-gray-300">
                <ShieldCheck className="w-4 h-4 text-[#00D2FF]" />
                Aucun stockage de clés API tiers
              </span>
              <span className="flex items-center gap-1.5 text-gray-300">
                <Terminal className="w-4 h-4 text-[#FF3E24]" />
                SLA 99.99% Enterprise
              </span>
            </div>
          </div>

          {/* Right Floating Badge Card */}
          <div className="mt-12 md:mt-0 md:absolute md:bottom-12 md:right-12 max-w-xs p-6 rounded-2xl bg-[#14161E] border border-[#262833] font-mono text-xs shadow-xl hidden lg:block">
            <div className="text-[#FF3E24] font-bold uppercase mb-1">
              {t.cta.consultingTitle}
            </div>
            <p className="text-gray-400 leading-relaxed font-sans mb-3">
              {t.cta.consultingDesc}
            </p>
            <button
              onClick={onOpenDemoModal}
              className="text-white hover:text-[#FF3E24] font-bold underline flex items-center gap-1"
            >
              Prendre rendez-vous avec un ingénieur <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

      </div>
    </section>
  );
}
