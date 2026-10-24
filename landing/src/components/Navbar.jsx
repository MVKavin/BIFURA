import React, { useState, useEffect } from 'react';
import { ShieldCheck, ChevronRight, Menu, X, Terminal, Cpu } from 'lucide-react';

export default function Navbar({ lang, setLang, t, onOpenDemoModal }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { label: t.nav.traceRoot, href: '#capabilities' },
    { label: t.nav.blastRadius, href: '#capabilities' },
    { label: t.nav.safetyEngine, href: '#safety' },
    { label: t.nav.workflow, href: '#workflow' },
    { label: t.nav.sandbox, href: '#sandbox' },
    { label: t.nav.proof, href: '#metrics' },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[#0B0C10]/90 backdrop-blur-md border-b border-[#262833] shadow-2xl py-3.5'
          : 'bg-transparent border-b border-[#262833]/50 py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          
          {/* Brand Logo & Editorial Wordmark */}
          <a href="#" className="flex items-center gap-3.5 group">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-[#1C1E27] to-[#111216] border border-[#262833] group-hover:border-[#FF3E24]/60 transition-all duration-300 shadow-md">
              {/* Bifura Geometric Split Icon */}
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" className="transition-transform duration-300 group-hover:scale-105">
                <path d="M4 4h5v4H4V4z" fill="#FFFFFF" />
                <path d="M6.5 8v5l6 6h7.5v-4h-5.5l-5-5V8" fill="#FF3E24" />
                <circle cx="19" cy="19" r="2.5" fill="#00D2FF" />
              </svg>
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-display font-extrabold text-xl tracking-tight text-white group-hover:text-white transition-colors">
                  BIFURA
                </span>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider bg-[#FF3E24]/10 text-[#FF3E24] border border-[#FF3E24]/30">
                  AI INCIDENT OS
                </span>
              </div>
              <span className="text-[10px] tracking-widest text-[#9CA3AF] uppercase font-mono hidden sm:block">
                ROOT CAUSE & SAFETY INTELLIGENCE
              </span>
            </div>
          </a>

          {/* Desktop Navigation Menu */}
          <nav className="hidden lg:flex items-center gap-7">
            {navLinks.map((item, idx) => (
              <a
                key={idx}
                href={item.href}
                className="text-sm font-medium text-[#9CA3AF] hover:text-white transition-colors relative group py-1"
              >
                {item.label}
                <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-[#FF3E24] transition-all duration-300 group-hover:w-full" />
              </a>
            ))}
          </nav>

          {/* Right Utilities: Lang Switcher & Pill CTA */}
          <div className="hidden sm:flex items-center gap-4">
            {/* Minimal Language Switcher */}
            <div className="flex items-center bg-[#171922] border border-[#262833] rounded-full p-1 text-xs font-mono">
              <button
                type="button"
                onClick={() => setLang('fr')}
                className={`px-2.5 py-1 rounded-full transition-all ${
                  lang === 'fr'
                    ? 'bg-[#FF3E24] text-white font-bold shadow-sm'
                    : 'text-[#9CA3AF] hover:text-white'
                }`}
              >
                FR
              </button>
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`px-2.5 py-1 rounded-full transition-all ${
                  lang === 'en'
                    ? 'bg-[#FF3E24] text-white font-bold shadow-sm'
                    : 'text-[#9CA3AF] hover:text-white'
                }`}
              >
                EN
              </button>
            </div>

            {/* Primary High-Contrast Pill CTA */}
            <button
              onClick={onOpenDemoModal}
              className="group relative inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#FF3E24] text-white text-sm font-semibold hover:bg-[#E0341B] transition-all duration-200 shadow-lg shadow-[#FF3E24]/20 hover:shadow-[#FF3E24]/40 hover:-translate-y-0.5 active:translate-y-0"
            >
              <span>{t.nav.bookDemo}</span>
              <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center gap-3 lg:hidden">
            <div className="flex items-center bg-[#171922] border border-[#262833] rounded-full p-0.5 text-xs font-mono">
              <button
                type="button"
                onClick={() => setLang('fr')}
                className={`px-2 py-0.5 rounded-full ${lang === 'fr' ? 'bg-[#FF3E24] text-white font-bold' : 'text-[#9CA3AF]'}`}
              >
                FR
              </button>
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`px-2 py-0.5 rounded-full ${lang === 'en' ? 'bg-[#FF3E24] text-white font-bold' : 'text-[#9CA3AF]'}`}
              >
                EN
              </button>
            </div>
            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl bg-[#171922] border border-[#262833] text-gray-300 hover:text-white"
              aria-label="Toggle Navigation"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

        </div>
      </div>

      {/* Mobile Slide-down Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-[#0B0C10] border-b border-[#262833] px-6 py-6 space-y-4">
          <div className="flex flex-col space-y-3">
            {navLinks.map((item, idx) => (
              <a
                key={idx}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className="text-base font-medium text-gray-300 hover:text-[#FF3E24] transition-colors py-1"
              >
                {item.label}
              </a>
            ))}
          </div>
          <div className="pt-4 border-t border-[#262833]">
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenDemoModal();
              }}
              className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-[#FF3E24] text-white font-semibold shadow-lg shadow-[#FF3E24]/20"
            >
              <span>{t.nav.bookDemo}</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
