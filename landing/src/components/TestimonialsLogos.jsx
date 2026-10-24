import React from 'react';
import { Quote, Star, Building2, CheckCircle2 } from 'lucide-react';

export default function TestimonialsLogos({ t, onOpenDemoModal }) {
  const enterpriseLogos = [
    { name: "Mistral AI Partner", tag: "Enterprise LLM" },
    { name: "Anthropic Ecosystem", tag: "Claude Model Safety" },
    { name: "LangChain Verified", tag: "LangGraph Integration" },
    { name: "Cohere Enterprise", tag: "Rerank & Embeddings" },
    { name: "Scale AI Certified", tag: "Dataset Benchmark" },
    { name: "Datadog Partner", tag: "APM Telemetry" },
  ];

  return (
    <section className="py-24 md:py-32 bg-[#FFFFFF] text-[#111827] relative border-b border-[#E5E7EB] overflow-hidden bg-grid-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Enterprise Logos Header */}
        <div className="text-center max-w-3xl mx-auto mb-14">
          <p className="text-xs font-mono font-bold uppercase tracking-widest text-[#6B7280]">
            INTEROPÉRABLE AVEC LES STANDARDS DE L'INDUSTRIE
          </p>
          <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-6 items-center">
            {enterpriseLogos.map((logo, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#111827] transition-all duration-300 text-center group cursor-default"
              >
                <div className="font-display font-extrabold text-sm text-[#374151] group-hover:text-[#111827] transition-colors">
                  {logo.name}
                </div>
                <div className="text-[10px] font-mono text-[#9CA3AF] mt-0.5">
                  {logo.tag}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Section Header */}
        <div className="max-w-3xl mb-16 md:mb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FF3E24]/10 border border-[#FF3E24]/20 text-xs font-mono font-bold tracking-widest uppercase text-[#FF3E24] mb-4">
            <span>{t.testimonials.tag}</span>
          </div>
          <h2 className="font-display font-extrabold text-3xl sm:text-5xl md:text-6xl tracking-tight text-[#111827] leading-[1.1]">
            {t.testimonials.title}
          </h2>
          <p className="mt-5 text-lg sm:text-xl text-[#4B5563] leading-relaxed">
            {t.testimonials.subtitle}
          </p>
        </div>

        {/* 3-Column Editorial Quotes */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {t.testimonials.quotes.map((q, idx) => (
            <div
              key={idx}
              className="rounded-3xl bg-[#F7F8FA] border border-[#E5E7EB] hover:border-[#FF3E24]/50 p-8 flex flex-col justify-between transition-all duration-300 hover:shadow-xl hover:-translate-y-1 group"
            >
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className="w-10 h-10 rounded-2xl bg-white border border-[#E5E7EB] flex items-center justify-center text-[#FF3E24] shadow-sm">
                    <Quote className="w-5 h-5" />
                  </div>
                  <div className="flex items-center gap-1 text-amber-400">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    ))}
                  </div>
                </div>

                <p className="text-base text-[#1F2937] leading-relaxed italic mb-8 font-serif">
                  « {q.quote} »
                </p>
              </div>

              <div className="pt-6 border-t border-[#E5E7EB] flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#111827] to-[#374151] text-white flex items-center justify-center font-display font-bold text-sm shadow-md">
                  {q.author.split(' ').map(n => n[0]).join('')}
                </div>
                <div>
                  <div className="font-display font-bold text-base text-[#111827]">{q.author}</div>
                  <div className="text-xs text-[#6B7280] font-sans">{q.role} • <strong className="text-[#111827]">{q.company}</strong></div>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}
