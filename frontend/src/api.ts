const base = (import.meta as ImportMeta & {env:Record<string,string>}).env.VITE_API_URL || 'http://127.0.0.1:8000';
export async function api<T>(path:string, method='GET', body?:unknown):Promise<T>{
  const response=await fetch(base+'/api'+path,{method,headers:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});
  if(!response.ok){const error=await response.json().catch(()=>({detail:'The server could not complete this request.'}));throw new Error(typeof error.detail==='string'?error.detail:'Please check field lengths and required values.');}
  return response.json();
}
export function exportUrl(id:string){return base+'/api/projects/'+id+'/export';}
