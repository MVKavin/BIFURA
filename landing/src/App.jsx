import React, { useState, useEffect } from 'react';
import AppleNav from './components/AppleNav';
import AppleFooter from './components/AppleFooter';
import AppleDemoModal from './components/AppleDemoModal';

import OverviewPage from './pages/OverviewPage';
import IntelligencePage from './pages/IntelligencePage';
import SafetyPage from './pages/SafetyPage';
import ReplayPage from './pages/ReplayPage';
import EnterprisePage from './pages/EnterprisePage';
import BuySpecPage from './pages/BuySpecPage';

export default function App() {
  // Sync page state with hash or default to 'overview'
  const getInitialPage = () => {
    const hash = window.location.hash.replace('#', '');
    const validPages = ['overview', 'intelligence', 'safety', 'replay', 'enterprise', 'buy'];
    return validPages.includes(hash) ? hash : 'overview';
  };

  const [activePage, setActivePage] = useState(getInitialPage);
  const [isDemoModalOpen, setIsDemoModalOpen] = useState(false);

  // Sync state with browser URL hash
  const handlePageChange = (pageId) => {
    setActivePage(pageId);
    window.location.hash = pageId;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    const onHashChange = () => {
      const hash = window.location.hash.replace('#', '');
      const validPages = ['overview', 'intelligence', 'safety', 'replay', 'enterprise', 'buy'];
      if (validPages.includes(hash)) {
        setActivePage(hash);
      }
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  return (
    <div className="min-h-screen bg-[#98FF98] text-[#0c1c13] font-text flex flex-col justify-between selection:bg-[#0c1c13] selection:text-[#98FF98]">
      
      {/* Sleek Frosted Unified Navigation Bar */}
      <AppleNav
        activePage={activePage}
        setActivePage={handlePageChange}
        onOpenDemo={() => setIsDemoModalOpen(true)}
      />

      {/* Main Multi-Page Landing Content */}
      <main className={`flex-1 ${activePage !== 'overview' ? 'pt-[60px]' : ''}`}>
        {activePage === 'overview' && (
          <OverviewPage
            setActivePage={handlePageChange}
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}

        {activePage === 'intelligence' && (
          <IntelligencePage
            setActivePage={handlePageChange}
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}

        {activePage === 'safety' && (
          <SafetyPage
            setActivePage={handlePageChange}
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}

        {activePage === 'replay' && (
          <ReplayPage
            setActivePage={handlePageChange}
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}

        {activePage === 'enterprise' && (
          <EnterprisePage
            setActivePage={handlePageChange}
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}

        {activePage === 'buy' && (
          <BuySpecPage
            onOpenDemo={() => setIsDemoModalOpen(true)}
          />
        )}
      </main>

      {/* Apple Parchment Multi-Column Dense Footer */}
      <AppleFooter setActivePage={handlePageChange} />

      {/* Certified Enterprise Demo Modal */}
      <AppleDemoModal
        isOpen={isDemoModalOpen}
        onClose={() => setIsDemoModalOpen(false)}
      />

    </div>
  );
}
