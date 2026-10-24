/**
 * Global Configuration for BIFURA Platform Integration
 * Points to the local application (Streamlit on localhost:8501) by default,
 * and supports custom VITE_BIFURA_APP_URL for production deployments.
 */
export const APP_CONFIG = {
  appName: 'BIFURA',
  appUrl: (typeof import.meta !== 'undefined' && import.meta.env?.VITE_BIFURA_APP_URL) || 'http://localhost:8501',
  port: 8501,
  tagline: 'One mistake. Many consequences. One verified fix.',
  status: 'Online',
};

/**
 * Utility to safely launch the application in a new browser tab
 */
export const launchApp = (path = '') => {
  const baseUrl = APP_CONFIG.appUrl.replace(/\/+$/, '');
  const target = path ? `${baseUrl}/${path.replace(/^\/+/, '')}` : baseUrl;
  window.open(target, '_blank', 'noopener,noreferrer');
};
