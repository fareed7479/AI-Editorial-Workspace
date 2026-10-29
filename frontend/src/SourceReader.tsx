import {useEffect,useRef} from 'react';
import {ArrowUpRight,BookOpen,X} from 'lucide-react';
import type {Source} from './types';
export default function SourceReader({source,onClose}:{source:Source;onClose:()=>void}){
 const dialog=useRef<HTMLDialogElement>(null);
 useEffect(()=>{const element=dialog.current;element?.showModal();const previous=document.body.style.overflow;document.body.style.overflow='hidden';return()=>{element?.close();document.body.style.overflow=previous;};},[]);
 return <dialog ref={dialog} className="source-reader" aria-labelledby="source-reader-title" onCancel={onClose} onClick={event=>{if(event.target===event.currentTarget)onClose();}}><div className="reader-inner"><header><div className="row"><span className="feature-icon"><BookOpen size={19}/></span><span className="eyebrow">SOURCE READER · {source.kind}</span></div><button className="icon-button bordered" autoFocus aria-label="Close source reader" onClick={onClose}><X size={20}/></button></header><h2 id="source-reader-title">{source.title}</h2><div className="reader-meta"><span className="tag amber">{source.reliability}</span><span>{source.content.trim().split(/\s+/).length} words</span>{source.url&&<a href={source.url} target="_blank" rel="noreferrer">Visit original<ArrowUpRight size={14}/></a>}</div><div className="reader-content">{source.content}</div><footer>Stored source text · Claims have not been independently verified.</footer></div></dialog>;
}
