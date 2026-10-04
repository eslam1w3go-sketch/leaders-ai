import os, re, sqlite3
from pathlib import Path
import fitz
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
BASE=Path(__file__).parent
PDF=BASE/"materials"/"تكنولوجيا المعلومات 2027.pdf"
if not PDF.exists(): raise SystemExit("PDF not found")
key=os.getenv("OPENAI_API_KEY")
if not key: raise SystemExit("Set OPENAI_API_KEY in .env")
client=OpenAI(api_key=key)
DB=BASE/"data"/"leaders.db"
DB.parent.mkdir(exist_ok=True)
c=sqlite3.connect(DB)
c.executescript("""
CREATE TABLE IF NOT EXISTS materials(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,subject TEXT,filename TEXT,vector_store_id TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS pages(id INTEGER PRIMARY KEY AUTOINCREMENT,material_id INTEGER,page_no INTEGER,text TEXT,image_path TEXT);
CREATE TABLE IF NOT EXISTS chats(id INTEGER PRIMARY KEY AUTOINCREMENT,material_id INTEGER,session_id TEXT,role TEXT,message TEXT,created_at TEXT);
""")
old=c.execute("SELECT id FROM materials WHERE filename=?",(PDF.name,)).fetchone()
if old:
    print("Material already installed."); raise SystemExit
vs=client.vector_stores.create(name="LEADERS AI - تكنولوجيا المعلومات 2027")
with open(PDF,"rb") as f: up=client.files.create(file=f,purpose="assistants")
client.vector_stores.files.create(vector_store_id=vs.id,file_id=up.id)
c.execute("INSERT INTO materials(name,subject,filename,vector_store_id,created_at) VALUES(?,?,?,?,datetime('now'))",
          ("تكنولوجيا المعلومات 2027","تكنولوجيا المعلومات",PDF.name,vs.id))
mid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
doc=fitz.open(PDF)
for i,p in enumerate(doc,1):
    c.execute("INSERT INTO pages(material_id,page_no,text,image_path) VALUES(?,?,?,?)",
              (mid,i,re.sub(r"\s+"," ",p.get_text()).strip(),""))
c.commit(); c.close()
print("Installed: تكنولوجيا المعلومات 2027")
