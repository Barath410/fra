import type { Metadata, Viewport } from "next";
import { Inter, Poppins, Noto_Sans_Devanagari } from "next/font/google";
import "./globals.css";
import "mapbox-gl/dist/mapbox-gl.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

const poppins = Poppins({
  variable: "--font-poppins",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  display: "swap",
});

const notoSansDevanagari = Noto_Sans_Devanagari({
  variable: "--font-noto-devanagari",
  subsets: ["devanagari"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "VanAdhikar Drishti — AI-Powered FRA Atlas & DSS",
    template: "%s | VanAdhikar Drishti",
  },
  description:
    "AI-Powered FRA Atlas and WebGIS Decision Support System for Integrated Monitoring of Forest Rights Act Implementation — Ministry of Tribal Affairs, Government of India",
  keywords: ["FRA", "Forest Rights Act", "Tribal Affairs", "WebGIS", "DSS", "Patta"],
  authors: [{ name: "Ministry of Tribal Affairs, Government of India" }],
  creator: "MoTA — NIC",
  publisher: "Ministry of Tribal Affairs",
  robots: { index: false, follow: false }, // Internal government system
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#007BFF",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="hi" className="scroll-smooth">
      <body
        className={`${inter.variable} ${poppins.variable} ${notoSansDevanagari.variable} antialiased bg-white min-h-screen font-sans`}
        style={{ fontFamily: 'var(--font-inter), system-ui, sans-serif' }}
      >
        <a href="#main-content" className="skip-nav">
          Skip to main content
        </a>
        {children}
      </body>
    </html>
  );
}
