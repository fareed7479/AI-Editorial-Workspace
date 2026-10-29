import {useEffect,useRef} from 'react';
import {ArrowRight,FileText,X} from 'lucide-react';
export default function ProjectDialog({title,busy,error,onChange,onCreate,onClose}:{title:string;busy:boolean;error:string;onChange:(title:string)=>void;onCreate:()=>void;onClose:()=>void}){
 const dialog=useRef<HTMLDialogElement>(null);
 useEffect(()=>{dialog.current?.showModal();return()=>dialog.current?.close();},[]);
 return <dialog ref={dialog} className="project-dialog" aria-labelledby="new-project-heading" onCancel={event=>{if(busy)event.preventDefault();else onClose();}}><div className="row between"><span className="feature-icon"><FileText size={20}/></span><button className="icon-button bordered" aria-label="Close new project" disabled={busy} onClick={onClose}><X size={18}/></button></div><div className="eyebrow">A FRESH PAGE</div><h2 id="new-project-heading">What story is on your mind?</h2><p>Give your project a name. You can bring the sources and the perspective next.</p>{error&&<div className="alert error" role="alert">{error}</div>}<form onSubmit={e=>{e.preventDefault();onCreate();}}><label>Project title<input autoFocus required maxLength={160} placeholder="A thought worth following…" value={title} onChange={e=>onChange(e.target.value)}/></label><button className="button full" disabled={busy||!title.trim()}>Create project<ArrowRight size={16}/></button></form></dialog>;
}
