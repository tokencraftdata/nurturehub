import type { Metadata } from 'next';
import './globals.css';
import './events.css';
import './profiles.css';
import './command.css';
import './transparency.css';
import './discover.css';
import './parties.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://nurturehub.boseaishwarya2.chatgpt.site'),
  title: 'NurtureHub — Your family, in one place',
  description: 'Track your child’s diet, activity, and growth in one private family journal.',
  manifest: '/manifest.webmanifest',
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [{ url: '/icons/apple-touch-icon.png', sizes: '180x180', type: 'image/png' }],
  },
  appleWebApp: { capable: true, title: 'NurtureHub', statusBarStyle: 'default' },
  applicationName: 'NurtureHub',
  openGraph: { title: 'NurtureHub — Your family, in one place', description: 'Meals, activities, growth, and schedules—together.', images: ['/og.png'] },
  twitter: { card: 'summary_large_image', title: 'NurtureHub — Your family, in one place', description: 'Meals, activities, growth, and schedules—together.', images: ['/og.png'] },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
