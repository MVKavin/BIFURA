import React from 'react';
import { ArrowUpRight } from 'lucide-react';

export default function SlideDeckCard({ 
  tag, 
  title, 
  subtitle, 
  stat, 
  statLabel, 
  imageSrc, 
  renderVisual,
  onClick 
}) {
  return (
    <div
      onClick={onClick}
      className="slide-deck-card relative rounded-apple-lg border border-[#e5e5ea] bg-[#ffffff] overflow-hidden cursor-pointer select-none flex flex-col justify-between group"
    >
      {/* 16:9 Aspect Ratio Visual Container */}
      <div className="relative aspect-video w-full overflow-hidden bg-[#0B0C10] border-b border-[#e5e5ea]">
        {/* Inner Graphic or Visual with smooth 600ms scale(1.04) */}
        <div className="slide-deck-image absolute inset-0 w-full h-full flex items-center justify-center p-6">
          {renderVisual ? (
            renderVisual
          ) : (
            <div className="w-full h-full rounded-apple-sm bg-[#171922] border border-[#262833] p-4 font-mono text-[11px] text-gray-300 flex flex-col justify-between">
              <div className="flex items-center justify-between text-[#86868b]">
                <span>TRACE MOCKUP 16:9</span>
                <span className="text-[#FF3E24]">VERITAS CERTIFIED</span>
              </div>
              <div className="text-white text-[13px] font-sans font-semibold">
                {title}
              </div>
              <div className="text-[#34c759] text-[10px]">
                Active Telemetry Node
              </div>
            </div>
          )}
        </div>

        {/* Deepening Gradient Overlay (rgba(0,0,0,0) -> rgba(0,0,0,0.3)) */}
        <div className="slide-deck-overlay absolute inset-0 pointer-events-none" />

        {/* Floating Badge Tag (shifts color & glows with #FF3E24 border on hover) */}
        <div className="absolute top-4 left-4 z-10">
          <span className="slide-deck-badge px-3 py-1 rounded-apple-pill bg-white/95 dark:bg-[#14151B]/95 text-[#1d1d1f] text-[11px] font-mono font-bold tracking-wider uppercase border border-[#e5e5ea] shadow-sm">
            {tag}
          </span>
        </div>

        {/* Hover Arrow Indicator */}
        <div className="absolute top-4 right-4 z-10 w-8 h-8 rounded-full bg-white/90 flex items-center justify-center text-[#1d1d1f] opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-sm">
          <ArrowUpRight className="w-4 h-4 text-[#FF3E24]" />
        </div>
      </div>

      {/* Card Content Footer */}
      <div className="p-6">
        <h4 className="text-[19px] font-semibold text-[#1d1d1f] mb-1.5 group-hover:text-[#FF3E24] transition-colors">
          {title}
        </h4>
        <p className="text-[14px] text-[#86868b] leading-relaxed mb-4">
          {subtitle}
        </p>

        {stat && (
          <div className="pt-4 border-t border-[#f0f0f0] flex items-baseline gap-2">
            <span className="text-[28px] font-bold text-[#FF3E24] tracking-tight">
              {stat}
            </span>
            <span className="text-[12px] text-[#86868b]">{statLabel}</span>
          </div>
        )}
      </div>
    </div>
  );
}
