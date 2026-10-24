import React from 'react';
import { Shield, Sparkles, CheckCircle, Award, Cpu, Lock } from 'lucide-react';

export default function TrustMarquee({ items }) {
  // Duplicate array for seamless infinite marquee loop
  const marqueeList = [...items, ...items];

  return (
    <div className="relative border-y border-[#262833] bg-[#111216] py-4 overflow-hidden select-none">
      {/* Edge gradient masks */}
      <div className="absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-[#111216] to-transparent z-10 pointer-events-none" />
      <div className="absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-[#111216] to-transparent z-10 pointer-events-none" />

      <div className="flex animate-marquee hover:[animation-play-state:paused] whitespace-nowrap">
        {marqueeList.map((text, idx) => (
          <div key={idx} className="flex items-center gap-6 mx-4">
            <div className="flex items-center gap-2.5 font-mono text-sm tracking-wide text-gray-300 hover:text-white transition-colors cursor-default">
              <span className="w-2 h-2 rounded-full bg-[#FF3E24] shadow-[0_0_8px_#FF3E24]" />
              <span className="font-semibold text-white">{text}</span>
            </div>
            <span className="text-[#FF3E24]/60 font-bold">•</span>
          </div>
        ))}
      </div>
    </div>
  );
}
