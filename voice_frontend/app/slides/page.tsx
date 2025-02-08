import { Slides } from "@/components/Slides";
import Reveal from "reveal.js";
import "reveal.js/dist/reveal.css";
import "reveal.js/dist/theme/black.css"; // "black" theme is just an example

export interface PageProps {
  searchParams: {
    instructions?: string;
  };
}

export const revalidate = 0;

export default async function Page({ searchParams }: PageProps) {
  const instructions = searchParams.instructions || "Presentation on how to build AI Agents";

  const response = await fetch("http://localhost:8000/slides", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ instructions }),
    cache: "no-store"
  });

  const html = await response.json();
  console.log(html);

  //   const html = "<section><h1>Heading</h1><p>Body</p></section>";

  return <Slides slides={html?.response} />;
}
