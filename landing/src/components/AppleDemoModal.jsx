import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, CheckCircle2, ShieldCheck, Terminal, ArrowRight, ArrowUpRight } from 'lucide-react';
import { APP_CONFIG } from '../config/appConfig';

export default function AppleDemoModal({ isOpen, onClose }) {
  const [submitted, setSubmitted] = useState(false);
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [framework, setFramework] = useState('LangGraph');

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 select-none">
          {/* Backdrop with 300ms fade */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-md"
          />

          {/* Modal Container with Custom Easing over 400ms */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 16 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
            className="relative z-10 w-full max-w-[560px] bg-[#ffffff] rounded-apple-lg border border-[#e0e0e0] shadow-apple-product-lg p-8 text-[#1d1d1f] font-text"
          >
            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-6 right-6 p-1.5 rounded-full bg-[#f5f5f7] text-[#86868b] hover:text-[#1d1d1f] transition-colors"
              aria-label="Close modal"
            >
              <X className="w-5 h-5" />
            </button>

            {!submitted ? (
              <div>
                <span className="text-[12px] font-mono font-semibold uppercase tracking-wider text-[#FF3E24] mb-2 block">
                  Certified Enterprise Demo
                </span>

                <h3 className="text-[28px] font-semibold tracking-tight text-[#1d1d1f] mb-2">
                  Experience BIFURA.
                </h3>

                <p className="text-[15px] text-[#86868b] leading-relaxed mb-4">
                  Connect with our principal reliability architects for a private telemetry audit of your autonomous agent stack.
                </p>

                {/* Direct Local App Launch Banner */}
                <div className="mb-6 p-3.5 rounded-xl bg-[#0c1c13] text-white flex items-center justify-between">
                  <div>
                    <div className="text-[11px] text-emerald-400 font-mono font-medium flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      <span>Localhost Service Detected</span>
                    </div>
                    <div className="text-[13px] text-white font-medium">Bifura Console on port {APP_CONFIG.port}</div>
                  </div>
                  <a
                    href={APP_CONFIG.appUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={onClose}
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#98FF98] text-[#0c1c13] text-[12px] font-semibold hover:bg-white transition-all shadow"
                  >
                    <span>Launch App</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block text-[13px] font-medium text-[#1d1d1f] mb-1">
                      Work Email
                    </label>
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@company.com"
                      className="w-full px-4 py-3 rounded-apple-sm bg-[#f5f5f7] border border-[#e5e5ea] text-[15px] text-[#1d1d1f] focus:outline-none focus:border-[#FF3E24] focus:bg-white transition-all font-mono"
                    />
                  </div>

                  <div>
                    <label className="block text-[13px] font-medium text-[#1d1d1f] mb-1">
                      Organization / Team
                    </label>
                    <input
                      type="text"
                      required
                      value={company}
                      onChange={(e) => setCompany(e.target.value)}
                      placeholder="e.g. Qonto, Mistral, Scale AI"
                      className="w-full px-4 py-3 rounded-apple-sm bg-[#f5f5f7] border border-[#e5e5ea] text-[15px] text-[#1d1d1f] focus:outline-none focus:border-[#FF3E24] focus:bg-white transition-all"
                    />
                  </div>

                  <div>
                    <label className="block text-[13px] font-medium text-[#1d1d1f] mb-1">
                      Primary Agent Framework
                    </label>
                    <select
                      value={framework}
                      onChange={(e) => setFramework(e.target.value)}
                      className="w-full px-4 py-3 rounded-apple-sm bg-[#f5f5f7] border border-[#e5e5ea] text-[15px] text-[#1d1d1f] focus:outline-none focus:border-[#FF3E24] focus:bg-white transition-all"
                    >
                      <option value="LangGraph">LangGraph / LangChain</option>
                      <option value="CrewAI">CrewAI Multi-Role</option>
                      <option value="AutoGen">Microsoft AutoGen</option>
                      <option value="OpenAI">OpenAI Swarm / Assistants</option>
                      <option value="Custom">Custom In-House Architecture</option>
                    </select>
                  </div>

                  <div className="pt-4">
                    <button
                      type="submit"
                      className="btn-magnetic group w-full py-3.5 rounded-apple-pill bg-[#FF3E24] text-white text-[15px] font-semibold hover:bg-[#E0341B] transition-all flex items-center justify-center gap-2 focus:outline-none"
                    >
                      <span>Schedule Technical Walkthrough</span>
                      <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
                    </button>
                  </div>
                </form>

                <div className="mt-6 pt-4 border-t border-[#f0f0f0] flex items-center justify-between text-[11px] text-[#86868b]">
                  <span>SOC 2 Type II Audited</span>
                  <span>Zero-Retention Cryptographic Scrubbing</span>
                </div>
              </div>
            ) : (
              <div className="text-center py-6">
                <div className="w-12 h-12 rounded-full bg-[#f0faf2] text-[#34c759] flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 className="w-6 h-6" />
                </div>

                <h3 className="text-[24px] font-semibold text-[#1d1d1f] mb-2">
                  Request Received.
                </h3>

                <p className="text-[15px] text-[#86868b] leading-relaxed mb-6">
                  Thank you. Our Site Reliability Engineering team will contact <strong className="text-[#1d1d1f]">{email}</strong> within two business hours to coordinate your trial enclave.
                </p>

                <button
                  onClick={onClose}
                  className="px-6 py-2.5 rounded-apple-pill bg-[#f5f5f7] text-[#1d1d1f] text-[14px] font-medium hover:bg-[#e5e5ea] apple-btn-active transition-all"
                >
                  Return to Site
                </button>
              </div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
