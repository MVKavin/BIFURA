import React from 'react';
import { Shield, Lock, Terminal, Activity, ArrowUpRight } from 'lucide-react';

export default function Footer({ t, lang, setLang }) {
  return (
    <footer className="bg-[#08080C] text-[#9CA3AF] font-sans border-t border-[#262833] pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Main Footer Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-12 pb-16 border-b border-[#262833]">
          
          {/* Brand Info & Mission (Span 4) */}
          <div className="lg:col-span-4 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-[#171922] border border-[#262833] flex items-center justify-center shadow-md">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4h5v4H4V4z" fill="#FFFFFF" />
                  <path d="M6.5 8v5l6 6h7.5v-4h-5.5l-5-5V8" fill="#FF3E24" />
                  <circle cx="19" cy="19" r="2.5" fill="#00D2FF" />
                </svg>
              </div>
              <span className="font-display font-extrabold text-xl text-white tracking-tight">
                BIFURA
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#FF3E24]/10 text-[#FF3E24] border border-[#FF3E24]/30 font-bold">
                INCIDENT INTELLIGENCE
              </span>
            </div>

            <p className="text-sm text-gray-400 leading-relaxed font-sans max-w-sm">
              {t.footer.desc}
            </p>

            {/* Live Infrastructure Status */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#111216] border border-[#262833] text-xs font-mono text-gray-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>{t.footer.status}</span>
            </div>
          </div>

          {/* Links Columns (Span 8) */}
          <div className="lg:col-span-8 grid grid-cols-2 sm:grid-cols-4 gap-8">
            
            {/* Col 1: Produit */}
            <div className="space-y-3 font-mono text-xs">
              <div className="font-display font-bold text-sm text-white uppercase tracking-wider font-sans">
                {t.footer.col1}
              </div>
              <ul className="space-y-2">
                <li><a href="#capabilities" className="hover:text-white transition-colors">Root-Cause Tracing</a></li>
                <li><a href="#capabilities" className="hover:text-white transition-colors">Blast Radius DAG</a></li>
                <li><a href="#safety" className="hover:text-white transition-colors">Safety Engine</a></li>
                <li><a href="#sandbox" className="hover:text-white transition-colors">Deterministic Replay</a></li>
                <li><a href="#workflow" className="hover:text-white transition-colors">SDK OpenTelemetry</a></li>
              </ul>
            </div>

            {/* Col 2: Sécurité & Normes */}
            <div className="space-y-3 font-mono text-xs">
              <div className="font-display font-bold text-sm text-white uppercase tracking-wider font-sans">
                {t.footer.col2}
              </div>
              <ul className="space-y-2">
                <li><a href="#metrics" className="hover:text-white transition-colors">ISO 27001:2022</a></li>
                <li><a href="#metrics" className="hover:text-white transition-colors">SOC 2 Type II</a></li>
                <li><a href="#metrics" className="hover:text-white transition-colors">EU AI Act (Art. 14)</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Rapport de Pénétration</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Politique Zéro Rétention</a></li>
              </ul>
            </div>

            {/* Col 3: Société */}
            <div className="space-y-3 font-mono text-xs">
              <div className="font-display font-bold text-sm text-white uppercase tracking-wider font-sans">
                {t.footer.col3}
              </div>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition-colors">Manifeste & Rigueur</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Études de Cas</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Équipe Fondatrice</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Carrières [Recrutement]</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Presse & Médias</a></li>
              </ul>
            </div>

            {/* Col 4: Développeurs */}
            <div className="space-y-3 font-mono text-xs">
              <div className="font-display font-bold text-sm text-white uppercase tracking-wider font-sans">
                {t.footer.col4}
              </div>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition-colors">Documentation SDK</a></li>
                <li><a href="#" className="hover:text-white transition-colors">GitHub Repository</a></li>
                <li><a href="#" className="hover:text-white transition-colors">LangGraph Adapter</a></li>
                <li><a href="#" className="hover:text-white transition-colors">CrewAI Middleware</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Reference v3</a></li>
              </ul>
            </div>

          </div>

        </div>

        {/* Bottom Bar: Copyright & Location */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-gray-500">
          <div>
            © {new Date().getFullYear()} BIFURA Inc. {t.footer.rights}
          </div>

          <div className="flex items-center gap-4 text-gray-400">
            <span>{t.footer.hq}</span>
            <span>•</span>
            <div className="flex items-center gap-1.5 bg-[#14151B] px-2.5 py-1 rounded border border-[#262833]">
              <button
                type="button"
                onClick={() => setLang('fr')}
                className={`hover:text-white ${lang === 'fr' ? 'text-[#FF3E24] font-bold' : ''}`}
              >
                FR
              </button>
              <span>|</span>
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`hover:text-white ${lang === 'en' ? 'text-[#FF3E24] font-bold' : ''}`}
              >
                EN
              </button>
            </div>
          </div>
        </div>

      </div>
    </footer>
  );
}
