import {test,expect} from '@playwright/test';

test('landing opens the workspace and supports the browser back button',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto('/');
 await expect(page.getByRole('heading',{name:/Find the signal/})).toBeVisible();
 await page.screenshot({path:test.info().outputPath('landing.png'),fullPage:true});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 await page.getByRole('button',{name:'Open workspace',exact:true}).click();
 await expect(page).toHaveURL(/#\/workspace/);
 await expect(page.getByRole('heading',{name:'Your project library'})).toBeVisible();
 await page.goBack();await expect(page.getByRole('heading',{name:/Find the signal/})).toBeVisible();
 expect(errors).toEqual([]);
});

test('library finds projects, changes views, previews saved material and reads full sources',async({page})=>{
 await page.goto('/#/workspace');
 await page.getByRole('button',{name:'Open sample project',exact:true}).click();
 await expect(page.getByText('Fictional sample loaded.',{exact:false})).toBeVisible();
 await page.getByRole('button',{name:'My workspace',exact:true}).click();
 await page.getByRole('textbox',{name:'Search workspace projects'}).fill('Local models: beyond the headline');
 await page.getByRole('button',{name:'3+ sources',exact:false}).click();
 await page.getByRole('button',{name:'List view',exact:true}).click();
 await expect(page.getByRole('button',{name:'List view',exact:true})).toHaveAttribute('aria-pressed','true');
 await page.getByLabel('Sort projects').selectOption('title');
 await page.getByRole('button',{name:'Preview Local models: beyond the headline',exact:true}).first().click();
 const preview=page.getByRole('complementary',{name:'Project preview'});
 await expect(preview.getByRole('heading',{name:'Local models: beyond the headline',exact:true})).toBeVisible();
 await expect(preview).toBeInViewport();
 await preview.getByRole('button',{name:/Sample · Cedar Labs release note/}).click();
 const reader=page.getByRole('dialog',{name:'Sample · Cedar Labs release note'});
 await expect(reader).toBeVisible();await expect(reader.getByText(/Commercial licensing has not yet been clarified/)).toBeVisible();
 await page.keyboard.press('Escape');await expect(reader).not.toBeVisible();
 await preview.getByRole('button',{name:'brief',exact:true}).click();await expect(preview.getByText('Saved research brief',{exact:true})).toBeVisible();
 await preview.getByRole('button',{name:'draft',exact:true}).click();await expect(preview.getByText(/Version 1/)).toBeVisible();
 await page.getByRole('button',{name:'Grid view',exact:true}).click();
 await page.screenshot({path:test.info().outputPath('library.png'),fullPage:true});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
 await preview.getByRole('button',{name:'Open writing studio'}).click();
 await expect(page.getByRole('textbox',{name:'Newsletter draft'})).toHaveValue(/A smaller model/);
 await page.getByRole('button',{name:'Expand workspace',exact:true}).click();
 await expect(page.getByRole('button',{name:'Show sidebar',exact:true})).toBeVisible();
 await page.getByRole('textbox',{name:'Newsletter draft'}).fill('Unsaved thought that must remain.');
 page.once('dialog',dialog=>dialog.dismiss());await page.getByRole('button',{name:'My workspace',exact:true}).click();
 await expect(page.getByRole('textbox',{name:'Newsletter draft'})).toHaveValue('Unsaved thought that must remain.');
});

test('library has useful no-results and reset behavior',async({page})=>{
 await page.goto('/#/workspace');
 await page.getByRole('textbox',{name:'Search workspace projects'}).fill('no-project-matches-this-unique-search');
 await expect(page.getByRole('heading',{name:'No projects in this view.'})).toBeVisible();
 await page.getByRole('button',{name:'Reset search & filters'}).click();
 await expect(page.getByRole('textbox',{name:'Search workspace projects'})).toHaveValue('');
});
