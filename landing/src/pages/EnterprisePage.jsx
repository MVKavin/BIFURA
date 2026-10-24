import React from 'react';
import { MotionSlideEntry, MotionStaggerContainer, MotionStaggerItem } from '../components/MotionScrollReveal';
import { ShieldCheck, Lock, Award, Building2, Check, Star, ArrowRight } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function EnterprisePage({ setActivePage, onOpenDemo }) {
  const caseStudies = [
    {
      company: "Qonto Platform",
      role: "FinTech Banking Infrastructure",
      quote: "BIFURA cut our agent incident post-mortems from 3 hours to 4 minutes. Realizing that the hallucination happened at step 2 when the API crashed at step 6 fundamentally changed how our engineering team builds agents.",
      author: "Alexandre Mercier",
      title: "Head of AI Engineering",
    },
    {
      company: "HexaScale AI Labs",
      role: "Enterprise Autonomous Fleet",
      quote: "The ALLOW / REVIEW / BLOCK safety engine allowed us to give write tools to autonomous agents without risking database corruption. It is the missing piece of the production LLM stack.",
      author: "Éléonore de V.",
      title: "VP Reliability & Safety",
    },
    {
      company: "Système U Tech",
      role: "Retail Supply Chain Automation",
      quote: "The French aesthetic rigor combined with an uncompromising real-time tech stack. Deterministic replay verification is the only viable way to manage mission-critical fleets.",
      author: "Marc-Antoine Laurent",
      title: "Principal LLM Architect",
    },
  ];

  return (
    <div className="bg-[#061811] text-white select-none font-sans">
      
      {/* Tile 1: Hero */}
      <section className="bg-[#061811] py-16 sm:py-24 px-4 sm:px-8 text-center border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionStaggerContainer staggerDelay={0.08}>
            <MotionStaggerItem>
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-3 block">
                Enterprise Grade
              </span>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <h1 className="text-[36px] sm:text-[48px] md:text-[56px] font-semibold tracking-[-0.035em] leading-[1.1] text-white mb-4">
                Built for mission-critical fleets.
              </h1>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <p className="text-[17px] sm:text-[20px] text-[#9bb0a5] font-light leading-relaxed max-w-2xl mx-auto mb-8">
                Certified information security, sovereign European cloud hosting, and private VPC deployment for financial and medical institutions.
              </p>
            </MotionStaggerItem>

            <MotionStaggerItem>
              <div className="flex flex-wrap items-center justify-center gap-3.5 mb-14">
                <a
                  href={APP_CONFIG.appUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#154633] border border-emerald-400/30 text-white text-[15px] font-semibold hover:bg-[#1c5a42] transition-all shadow-lg shadow-emerald-950/40"
                >
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Launch Enterprise Console</span>
                  <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
                </a>
                <button
                  onClick={() => setActivePage('buy')}
                  className="px-6 py-3 rounded-full bg-[#0a2318] border border-emerald-900/50 text-[#c2d7cd] text-[15px] font-normal hover:bg-[#0f2e20] hover:text-white transition-all"
                >
                  Configure Deployment
                </button>
              </div>
            </MotionStaggerItem>
          </MotionStaggerContainer>

          {/* 4 Official Compliance Certifications */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 text-left">
            <MotionSlideEntry delay={0.05}>
              <div className="p-6 rounded-2xl bg-[#092218] border border-emerald-800/30 shadow-xl h-full">
                <div className="text-[17px] font-semibold text-white mb-1.5">SOC 2 Type II</div>
                <p className="text-[13px] text-[#9bb0a5] leading-relaxed">Continuous third-party security, availability, and confidentiality audit.</p>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.12}>
              <div className="p-6 rounded-2xl bg-[#092218] border border-emerald-800/30 shadow-xl h-full">
                <div className="text-[17px] font-semibold text-white mb-1.5">ISO 27001:2022</div>
                <p className="text-[13px] text-[#9bb0a5] leading-relaxed">Certified information security management systems with zero data retention.</p>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.19}>
              <div className="p-6 rounded-2xl bg-[#092218] border border-emerald-800/30 shadow-xl h-full">
                <div className="text-[17px] font-semibold text-white mb-1.5">EU AI Act (Art. 14)</div>
                <p className="text-[13px] text-[#9bb0a5] leading-relaxed">Full compliance with high-risk AI human oversight and logging mandates.</p>
              </div>
            </MotionSlideEntry>

            <MotionSlideEntry delay={0.26}>
              <div className="p-6 rounded-2xl bg-[#092218] border border-emerald-800/30 shadow-xl h-full">
                <div className="text-[17px] font-semibold text-white mb-1.5">SLA 99.99%</div>
                <p className="text-[13px] text-[#9bb0a5] leading-relaxed">Enterprise uptime guarantee with 24/7 dedicated site reliability engineering.</p>
              </div>
            </MotionSlideEntry>
          </div>

        </div>
      </section>


      {/* Tile 2: Customer Stories */}
      <section className="bg-[#092218] py-16 sm:py-24 px-4 sm:px-8 border-b border-emerald-900/25">
        <div className="max-w-5xl mx-auto">
          
          <MotionSlideEntry>
            <div className="text-center max-w-2xl mx-auto mb-14">
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
                Case Studies
              </span>
              <h2 className="text-[30px] sm:text-[40px] font-semibold tracking-tight text-white mb-3">
                Proven in high-stakes production.
              </h2>
              <p className="text-[15px] text-[#9bb0a5] leading-relaxed">
                How engineering leads protect their applications from autonomous hallucinations.
              </p>
            </div>
          </MotionSlideEntry>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {caseStudies.map((cs, idx) => (
              <MotionSlideEntry key={idx} delay={idx * 0.1}>
                <div className="p-7 rounded-2xl bg-[#0a241a] border border-emerald-800/30 flex flex-col justify-between h-full">
                  <div>
                    <div className="flex items-center gap-1 text-emerald-400 mb-4">
                      {[...Array(5)].map((_, i) => (
                        <span key={i} className="text-[14px]">★</span>
                      ))}
                    </div>
                    <p className="text-[14px] text-[#c2d7cd] leading-relaxed italic mb-6">
                      « {cs.quote} »
                    </p>
                  </div>

                  <div className="pt-5 border-t border-emerald-900/40">
                    <div className="text-[15px] font-semibold text-white">{cs.author}</div>
                    <div className="text-[12px] text-[#9bb0a5]">{cs.title} • <strong className="text-emerald-400">{cs.company}</strong></div>
                  </div>
                </div>
              </MotionSlideEntry>
            ))}
          </div>

        </div>
      </section>

    </div>
  );
}