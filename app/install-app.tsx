'use client';

import { useEffect, useState } from 'react';

type InstallPromptEvent = Event & {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
};

export default function InstallApp() {
  const [prompt, setPrompt] = useState<InstallPromptEvent | null>(null);
  const [installed, setInstalled] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [copied, setCopied] = useState(false);
  const [platform, setPlatform] = useState<'ios' | 'safari' | 'chromium' | 'other'>('other');

  useEffect(() => {
    if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js').catch(() => undefined);

    const agent = navigator.userAgent;
    const ios = /iPad|iPhone|iPod/.test(agent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const chromium = /Chrome|Chromium|Edg\//.test(agent) && !/CriOS/.test(agent);
    const safari = /Safari/.test(agent) && !/Chrome|Chromium|Edg\//.test(agent);
    setPlatform(ios ? 'ios' : chromium ? 'chromium' : safari ? 'safari' : 'other');

    const standalone = window.matchMedia('(display-mode: standalone)').matches ||
      Boolean((navigator as Navigator & { standalone?: boolean }).standalone);
    setInstalled(standalone);

    const onPrompt = (event: Event) => {
      event.preventDefault();
      setPrompt(event as InstallPromptEvent);
    };
    const onInstalled = () => {
      setInstalled(true);
      setPrompt(null);
    };

    window.addEventListener('beforeinstallprompt', onPrompt);
    window.addEventListener('appinstalled', onInstalled);
    return () => {
      window.removeEventListener('beforeinstallprompt', onPrompt);
      window.removeEventListener('appinstalled', onInstalled);
    };
  }, []);

  if (installed) return null;

  async function install() {
    if (!prompt) {
      setShowHelp(true);
      return;
    }
    await prompt.prompt();
    const choice = await prompt.userChoice;
    if (choice.outcome === 'accepted') {
      setPrompt(null);
      setInstalled(true);
    }
  }

  async function copyLink() {
    await navigator.clipboard.writeText('https://nurturehub.boseaishwarya2.chatgpt.site/');
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <div className="install-wrap">
      <button className="install-button" onClick={install} aria-expanded={showHelp}>
        <span aria-hidden="true">↧</span> {prompt ? 'Install app' : 'How to install'}
      </button>
      {showHelp && (
        <div className="install-help" role="dialog" aria-label="Install NurtureHub">
          <button className="install-close" onClick={() => setShowHelp(false)} aria-label="Close">×</button>
          <strong>Install NurtureHub</strong>
          {platform === 'ios' && <p>Open this page in <b>Safari</b>, tap Share, then choose <b>Add to Home Screen</b>.</p>}
          {platform === 'safari' && <p>In Safari, choose <b>File → Add to Dock</b>. On iPhone or iPad, use <b>Share → Add to Home Screen</b>.</p>}
          {platform === 'chromium' && <p>The browser has not offered installation yet. Open the browser menu and choose <b>Install NurtureHub</b> or <b>Apps → Install this site as an app</b>.</p>}
          {platform === 'other' && <p>This preview browser cannot install apps. Copy the link, open it in <b>Chrome, Edge, or Safari</b>, then use that browser’s install option.</p>}
          <button className="install-copy" onClick={copyLink}>{copied ? 'Link copied ✓' : 'Copy app link'}</button>
        </div>
      )}
    </div>
  );
}
