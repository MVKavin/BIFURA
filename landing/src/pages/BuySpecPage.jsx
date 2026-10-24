import React, { useState } from 'react';
import { MotionSlideEntry } from '../components/MotionScrollReveal';
import { Check, ShieldCheck, Cpu, Terminal, ArrowRight, Lock } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function BuySpecPage({ onOpenDemo }) {
  const [fleetSize, setFleetSize] = useState('10-50');
  const [deployment, setDeployment] = useState('cloud-eu');

  const fleetOptions = [
    { id: '1-10', label: '1 to 10 Agents', note: 'Early Stage Fleet' },
    { id: '10-50', label: '10 to 50 Agents', note: 'Production Scale' },
    { id: '50+', label: '50+ Agents', note: 'Enterprise Fleet' },
  ];

  const deploymentOptions = [
    { id: 'cloud-eu', label: 'Sovereign EU Cloud', note: 'Paris & Frankfurt' },
    { id: 'aws-vpc', label: 'Dedicated AWS VPC', note: 'Your Cloud Perimeter' },
    { id: 'azure-enclave', label: 'Azure Confidential', note: 'Hardware Enclave' },
    { id: 'air-gapped', label: 'Air-Gapped Enclave', note: 'Zero External Egress' },
  ];

  const specRows = [
    { feature: 'Earliest Divergence Pinpointing', value: 'Included across all tiers' },
    { feature: 'Blast Radius DAG Mapping', value: 'Real-time topological graph' },
    { feature: 'Tri-State Safety Interception (ALLOW/REVIEW/BLOCK)', value: 'Sub-14ms edge evaluation' },
    { feature: 'Deterministic Replay Test Harness', value: 'Frozen snapshot fixtures with CI/CD hooks' },
    { feature: 'Supported Frameworks', value: 'LangGraph, CrewAI, AutoGen, OpenAI Swarm, Custom OpenTelemetry' },
    { feature: 'Regulatory Compliance', value: 'EU AI Act (Art. 14), SOC 2 Type II, ISO 27001:2022' },
    { feature: 'Data Retention Policy', value: 'Zero-retention cryptographic scrubbing' },
    { feature: 'Dedicated Reliability Engineer SLA', value: '2-hour response window, 99.99% uptime guarantee' },
  ];

  return (
    <div className="bg-[#061811] text-white select-none font-sans">
      
      {/* Top Hero Heading */}
      <section className="py-16 sm:py-20 px-4 sm:px-8 text-center border-b border-emerald-900/25 bg-[#061811]">
        <div className="max-w-4xl mx-auto">
          <MotionSlideEntry>
            <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
              Deployment Architecture
            </span>
            <h1 className="text-[36px] sm:text-[48px] font-semibold tracking-[-0.035em] text-white mb-3">
              Deploy BIFURA.
            </h1>
            <p className="text-[17px] sm:text-[20px] text-[#9bb0a5] font-light leading-relaxed">
              Select your fleet scale and deployment architecture.
            </p>
          </MotionSlideEntry>
        </div>
      </section>

      {/* Configurator Section */}
      <section className="py-16 px-4 sm:px-8 bg-[#092218] border-b border-emerald-900/25">
        <div className="max-w-4xl mx-auto space-y-12">
          
          {/* 1. Fleet Scale */}
          <MotionSlideEntry delay={0.05}>
            <div>
              <h2 className="text-[19px] font-semibold text-white mb-3">
                1. Fleet Scale. <span className="text-[#9bb0a5] font-normal text-[15px]">How many critical agents run in production?</span>
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {fleetOptions.map((opt) => {
                  const isSelected = fleetSize === opt.id;
                  return (
                    <button
                      key={opt.id}
                      onClick={() => setFleetSize(opt.id)}
                      className={`p-5 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? 'bg-[#0a241a] border-emerald-400 ring-2 ring-emerald-400/20 shadow-lg shadow-emerald-950/40'
                          : 'bg-[#061811] border-emerald-900/40 hover:border-emerald-700/60'
                      }`}
                    >
                      <div className="text-[16px] font-semibold text-white mb-1">{opt.label}</div>
                      <div className="text-[13px] text-[#9bb0a5]">{opt.note}</div>
                    </button>
                  );
                })}
              </div>
            </div>
          </MotionSlideEntry>

          {/* 2. Deployment Perimeter */}
          <MotionSlideEntry delay={0.12}>
            <div>
              <h2 className="text-[19px] font-semibold text-white mb-3">
                2. Deployment Perimeter. <span className="text-[#9bb0a5] font-normal text-[15px]">Where should telemetry execute?</span>
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {deploymentOptions.map((opt) => {
                  const isSelected = deployment === opt.id;
                  return (
                    <button
                      key={opt.id}
                      onClick={() => setDeployment(opt.id)}
                      className={`p-5 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? 'bg-[#0a241a] border-emerald-400 ring-2 ring-emerald-400/20 shadow-lg shadow-emerald-950/40'
                          : 'bg-[#061811] border-emerald-900/40 hover:border-emerald-700/60'
                      }`}
                    >
                      <div className="text-[16px] font-semibold text-white mb-1">{opt.label}</div>
                      <div className="text-[13px] text-[#9bb0a5]">{opt.note}</div>
                    </button>
                  );
                })}
              </div>
            </div>
          </MotionSlideEntry>

          {/* Configuration Callout */}
          <MotionSlideEntry delay={0.18}>
            <div className="p-6 rounded-2xl bg-[#0a241a] border border-emerald-800/30 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <div className="text-[16px] font-semibold text-white">
                  Ready to initiate trial deployment.
                </div>
                <div className="text-[13px] text-[#9bb0a5]">
                  Selected: {fleetSize} Agents • {deploymentOptions.find(d => d.id === deployment)?.label}
                </div>
              </div>

              <a
                href={APP_CONFIG.appUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#154633] border border-emerald-400/30 text-white text-[15px] font-semibold hover:bg-[#1c5a42] transition-all whitespace-nowrap shadow-lg shadow-emerald-950/40"
              >
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>Launch App for Fleet Setup</span>
                <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
              </a>
            </div>
          </MotionSlideEntry>

        </div>
      </section>

      {/* 3. Deep Architectural Specifications */}
      <section className="py-16 sm:py-20 px-4 sm:px-8 bg-[#061811]">
        <div className="max-w-4xl mx-auto">
          <MotionSlideEntry>
            <div className="text-center mb-12">
              <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-emerald-400 mb-2 block">
                Technical Specifications
              </span>
              <h2 className="text-[28px] sm:text-[36px] font-semibold text-white">
                Platform Capabilities
              </h2>
            </div>
          </MotionSlideEntry>

          <MotionSlideEntry delay={0.1}>
            <div className="rounded-2xl border border-emerald-800/30 bg-[#092218] overflow-hidden shadow-xl">
              <div className="divide-y divide-emerald-900/30">
                {specRows.map((row, idx) => (
                  <div
                    key={idx}
                    className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 hover:bg-emerald-950/20 transition-colors"
                  >
                    <div className="text-[14px] font-medium text-white">{row.feature}</div>
                    <div className="text-[13px] font-mono text-[#9bb0a5] sm:text-right">{row.value}</div>
                  </div>
                ))}
              </div>
            </div>
          </MotionSlideEntry>
        </div>
      </section>

    </div>
  );
}