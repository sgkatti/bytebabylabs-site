"use client";

import { motion } from 'framer-motion';
import {
  ArrowRight,
  Atom,
  BrainCircuit,
  Cpu,
  Gauge,
  Globe2,
  Layers3,
  Network,
  Orbit,
  RadioTower,
  Sparkles,
  Waves,
  Zap,
} from 'lucide-react';

const tools = [
  { title: 'OSPF Analyzer', description: 'Inspect LSDB behavior and model routing decisions with clarity.', icon: Network },
  { title: 'PM File Analyzer', description: 'Surface KPIs and anomalies from complex performance data.', icon: Cpu },
  { title: 'OTDR Visualizer', description: 'Trace and explore link health with precision and context.', icon: RadioTower },
  { title: 'Optical Power Budget', description: 'Size margins across terrestrial and submarine deployments.', icon: Gauge },
  { title: 'OSNR Calculator', description: 'Estimate margin and amplifier impact in seconds.', icon: Zap },
  { title: 'Latency Calculator', description: 'Model path delay and propagation impact quickly.', icon: Orbit },
  { title: 'Fiber Loss Calculator', description: 'Quantify loss budgets for route and span design.', icon: Waves },
  { title: 'Submarine Cable Simulator', description: 'Prototype cable behavior and topology interactions.', icon: Globe2 },
];

const knowledgeCards = [
  'Latest Articles',
  'Tutorials',
  'Whitepapers',
  'Standards',
  'Python Scripts',
  'Open Source Projects',
];

const examples = [
  'How does Raman amplification work?',
  'Explain OSNR.',
  'Analyze this PM file.',
  'Why is my pre-FEC increasing?',
];

export default function Home() {
  return (
    <main className="relative overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(94,231,255,0.18),transparent_28%),radial-gradient(circle_at_80%_20%,rgba(108,124,255,0.16),transparent_24%)]" />

      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="flex items-center gap-3 text-sm font-medium tracking-[0.22em] text-slate-200 uppercase">
          <div className="flex h-10 w-10 items-center justify-center rounded-full border border-cyan-400/30 bg-cyan-400/10">
            <Atom className="h-5 w-5 text-cyan-300" />
          </div>
          ByteBabyLabs
        </div>
        <nav className="hidden items-center gap-8 text-sm text-slate-300 md:flex">
          <a href="#tools" className="transition hover:text-white">Tools</a>
          <a href="#labs" className="transition hover:text-white">Labs</a>
          <a href="#learning" className="transition hover:text-white">Learning</a>
          <a href="#about" className="transition hover:text-white">About</a>
        </nav>
      </header>

      <section className="mx-auto grid max-w-7xl gap-12 px-6 pb-24 pt-8 lg:grid-cols-[1.1fr_0.9fr] lg:px-8 lg:pb-32 lg:pt-12">
        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="max-w-2xl">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200">
            <Sparkles className="h-4 w-4" />
            Engineering platform for optical and submarine networks
          </div>
          <h1 className="text-4xl font-semibold leading-[0.95] text-white sm:text-5xl lg:text-7xl">
            Engineering the Future of Networks
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
            AI-powered tools, simulations and engineering resources for optical, telecom and submarine network professionals.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <a href="#tools" className="inline-flex items-center gap-2 rounded-full bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.01]">
              Explore Tools <ArrowRight className="h-4 w-4" />
            </a>
            <a href="#labs" className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:bg-white/10">
              Launch Interactive Lab <Layers3 className="h-4 w-4" />
            </a>
          </div>
          <div className="mt-10 flex flex-wrap gap-6 text-sm text-slate-400">
            <span className="flex items-center gap-2"><BrainCircuit className="h-4 w-4 text-cyan-300" /> AI-assisted engineering</span>
            <span className="flex items-center gap-2"><Globe2 className="h-4 w-4 text-indigo-300" /> Global network modeling</span>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7, delay: 0.1 }} className="relative">
          <div className="absolute inset-0 rounded-[2rem] bg-gradient-to-br from-cyan-400/20 to-indigo-500/20 blur-3xl" />
          <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-slate-950/70 p-6 shadow-glow backdrop-blur-xl">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <div>
                <p className="text-sm text-slate-400">Live network topology</p>
                <p className="text-lg font-semibold text-white">Optical routing canvas</p>
              </div>
              <div className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200">Realtime</div>
            </div>
            <div className="mt-6 rounded-[1.5rem] border border-white/10 bg-[radial-gradient(circle_at_center,rgba(94,231,255,0.15),transparent_55%)] p-6">
              <div className="relative h-72">
                <div className="absolute left-10 top-16 h-24 w-24 rounded-full border border-cyan-400/30 bg-cyan-400/10" />
                <div className="absolute right-12 top-14 h-24 w-24 rounded-full border border-indigo-400/30 bg-indigo-400/10" />
                <div className="absolute bottom-10 left-20 h-24 w-24 rounded-full border border-slate-500/20 bg-slate-500/10" />
                <svg viewBox="0 0 320 220" className="h-full w-full">
                  <path d="M56 96 C110 64, 164 66, 208 96 S286 130, 318 86" stroke="rgba(94,231,255,0.6)" strokeWidth="2.4" fill="none" />
                  <path d="M74 144 C112 116, 156 138, 204 100 S270 116, 292 154" stroke="rgba(108,124,255,0.55)" strokeWidth="2.4" fill="none" />
                  <circle cx="56" cy="96" r="6" fill="#5ee7ff" />
                  <circle cx="208" cy="96" r="6" fill="#5ee7ff" />
                  <circle cx="318" cy="86" r="6" fill="#5ee7ff" />
                  <circle cx="74" cy="144" r="5" fill="#6c7cff" />
                  <circle cx="204" cy="100" r="5" fill="#6c7cff" />
                  <circle cx="292" cy="154" r="5" fill="#6c7cff" />
                </svg>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      <section id="tools" className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Featured tools</p>
            <h2 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">Engineering workflows, simplified.</h2>
          </div>
          <a href="#labs" className="text-sm font-medium text-slate-300 transition hover:text-white">See interactive lab</a>
        </div>
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {tools.map((tool, index) => {
            const Icon = tool.icon;
            return (
              <motion.article key={tool.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.2 }} transition={{ duration: 0.45, delay: index * 0.04 }} className="group rounded-[1.5rem] border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition hover:-translate-y-1 hover:border-cyan-400/30 hover:bg-white/10">
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-white">{tool.title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-400">{tool.description}</p>
                <a href="#" className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-cyan-200 transition group-hover:gap-3">
                  Launch <ArrowRight className="h-4 w-4" />
                </a>
              </motion.article>
            );
          })}
        </div>
      </section>

      <section id="labs" className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="rounded-[2rem] border border-white/10 bg-slate-950/70 p-8 shadow-glow backdrop-blur-xl lg:p-12">
          <div className="max-w-2xl">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Interactive playground</p>
            <h2 className="mt-3 text-3xl font-semibold text-white sm:text-4xl">From raw input to engineered insight.</h2>
            <p className="mt-4 text-lg leading-8 text-slate-300">Paste OSPF LSDB data, upload PM files or sketch a fiber route and let the platform turn it into a guided engineering workflow.</p>
          </div>
          <div className="mt-10 grid gap-6 lg:grid-cols-3">
            {[
              ['Paste OSPF LSDB', 'Visual topology'],
              ['Upload PM file', 'Automatic KPI analysis'],
              ['Draw fiber route', 'Loss estimation'],
            ].map(([title, outcome]) => (
              <div key={title} className="rounded-[1.5rem] border border-white/10 bg-white/5 p-6">
                <p className="text-sm uppercase tracking-[0.28em] text-slate-400">{title}</p>
                <div className="mt-4 h-24 rounded-[1rem] border border-dashed border-cyan-400/20 bg-cyan-400/5" />
                <p className="mt-4 text-sm font-medium text-slate-200">↓ {outcome}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 backdrop-blur-xl">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Submarine systems</p>
            <h2 className="mt-3 text-3xl font-semibold text-white">A global lens for submarine cable planning.</h2>
            <p className="mt-4 text-lg leading-8 text-slate-300">Explore publicly sourced cable references, landing stations and route characteristics while keeping every link grounded in engineering context.</p>
            <div className="mt-8 rounded-[1.5rem] border border-white/10 bg-slate-950/60 p-6">
              <div className="flex items-center justify-between text-sm text-slate-400">
                <span>Reference datasets</span>
                <span>External links</span>
              </div>
              <div className="mt-4 space-y-3 text-sm text-slate-200">
                <a href="https://www.submarinecablemap.com/" className="block rounded-xl border border-white/10 bg-white/5 px-4 py-3 transition hover:bg-white/10">TeleGeography Submarine Cable Map</a>
                <a href="https://www.telecomsbroadband.com/submarine-cables/" className="block rounded-xl border border-white/10 bg-white/5 px-4 py-3 transition hover:bg-white/10">Public cable reference resources</a>
              </div>
            </div>
          </div>

          <div className="rounded-[2rem] border border-white/10 bg-slate-950/70 p-8 shadow-glow backdrop-blur-xl">
            <div className="flex items-center gap-3 text-cyan-200">
              <Globe2 className="h-5 w-5" />
              <span className="text-sm uppercase tracking-[0.3em]">Route intelligence</span>
            </div>
            <div className="mt-6 relative h-72 overflow-hidden rounded-[1.5rem] border border-white/10 bg-[radial-gradient(circle_at_center,rgba(94,231,255,0.16),transparent_48%)] p-6">
              <div className="absolute inset-0 opacity-70">
                <svg viewBox="0 0 320 220" className="h-full w-full">
                  <path d="M42 54 C120 32, 190 36, 232 84 S292 138, 280 172" stroke="rgba(255,255,255,0.24)" strokeWidth="1.5" fill="none" />
                  <path d="M60 126 C120 95, 184 98, 218 132 S290 168, 300 180" stroke="rgba(94,231,255,0.58)" strokeWidth="2" fill="none" />
                  <circle cx="42" cy="54" r="5" fill="#5ee7ff" />
                  <circle cx="232" cy="84" r="5" fill="#5ee7ff" />
                  <circle cx="280" cy="172" r="5" fill="#5ee7ff" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="learning" className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="mb-10">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Knowledge hub</p>
          <h2 className="mt-3 text-3xl font-semibold text-white sm:text-4xl">Build deeper engineering fluency.</h2>
        </div>
        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {knowledgeCards.map((card) => (
            <div key={card} className="rounded-[1.5rem] border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
                <Layers3 className="h-5 w-5" />
              </div>
              <h3 className="mt-5 text-lg font-semibold text-white">{card}</h3>
              <p className="mt-3 text-sm leading-7 text-slate-400">Curated technical references designed for practical network engineering work.</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="rounded-[2rem] border border-white/10 bg-gradient-to-br from-cyan-400/10 to-indigo-500/10 p-8 backdrop-blur-xl lg:p-12">
          <div className="max-w-2xl">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">Ask ByteBaby AI</p>
            <h2 className="mt-3 text-3xl font-semibold text-white sm:text-4xl">A practical engineering assistant for modern networks.</h2>
          </div>
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {examples.map((question) => (
              <div key={question} className="rounded-[1.25rem] border border-white/10 bg-slate-950/60 px-5 py-4 text-sm text-slate-200">
                {question}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="about" className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[0.75fr_1.25fr]">
          <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 backdrop-blur-xl">
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200">About</p>
            <h2 className="mt-3 text-3xl font-semibold text-white">Built by a network engineering veteran.</h2>
          </div>
          <div className="rounded-[2rem] border border-white/10 bg-slate-950/70 p-8 shadow-glow backdrop-blur-xl">
            <p className="text-lg leading-8 text-slate-300">
              With over 23 years of experience designing carrier-scale optical and transport networks across hyperscale and telecom environments, ByteBabyLabs brings together long-haul, metro, DWDM, submarine systems and automation into one premium engineering platform.
            </p>
          </div>
        </div>
      </section>

      <footer className="mx-auto max-w-7xl px-6 pb-20 pt-8 text-sm text-slate-400 lg:px-8">
        <div className="flex flex-wrap items-center justify-between gap-6 border-t border-white/10 pt-8">
          <p>© 2026 ByteBabyLabs</p>
          <div className="flex flex-wrap gap-5">
            {['Tools', 'Labs', 'Learning', 'Documentation', 'GitHub', 'Roadmap', 'Contact'].map((link) => (
              <a key={link} href="#" className="transition hover:text-white">{link}</a>
            ))}
          </div>
        </div>
      </footer>
    </main>
  );
}
