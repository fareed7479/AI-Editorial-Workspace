import {test,expect} from '@playwright/test';

test('workspace login shows errors, opens the library, and signs out',async({page})=>{
 await page.route('**/api/auth/session',route=>route.fulfill({json:{required:true,authenticated:false}}));
 await page.route('**/api/auth/login',route=>{const valid=route.request().postDataJSON().password==='synthetic-owner-password';return route.fulfill({status:valid?200:401,json:valid?{authenticated:true}:{detail:'Incorrect workspace password.'}});});
 await page.goto('/#/workspace');
 await expect(page.getByLabel('Workspace password')).toBeVisible();
 await page.getByLabel('Workspace password').fill('incorrect');await page.getByRole('button',{name:'Open workspace',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('Incorrect workspace password.');
 await page.getByLabel('Workspace password').fill('synthetic-owner-password');await page.getByRole('button',{name:'Open workspace',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Your project library'})).toBeVisible();
 await page.getByRole('button',{name:'Sign out',exact:true}).click();await expect(page.getByLabel('Workspace password')).toBeVisible();
});

test('Gemini errors preserve text and generated newsletters require explicit review',async({page})=>{
 await page.route('**/api/ai/config',route=>route.fulfill({json:{configured:true,model:'controlled-test-model',daily_request_limit:20,max_input_chars:80000,max_output_tokens:8192}}));
 await page.route('**/api/ai/usage',route=>route.fulfill({json:{requests:0,remaining:20,limit:20}}));
 await page.route('**/api/projects/*/ai/jobs',route=>route.fulfill({json:[]}));
 await page.goto('/#/workspace');await page.getByRole('button',{name:'Open sample project',exact:true}).click();
 await expect(page.getByText('Fictional sample loaded.',{exact:false})).toBeVisible();
 await page.getByRole('button',{name:/Writing studio/}).click();
 const original=await page.getByRole('textbox',{name:'Newsletter draft'}).inputValue();
 await page.route('**/api/projects/*/ai/generate',route=>route.fulfill({contentType:'application/x-ndjson',body:JSON.stringify({type:'error',code:'provider_quota',message:'Controlled Gemini quota failure.'})+'\n'}));
 await page.getByRole('button',{name:'Review writing with Gemini'}).click();await expect(page.getByText('Controlled Gemini quota failure.')).toBeVisible();
 await expect(page.getByRole('textbox',{name:'Newsletter draft'})).toHaveValue(original);
 await page.unroute('**/api/projects/*/ai/generate');
 const generated='# Controlled newsletter\n\nA reviewable generated draft.\n\n## Sources\n1. Controlled source';
 await page.route('**/api/projects/*/ai/generate',async route=>{
  const project=(await (await page.request.get(route.request().url().replace('/ai/generate',''))).json());
  const job={id:'controlled-newsletter-id',kind:'newsletter',status:'complete',provider:'gemini',model:'controlled-test-model',created_at:new Date().toISOString(),draft_version:1,usage:{total_token_count:100},error_code:null,result:{text:generated,body_words:320}};
  await route.fulfill({contentType:'application/x-ndjson',body:[{type:'started',job_id:job.id,model:job.model},{type:'progress',characters:123},{type:'complete',job,project}].map(e=>JSON.stringify(e)).join('\n')+'\n'});
  await page.route('**/api/projects/*/ai/jobs/controlled-newsletter-id/apply',route=>route.fulfill({json:{...project,draft:{...project.draft,current:generated,version:2}}}));
 });
 await page.getByRole('button',{name:'Generate newsletter',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Review the generated newsletter'})).toBeVisible();
 await expect(page.getByRole('textbox',{name:'Newsletter draft'})).toHaveValue(original);
 await page.getByRole('button',{name:'Use this draft',exact:true}).click();
 await expect(page.getByRole('textbox',{name:'Newsletter draft'})).toHaveValue(generated);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
