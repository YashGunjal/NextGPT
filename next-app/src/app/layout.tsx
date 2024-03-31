import "@/styles/globals.css";
import { ClerkProvider } from '@clerk/nextjs'

import { Inter } from "next/font/google";

import { TRPCReactProvider } from "@/trpc/react";
import Navbar from "./_components/navbar";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata = {
  title: "NextGPT",
  description: "create RAG for effective information retrieval",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`font-sans ${inter.variable}`}>
      <ClerkProvider>
        <TRPCReactProvider>
          <Navbar />
          {children}</TRPCReactProvider>
      </ClerkProvider>
      </body>
    </html>
  );
}



