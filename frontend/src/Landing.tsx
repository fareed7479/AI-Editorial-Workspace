import {ArrowDown,ArrowRight,ArrowUpRight,BookOpen,Check,CheckCheck,FileText,FlaskConical,Leaf,MoveRight,ShieldCheck} from 'lucide-react';

type Props={onEnter:()=>void;onDemo:()=>void};
export default function Landing({onEnter,onDemo}:Props){
 return <div className="landing">
  <a className="skip-link" href="#landing-content">Skip to content</a>
  <header className="landing-nav landing-wrap">
   <a className="brand" href="#/" aria-label="Fieldnotes home"><span className="brand-icon"><Leaf size={22}/></span>fieldnotes<span className="brand-period">.</span></a>
   <nav aria-label="Main navigation"><a href="#how-it-works">The process</a><a href="#a-considered-workspace">The workspace</a><button className="button" onClick={onEnter}>Open workspace<ArrowUpRight size={16}/></button></nav>
  </header>
  <main id="landing-content">
   <section className="landing-hero landing-wrap">
    <div className="landing-intro"><div className="eyebrow"><span className="tiny-rule"/>A QUIETER PLACE TO MAKE SOMETHING MATTER</div><h1>Find the signal.<br/>Give it <em>your voice.</em></h1><p>From a collection of sources to a story worth reading. A thoughtful workspace for research, writing, and every revision in between.</p><div className="landing-actions"><button className="button" onClick={onEnter}>Make room for your next story<ArrowRight size={17}/></button><button className="text-button" onClick={onDemo}>Explore a sample<ArrowUpRight size={16}/></button></div><div className="landing-proof"><span><Check size={13}/>Sources stay connected</span><span><Check size={13}/>Originals stay intact</span></div></div>
    <div className="editorial-collage" aria-label="Illustration of source notes becoming an editorial draft">
     <span className="collage-orbit orbit-one"/><span className="collage-orbit orbit-two"/>
     <div className="collage-label">A FEW GOOD SOURCES.<br/>ONE CLEAR POINT OF VIEW.</div>
     <div className="collage-source source-back"><span>FIELD NOTE / 01</span><BookOpen size={19}/><h3>Start with<br/>the evidence.</h3><i/><i/><i/></div>
     <div className="collage-sheet"><div className="sheet-masthead"><Leaf size={15}/><span>THE WEEK, CONSIDERED</span><span>VOL. 01</span></div><div className="sheet-category">RESEARCH → PERSPECTIVE</div><h2>A better story<br/>starts with a<br/><em>closer look.</em></h2><p>Collect the context. Find your angle.<br/>Leave the noise behind.</p><div className="sheet-lines"><i/><i/><i/></div><div className="sheet-foot"><span>YOUR NEXT DRAFT</span><ArrowUpRight size={19}/></div></div>
     <div className="collage-note"><span className="handwritten">Keep the nuance.</span><span className="small">The best edit still sounds like you.</span></div><div className="collage-stamp"><CheckCheck size={18}/><span>YOUR VOICE.<br/>YOUR FINAL CALL.</span></div><span className="collage-asterisk" aria-hidden="true">✳</span>
    </div>
    <a className="landing-scroll" href="#how-it-works">A little structure goes a long way<ArrowDown size={14}/></a>
   </section>
   <div className="principle-band"><div className="landing-wrap"><span>BUILT FOR THOUGHTFUL WORK</span><p>Evidence before opinion.</p><span className="band-star">✳</span><p>Clarity without losing context.</p><span className="band-star">✳</span><p>Your judgment at every step.</p></div></div>
   <section className="landing-process landing-wrap" id="how-it-works"><div className="landing-section-head"><div><div className="eyebrow">FROM SCATTERED TO CONSIDERED</div><h2>One story.<br/>A little more perspective.</h2></div><p>A simple rhythm for the work that matters.<br/>Gather well, write clearly, and keep the important details close.</p></div><div className="process-columns">{[
    {n:'01',icon:<BookOpen size={22}/>,title:'Gather what matters.',text:'Bring articles, reports, and field notes together. Keep the original text and source link within reach.'},
    {n:'02',icon:<FlaskConical size={22}/>,title:'Connect the dots.',text:'Review a source-linked brief. Separate reported claims from editorial interpretation, then find an angle.'},
    {n:'03',icon:<FileText size={22}/>,title:'Make it sound like you.',text:'Shape your draft with specific writing checks. Review each suggestion and compare every saved revision.'}
   ].map(step=><article key={step.n}><div className="row between"><span className="process-icon">{step.icon}</span><span className="process-number">{step.n}</span></div><h3>{step.title}</h3><p>{step.text}</p></article>)}</div></section>
   <section className="landing-workspace" id="a-considered-workspace"><div className="landing-wrap workspace-showcase"><div className="showcase-visual" aria-label="Illustrative workspace layout"><div className="mini-top"><span><Leaf size={13}/>fieldnotes.</span><span>YOUR EDITORIAL DESK</span></div><div className="mini-body"><div className="mini-sidebar"><i/><i/><i/><i/></div><div className="mini-main"><span className="eyebrow">MY WORKSPACE</span><h3>A home for every<br/>unfinished thought.</h3><div className="mini-cards"><div><BookOpen size={17}/><span>Research notes</span><i/></div><div><FileText size={17}/><span>The next draft</span><i/></div></div><div className="mini-review"><Check size={13}/><span>The original stays with you.</span></div></div></div><span className="showcase-caption">ILLUSTRATIVE PREVIEW · YOUR PROJECTS APPEAR IN THE WORKSPACE</span></div><div className="showcase-copy"><div className="eyebrow">EVERYTHING IN ITS PLACE</div><h2>Less searching.<br/>More space to think.</h2><p>Your projects deserve more than a crowded sidebar. Browse your library, preview the material, and pick up exactly where your thinking left off.</p><ul><li><Check size={15}/>Grid and list views for your projects</li><li><Check size={15}/>Sources, brief, and draft in one preview</li><li><Check size={15}/>Full source reading and a wider editing space</li></ul><button className="text-button" onClick={onEnter}>Step inside the workspace<MoveRight size={19}/></button></div></div></section>
   <section className="landing-close landing-wrap"><div className="eyebrow">A BLANK PAGE. A BETTER START.</div><h2>Your next story<br/>has a place <em>to begin.</em></h2><button className="button" onClick={onEnter}>Open your workspace<ArrowUpRight size={17}/></button><p><ShieldCheck size={14}/>You decide what makes the final draft.</p></section>
  </main>
  <footer className="landing-footer landing-wrap"><a className="brand" href="#/"><Leaf size={20}/>fieldnotes.</a><span>An editorial workspace for thoughtful work.</span><span>RESEARCH. WRITE. RECONSIDER.</span></footer>
 </div>;
}
