/* Optimize images in assets/. Run:  npm i sharp  then  node tools/optimize.js
   Resizes any assets/*.png|jpg referenced in index.html to <=1500px and
   recompresses; deletes assets not referenced anywhere in index.html. */
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const PROJ = path.join(__dirname, '..');
const ASSETS = path.join(PROJ, 'assets');
const html = fs.readFileSync(path.join(PROJ, 'index.html'), 'utf8');

const referenced = new Set();
const re = /assets\/([A-Za-z0-9._-]+)/g; let m;
while ((m = re.exec(html))) referenced.add(m[1]);

const MAX = 1500; let before=0, after=0;
(async () => {
  for (const f of fs.readdirSync(ASSETS).filter(f => /\.(png|jpe?g|webp)$/i.test(f))) {
    const fp = path.join(ASSETS, f); const b = fs.statSync(fp).size; before += b;
    if (!referenced.has(f)) { fs.unlinkSync(fp); console.log('DELETED (unused) '+f); continue; }
    const meta = await sharp(fp).metadata();
    let pipe = sharp(fp);
    if (Math.max(meta.width, meta.height) > MAX)
      pipe = pipe.resize({ width: meta.width>=meta.height?MAX:null, height: meta.height>meta.width?MAX:null, withoutEnlargement:true });
    const isMark = /logo|mark/i.test(f);
    const buf = await pipe.png({ compressionLevel:9, effort:9, quality:isMark?100:82, palette:!isMark }).toBuffer();
    if (buf.length < b) fs.writeFileSync(fp, buf);
    after += fs.statSync(fp).size;
    console.log(f.padEnd(22)+' '+(b/1e6).toFixed(2)+'MB -> '+(fs.statSync(fp).size/1e6).toFixed(2)+'MB');
  }
  console.log('TOTAL '+(before/1e6).toFixed(2)+'MB -> '+(after/1e6).toFixed(2)+'MB');
})();
