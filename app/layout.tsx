import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'ByteBabyLabs | Engineering the Future of Networks',
  description:
    'AI-powered tools, simulations and engineering resources for optical, telecom and submarine network professionals.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
