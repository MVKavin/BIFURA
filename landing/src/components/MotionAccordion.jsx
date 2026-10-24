import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus } from 'lucide-react';

export default function MotionAccordion({ items }) {
  const [openIndex, setOpenIndex] = useState(0);

  const toggle = (idx) => {
    setOpenIndex(openIndex === idx ? -1 : idx);
  };

  const defaultItems = [
    {
      q: "How does BIFURA identify the root cause instead of just where the agent crashed?",
      a: "Traditional error trackers capture only the unhandled runtime exception. BIFURA continuously tracks state transitions, prompt token variations, and tool response diffs. By walking the counterfactual causal graph backward, BIFURA isolates the earliest point where intent drifted, often 4 to 8 steps before the fatal crash."
    },
    {
      q: "What is the runtime latency overhead of the Tri-State Safety Engine?",
      a: "Our tri-state policy evaluator (ALLOW / REVIEW / BLOCK) operates in sub-14 milliseconds using dual-redundant edge enclaves. Safe read operations (ALLOW) pass through seamlessly in 1.2ms with zero perceived inference blocking."
    },
    {
      q: "How does Deterministic Replay work without mutating live production APIs?",
      a: "BIFURA freezes model, database, and network payloads as cryptographic fixtures. During patch validation, the agent re-executes strictly against this frozen synthetic environment, verifying that the fix prevents regression without incurring live side effects."
    },
    {
      q: "Which autonomous agent frameworks are supported out of the box?",
      a: "BIFURA provides turnkey SDK wrappers for LangChain, LangGraph, CrewAI, AutoGen, and OpenAI Assistants/Swarm, plus a zero-overhead universal OpenTelemetry hook for custom Python, TypeScript, and Go agent loops."
    },
    {
      q: "Can BIFURA be deployed on-premises or within air-gapped VPCs?",
      a: "Yes. In addition to our Sovereign European Cloud (ISO 27001 & GDPR certified), BIFURA offers full Terraform and Helm deployment modules for private AWS/Azure VPCs and air-gapped on-premise clusters with zero external network egress."
    }
  ];

  const faqList = items || defaultItems;

  return (
    <div className="max-w-[840px] mx-auto space-y-3.5 my-8">
      {faqList.map((item, idx) => {
        const isOpen = openIndex === idx;

        return (
          <div
            key={idx}
            className="rounded-apple-lg border border-[#e5e5ea] bg-[#ffffff] shadow-xs overflow-hidden transition-colors"
          >
            {/* Header Button */}
            <button
              type="button"
              onClick={() => toggle(idx)}
              className="w-full p-6 text-left flex items-center justify-between gap-4 select-none group"
            >
              <span className="text-[17px] sm:text-[19px] font-semibold text-[#1d1d1f] group-hover:text-[#FF3E24] transition-colors">
                {item.q}
              </span>

              {/* Toggle icon rotating 45deg on transform-origin: center */}
              <motion.div
                animate={{ rotate: isOpen ? 45 : 0 }}
                transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
                className="w-8 h-8 rounded-full bg-[#f5f5f7] flex items-center justify-center flex-shrink-0 text-[#1d1d1f] group-hover:bg-[#FF3E24] group-hover:text-white transition-colors origin-center"
              >
                <Plus className="w-4 h-4" />
              </motion.div>
            </button>

            {/* Hardware-accelerated height expansion with AnimatePresence */}
            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  key="content"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                  className="overflow-hidden"
                >
                  <div className="px-6 pb-6 pt-1 text-[15px] sm:text-[16px] text-[#86868b] leading-relaxed border-t border-[#f0f0f0]">
                    {item.a}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        );
      })}
    </div>
  );
}
