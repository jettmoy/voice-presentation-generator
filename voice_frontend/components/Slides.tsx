"use client";

import Reveal from "reveal.js";
import { useEffect, useRef } from "react";
import Script from "next/script";

export function Slides({ slides }: { slides: string }) {
  const deckDivRef = useRef<HTMLDivElement>(null); // reference to deck container div
  const deckRef = useRef<Reveal.Api | null>(null); // reference to deck reveal instance

  useEffect(() => {
    // Prevents double initialization in strict mode
    if (deckRef.current) return;

    deckRef.current = new Reveal(deckDivRef.current!, {
      transition: "slide",
      // other config options
      //   plugins: [RevealLoadContent],
      autoSlide: 2
    });

    deckRef.current.initialize().then(() => {
      // good place for event handlers and plugin setups
    });

    return () => {
      try {
        if (deckRef.current) {
          deckRef.current.destroy();
          deckRef.current = null;
        }
      } catch (e) {
        console.warn("Reveal.js destroy call failed.");
      }
    };
  }, []);

  return (
    <>
      {/* <Script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/loadcontent/plugin.js"></Script> */}

      <div className="reveal" ref={deckDivRef}>
        <div className="slides" dangerouslySetInnerHTML={{ __html: slides }} />
      </div>
    </>
  );
}
