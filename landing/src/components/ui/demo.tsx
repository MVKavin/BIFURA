"use client";

import React, { useEffect, useState, type ReactNode } from "react";
import GlyphPortal from "@/components/ui/glyph-portal";
import { APP_CONFIG } from "@/config/appConfig";

export type BifuraPortalProps = {
  children?: ReactNode;
  onOpenDemo?: () => void;
};

const family = '"Glyph Portal Jakarta", "Impact", "Arial Black", sans-serif';
let fontLoad: Promise<void> | undefined;

export default function BifuraPortal({ children, onOpenDemo }: BifuraPortalProps) {
  const [face, setFace] = useState<string | null>(null);

  useEffect(() => {
    let settled = false;
    const finish = (value: string) => {
      if (!settled) {
        settled = true;
        setFace(value);
      }
    };

    // Preload Glyph Portal Jakarta face for accurate stem rasterization
    fontLoad ??= new FontFace(
      "Glyph Portal Jakarta",
      'url("https://cdn.21st.dev/assets/mirror/15/153fc85b70298beeb1d61a5f723331649e7f23bb77302a66e61cb3e2fbdb5e79.woff2")',
      { weight: "400 700 900" }
    )
      .load()
      .then((font) => {
        document.fonts.add(font);
      });

    const timeout = window.setTimeout(() => finish('"Impact", "Arial Black", sans-serif'), 1200);
    void fontLoad.then(
      () => finish(family),
      () => finish('"Impact", "Arial Black", sans-serif')
    );

    return () => {
      settled = true;
      clearTimeout(timeout);
    };
  }, []);

  return (
    <div
      data-bifura-entry-wrapper
      className="w-full relative select-none"
      style={{
        background: "#ffffff",
        fontFamily: face ?? '"Impact", "Arial Black", sans-serif',
      }}
    >
      <style>{`
        [data-bifura-entry-wrapper] [data-gp-caption]{
          inset: calc(var(--gp-word-bottom, 50%) + 64px) 24px auto;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 12px;
        }
        [data-bifura-entry-wrapper] [data-gp-hint]{ display: none; }
        [data-bifura-entry-wrapper] [data-gp-enter]{
          min-height: 44px;
          padding: 0 28px;
          display: inline-flex;
          align-items: center;
          gap: 10px;
          background: #123325;
          border: 1px solid rgba(18, 51, 37, 0.2);
          border-radius: 9999px;
          color: #ffffff;
          font-size: 14px;
          font-weight: 600;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
          box-shadow: 0 8px 24px -4px rgba(18, 51, 37, 0.35);
          transition: background .2s, transform .2s, box-shadow .2s;
          text-decoration: none;
        }
        [data-bifura-entry-wrapper] [data-gp-enter]:hover{
          background: #174230;
          transform: scale(1.02);
          box-shadow: 0 12px 28px -4px rgba(18, 51, 37, 0.45);
        }
        [data-bifura-entry-wrapper] [data-gp-enter]:focus-visible{
          outline: 2px solid #123325;
          outline-offset: 4px;
        }
        [data-bifura-entry-wrapper] [data-gp-touch-picker]{
          display: none !important;
        }

        /* Opening Frame Clean Editorial Hierarchy - 1:1 match with Image 1 */
        [data-bifura-header]{
          position: absolute;
          inset: clamp(24px, 4.5cqw, 44px) clamp(24px, 5cqw, 64px) auto;
          display: flex;
          align-items: center;
          justify-content: space-between;
          pointer-events: auto;
        }
        [data-bifura-logo]{
          font-size: 24px;
          font-weight: 700;
          letter-spacing: -0.04em;
          color: #111827;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif;
        }
        [data-bifura-category]{
          font-size: 14px;
          font-weight: 400;
          color: #6b7280;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
        }
        [data-bifura-eyebrow]{
          position: absolute;
          inset: auto 24px calc(100% - var(--gp-word-top, 35%) + 24px);
          margin: 0;
          text-align: center;
          font-size: 15px;
          font-weight: 400;
          color: #6b7280;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
          letter-spacing: 0.02em;
        }
        [data-bifura-support]{
          position: absolute;
          inset: calc(var(--gp-word-bottom, 50%) + 18px) 24px auto;
          margin: 0;
          text-align: center;
          font-size: clamp(17px, 1.8cqw, 21px);
          font-weight: 400;
          color: #4b5563;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif;
        }
        [data-bifura-scroll]{
          position: absolute;
          inset: calc(var(--gp-word-bottom, 50%) + 124px) 24px auto;
          text-align: center;
          color: #9ca3af;
          font-size: 12px;
          font-weight: 500;
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
          pointer-events: none;
        }
        [data-bifura-entry-wrapper] [data-gp-content]{
          font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
          color: #0c1c13;
          padding: 0 !important;
        }
      `}</style>

      {face ? (
        <GlyphPortal
          word="BIFURA"
          focusChar="I"
          fontFamily={face}
          fontWeight={900}
          scrollLength={2.6}
          interactive={true}
          annotations={false}
          enterLabel="Step inside"
          style={{
            fontFamily: face,
            "--gp-paper": "#ffffff",
            "--gp-ink": "#0b3b2a",
            "--gp-field": "#0b3b2a",
            "--gp-foreground": "#ffffff",
          }}
          background={
            <div
              style={{
                position: "absolute",
                inset: 0,
                transform: "scale(var(--gp-field-scale, 1))",
                background: `
                  radial-gradient(circle at 18% 8%, rgba(68,125,98,.78), transparent 34%),
                  radial-gradient(circle at 82% 20%, rgba(251,251,250,.14), transparent 28%),
                  radial-gradient(circle at 48% 78%, rgba(9,48,35,.55), transparent 44%),
                  linear-gradient(135deg, #071f16 0%, #0b3b2a 45%, #051a12 100%)
                `,
              }}
            />
          }
          front={
            <>
              {/* Clean minimal top bar: bifura. | AI incident intelligence | Launch App ↗ */}
              <div data-bifura-header>
                <span data-bifura-logo>bifura.</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <span data-bifura-category>AI incident intelligence</span>
                  <a
                    href={APP_CONFIG.appUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '6px',
                      padding: '5px 14px',
                      borderRadius: '9999px',
                      backgroundColor: '#0c1c13',
                      color: '#98FF98',
                      fontSize: '13px',
                      fontWeight: 600,
                      textDecoration: 'none',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.12)',
                      fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif',
                    }}
                  >
                    <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#047857' }} />
                    <span>Launch App</span>
                    <span>↗</span>
                  </a>
                </div>
              </div>

              {/* Positioned safely ABOVE the word: A different perspective starts here. */}
              <p data-bifura-eyebrow>A different perspective starts here.</p>

              {/* Positioned safely BELOW the word: Follow your curiosity. */}
              <p data-bifura-support>Follow your curiosity.</p>

              {/* Positioned below the button: Scroll for a closer look ↓ */}
              <div data-bifura-scroll>Scroll for a closer look ↓</div>
            </>
          }
        >
          {/* Once the camera zooms through the letter into the green field, the website content is revealed! */}
          {children}
        </GlyphPortal>
      ) : (
        <div
          role="status"
          style={{
            height: "100vh",
            display: "grid",
            placeItems: "center",
            background: "#ffffff",
            color: "#6b7280",
            fontSize: 14,
            fontFamily: "-apple-system, sans-serif",
          }}
        >
          Loading BIFURA…
        </div>
      )}
    </div>
  );
}