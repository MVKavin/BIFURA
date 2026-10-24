import React, { useState, useEffect } from 'react';
import { Menu, X, ArrowUpRight } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function AppleNav({ activePage, setActivePage, onOpenDemo }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [navVisible, setNavVisible] = useState(activePage !== 'overview');

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
      if (activePage === 'overview') {
        // Show sleek nav once user scrolls into the revealed portal (approx 1.4 viewport heights)
        const threshold = window.innerHeight * 1.4;
        setNavVisible(window.scrollY > threshold);
      } else {
        setNavVisible(true);
      }
    };
    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [activePage]);

  const pages = [
    { id: 'overview', label: 'Overview' },
    { id: 'intelligence', label: 'Incident Intelligence' },
    { id: 'safety', label: 'Safety Engine' },
    { id: 'replay', label: 'Deterministic Replay' },
    { id: 'enterprise', label: 'Enterprise & Security' },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ease-out ${
        navVisible
          ? 'translate-y-0 opacity-100 pointer-events-auto'
          : '-translate-y-full opacity-0 pointer-events-none'
      }`}
    >
      <div className="h-[60px] px-4 sm:px-8 backdrop-blur-xl bg-[#0c1c13]/90 border-b border-black/10 text-white shadow-lg shadow-black/15 select-none">
        <div className="max-w-6xl mx-auto h-full flex items-center justify-between">
          
          {/* Brand Logo */}
          <button
            type="button"
            onClick={() => {
              setActivePage('overview');
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
            className="flex items-center gap-1.5 group"
            aria-label="BIFURA Home"
          >
            <span className="text-[20px] font-bold tracking-tight text-white font-sans">
              bifura<span className="text-[#98FF98]">.</span>
            </span>
          </button>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-7 text-[13px] font-medium tracking-tight text-[#c2e2cf]">
            {pages.map((p) => {
              const isActive = activePage === p.id;
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setActivePage(p.id)}
                  className={`transition-colors py-1 ${
                    isActive ? 'text-[#98FF98] font-semibold' : 'hover:text-white'
                  }`}
                >
                  {p.label}
                </button>
              );
            })}
          </nav>

          {/* Right Action CTA */}
          <div className="hidden sm:flex items-center gap-4">
            <button
              onClick={() => setActivePage('buy')}
              className="text-[13px] text-[#9bb0a5] hover:text-white transition-colors"
            >
              Enterprise Spec
            </button>
            <a
              href={APP_CONFIG.appUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-[#98FF98] text-[#0c1c13] text-[13px] font-semibold hover:bg-white transition-all shadow-md shadow-black/20 group"
            >
              <span className="w-2 h-2 rounded-full bg-[#047857] animate-pulse" />
              <span>Launch App</span>
              <ArrowUpRight className="w-3.5 h-3.5 text-[#0c1c13] transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 md:hidden text-[#c2d7cd] hover:text-white"
            aria-label="Toggle navigation"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#061811]/95 backdrop-blur-2xl border-b border-emerald-500/20 px-6 py-6 text-white">
          <div className="flex flex-col gap-4">
            {pages.map((p) => (
              <button
                key={p.id}
                onClick={() => {
                  setActivePage(p.id);
                  setMobileMenuOpen(false);
                }}
                className={`text-left text-[16px] py-1 ${
                  activePage === p.id ? 'text-emerald-400 font-semibold' : 'text-[#c2d7cd]'
                }`}
              >
                {p.label}
              </button>
            ))}
            <div className="pt-4 border-t border-emerald-900/50 flex flex-col gap-3">
              <button
                onClick={() => {
                  setActivePage('buy');
                  setMobileMenuOpen(false);
                }}
                className="text-left text-[14px] text-[#9bb0a5]"
              >
                Enterprise Spec
              </button>
              <a
                href={APP_CONFIG.appUrl}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-full bg-[#98FF98] text-[#0c1c13] text-[14px] font-semibold"
              >
                <span className="w-2 h-2 rounded-full bg-[#047857] animate-pulse" />
                <span>Launch App (localhost:8501)</span>
                <ArrowUpRight className="w-4 h-4 text-[#0c1c13]" />
              </a>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}