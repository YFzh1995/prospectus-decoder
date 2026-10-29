"""Exercise package completeness, rename migration and update from local releases."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
installer=load('install_skill');packager=load('build_packages')

class InstallPackageTest(unittest.TestCase):
 def test_three_packages_share_core_and_workbuddy_metadata(self):
  with TemporaryDirectory() as tmp:
   files=packager.build(Path(tmp)/'out');self.assertEqual(len(files),4);core=[]
   for f in files[:3]:
    with zipfile.ZipFile(f) as z:
     names=set(z.namelist());prefix='gxg-company-decoder/'
     for n in ['SKILL.md','VERSION','scripts/render_report.py','prompts/reason-business.md','references/platforms.md','templates/report-template.md']:
      self.assertIn(prefix+n,names)
     self.assertNotIn(prefix+'.git/config',names)
     doc=z.read(prefix+'SKILL.md').decode();core.append(doc.split('---',2)[2]);self.assertEqual(doc.splitlines()[1].split(':',1)[1].strip().strip(chr(34)+chr(39)), 'gxg-company-decoder')
     if 'workbuddy' in f.name:
      for field in ['display_name:','display_name_en:','description_zh:','description_en:','version:','author:','examples_zh:']:self.assertIn(field,doc)
   self.assertTrue(all(x==core[0] for x in core))
   with zipfile.ZipFile(files[3]) as z:
    names=set(z.namelist());prefix='gxg-company-decoder/'
    self.assertIn(prefix+'VERSION.md',names);self.assertNotIn(prefix+'VERSION',names);self.assertNotIn(prefix+'.gitignore',names)
    self.assertIn('VERSION.md',z.read(prefix+'scripts/install_skill.py').decode())
 def test_migrate_and_update_preserve_old_material(self):
  with TemporaryDirectory() as tmp:
   base=Path(tmp);target=base/'skills'/'gxg-company-decoder';old=target.with_name('prospectus-decoder');old.mkdir(parents=True)
   (old/'SKILL.md').write_text('---\nname: prospectus-decoder\n---\n');(old/'notes.txt').write_text('user changes')
   (old/'.git').mkdir();(old/'.git/config').write_text('old git')
   backup=base/'backups';r=installer.install(ROOT,target,backup)
   self.assertTrue((target/'SKILL.md').exists());self.assertFalse(old.exists());self.assertEqual(len(r['backups']),1)
   saved=Path(r['backups'][0]);self.assertEqual((saved/'notes.txt').read_text(),'user changes');self.assertEqual((saved/'.git/config').read_text(),'old git')
   (target/'custom.txt').write_text('new edits');r2=installer.install(ROOT,target,backup)
   self.assertEqual((Path(r2['backups'][0])/'custom.txt').read_text(),'new edits')
   self.assertEqual((target/'VERSION').read_text().strip(),'2.2.1')
 def test_unrelated_same_name_is_not_migrated(self):
  with TemporaryDirectory() as tmp:
   base=Path(tmp);target=base/'skills'/'gxg-company-decoder';old=target.with_name('prospectus-decoder');old.mkdir(parents=True)
   (old/'SKILL.md').write_text('---\nname: different-skill\n---\n');r=installer.install(ROOT,target,base/'backups')
   self.assertTrue(old.exists());self.assertEqual(r['backups'],[])
 def test_no_platform_without_choice_and_no_source_target_recursion(self):
  with TemporaryDirectory() as tmp:
   target=ROOT/'subdir'/'gxg-company-decoder'
   with self.assertRaises(ValueError):installer.install(ROOT,target,Path(tmp))
if __name__=='__main__':unittest.main()
