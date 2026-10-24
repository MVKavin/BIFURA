import React, { useState } from 'react';
import { Plus, Minus, HelpCircle } from 'lucide-react';

export default function FAQSection({ t }) {
  const [openIndex, setOpenIndex] = useState(0);

  const toggleItem = (idx) => {
    setOpenIndex(openIndex === idx ? -1 : idx);
  };

  return (
    <section className="py-24 md:py-32 bg-[#0B0C10] text-white relative overflow-hidden bg-grid-pattern border-b border-[#262833]">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#171922] border border-[#262833] text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-4">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>{t.faq.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-white leading-[1.1]">
            {t.faq.title}
          </h2>
          <p className="mt-4 text-lg text-gray-400 leading-relaxed">
            {t.faq.subtitle}
          </p>
        </div>

        {/* Clean Accordion Items */}
        <div className="space-y-4">
          {t.faq.items.map((item, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div
                key={idx}
                className={`rounded-2xl border transition-all duration-300 overflow-hidden ${
                  isOpen
                    ? 'bg-[#171922] border-[#FF3E24]/60 shadow-xl shadow-[#FF3E24]/5'
                    : 'bg-[#111216] border-[#262833] hover:border-gray-600'
                }`}
              >
                <button
                  type="button"
                  onClick={() => toggleItem(idx)}
                  className="w-full p-6 text-left flex items-center justify-between gap-4 select-none"
                  aria-expanded={isOpen}
                >
                  <span className="font-display font-bold text-lg sm:text-xl text-white pr-4">
                    {item.q}
                  </span>
                  <div className={`w-8 h-8 rounded-full border flex items-center justify-center flex-shrink-0 transition-all ${
                    isOpen
                      ? 'bg-[#FF3E24] border-[#FF3E24] text-white'
                      : 'bg-[#1C1E27] border-[#262833] text-gray-400'
                  }`}>
                    {isOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
                  </div>
                </button>

                {isOpen && (
                  <div className="px-6 pb-6 pt-1 text-sm sm:text-base text-gray-300 font-normal leading-relaxed border-t border-[#262833]/50">
                    {item.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
