const env = (import.meta as ImportMeta & {env:{VITE_API_URL?:string;PROD:boolean}}).env;
export const apiBase = env.VITE_API_URL ?? (env.PROD ? '' : 'http://127.0.0.1:8000');
export function apiError(detail:unknown):string{
 if(typeof detail==='string')return detail;
 if(detail&&typeof detail==='object'&&'message' in detail)return String(detail.message);
 return 'Please check the field lengths and required values.';
}
export async function api<T>(path:string, method='GET', body?:unknown):Promise<T>{
 const response=await fetch(apiBase+'/api'+path,{method,credentials:'include',headers:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});
 if(!response.ok){const error=await response.json().catch(()=>({detail:'The server could not complete this request.'}));throw new Error(apiError(error.detail));}
 return response.json();
}
export function exportUrl(id:string){return apiBase+'/api/projects/'+id+'/export';}
