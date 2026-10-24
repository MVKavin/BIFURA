import React from 'react';

export default function MotionMarquee() {
  const credentials = [
    "Depuis 2024",
    "ISO 27001:2022 Certifié",
    "SOC 2 Type II",
    "99.98% Précision Root-Cause",
    "+14 000 000 Traces Analysées",
    "0 Régression Non Détectée",
    "Safety Guardrails (ALLOW / REVIEW / BLOCK)",
    "Latence d'Interception < 14ms",
    "Replay Déterministe Certifié",
    "Compatible LangGraph, CrewAI & AutoGen",
    "Note 5.0/5 Équipes d'Ingénierie IA",
  ];

  // Duplicate for continuous seamless 30s loop
  const list = [...credentials, ...credentials];

  return (
    <div className="relative border-y border-[#262833] bg-[#0E0F14] py-3.5 overflow-hidden select-none">
      {/* Edge gradient masks */}
      <div className="absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-[#0E0F14] to-transparent z-10 pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-[#0E0F14] to-transparent z-10 pointer-events-none" />

      <div className="animate-marquee whitespace-nowrap">
        {list.map((item, idx) => (
          <div key={idx} className="flex items-center gap-6 mx-5">
            <div className="flex items-center gap-2 font-mono text-[13px] tracking-wide text-[#a1a1a6] hover:text-white transition-colors cursor-default">
              <span className="w-1.5 h-1.5 rounded-full bg-[#FF3E24] shadow-[0_0_8px_#FF3E24]" />
              <span className="font-medium text-white">{item}</span>
            </div>
            <span className="text-[#FF3E24]/60 font-bold">•</span>
          </div>
        ))}
      </div>
    </div>
  );
}
