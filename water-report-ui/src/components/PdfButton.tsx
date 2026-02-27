
"use client";

import { Button } from "@/components/ui/button";

export default function PdfButton() {
  const handlePrint = () => {
    window.print();
  };

  return (
    <Button 
      onClick={handlePrint} 
      // ensures the button doesn't show up IN the PDF!
      className="print:hidden bg-slate-900 hover:bg-slate-800 text-white"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="mr-2 h-4 w-4"
      >
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" x2="12" y1="15" y2="3" />
      </svg>
      Download Report PDF
    </Button>
  );
}