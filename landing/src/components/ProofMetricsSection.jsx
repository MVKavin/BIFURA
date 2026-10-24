import React from 'react';
import { ShieldCheck, Award, Lock, Star, CheckCircle, FileCheck, ArrowUpRight } from 'lucide-react';

export default function ProofMetricsSection({ t, onOpenDemoModal }) {
  return (
    <section id="metrics" className="py-24 md:py-32 bg-[#F7F8FA] text-[#111827] relative border-b border-[#E5E7EB] overflow-hidden bg-grid-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="max-w-3xl mb-16 md:mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#1D4ED8]/10 border border-[#1D4ED8]/20 text-xs font-mono font-bold tracking-widest uppercase text-[#1D4ED8] mb-4">
            <ShieldCheck className="w-4 h-4 text-[#1D4ED8]" />
            <span>{t.metrics.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-[#111827] leading-[1.1]">
            {t.metrics.title}
          </h2>
          <p className="mt-5 text-lg sm:text-xl text-[#4B5563] leading-relaxed">
            {t.metrics.subtitle}
          </p>
        </div>

        {/* 4-Column High-Impact Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {t.metrics.items.map((m, idx) => (
            <div
              key={idx}
              className="rounded-3xl bg-white border border-[#E5E7EB] hover:border-[#FF3E24]/50 p-8 flex flex-col justify-between transition-all duration-300 hover:shadow-xl hover:-translate-y-1 group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-mono uppercase font-bold tracking-wider px-2.5 py-1 rounded-full bg-[#F7F8FA] border border-[#E5E7EB] text-[#4B5563]">
                    {m.badge}
                  </span>
                  <span className="w-2 h-2 rounded-full bg-[#FF3E24] opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>

                <div className="flex items-baseline gap-2 mb-3">
                  <span className="font-display font-black text-5xl sm:text-6xl text-[#111827] tracking-tight group-hover:text-[#FF3E24] transition-colors">
                    {m.num}
                  </span>
                  <span className="font-mono text-sm font-bold text-[#6B7280] uppercase">
                    {m.unit}
                  </span>
                </div>
              </div>

              <p className="text-sm text-[#4B5563] leading-relaxed pt-4 border-t border-[#F3F4F6]">
                {m.label}
              </p>
            </div>
          ))}
        </div>

        {/* Official Certifications & Compliance Ribbon */}
        <div className="rounded-3xl bg-[#111216] border border-[#262833] text-white p-8 md:p-10 shadow-2xl">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-8 border-b border-[#262833]">
            <div>
              <div className="flex items-center gap-2 text-xs font-mono text-[#00D2FF] uppercase font-bold mb-1">
                <Lock className="w-3.5 h-3.5" />
                <span>Audits & Agréments Officiels</span>
              </div>
              <h3 className="font-display font-bold text-2xl text-white">
                Certification de sécurité et de reproductibilité algorithmique
              </h3>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1 text-amber-400">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 fill-amber-400 text-amber-400" />
                ))}
              </div>
              <span className="font-mono text-xs text-gray-300 font-bold">5.0 / 5 Note Développeurs</span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 pt-8">
            {t.metrics.certifications.map((cert, idx) => (
              <div key={idx} className="flex items-start gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-[#171922] border border-[#262833] flex items-center justify-center flex-shrink-0 text-[#00D2FF]">
                  <FileCheck className="w-5 h-5" />
                </div>
                <div>
                  <div className="font-display font-bold text-base text-white">{cert.title}</div>
                  <div className="text-xs text-gray-400 leading-snug mt-0.5">{cert.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
