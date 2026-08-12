const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file:///home/claude/work/apunte.html', {waitUntil: 'load'});
  await p.emulateMedia({media: 'print'});
  await p.pdf({
    path: '/home/claude/work/apunte.pdf', format: 'A4', printBackground: true,
    margin: {top: '17mm', bottom: '18mm', left: '16mm', right: '16mm'},
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8pt;color:#898781;' +
      'font-family:system-ui,sans-serif;padding:0 16mm;display:flex;' +
      'justify-content:space-between"><span>Perceptrón simple · Inteligencia Computacional · FICH–UNL</span>' +
      '<span class="pageNumber"></span></div>'
  });
  await b.close();
  console.log('PDF ok');
})();
