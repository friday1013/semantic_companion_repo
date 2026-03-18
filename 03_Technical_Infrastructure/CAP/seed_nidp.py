#!/usr/bin/env python3
"""Seed a single framework JSON file into CAP. Bypasses C8 batch-seed issue."""
import asyncio, json, sys
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

FILE = Path(__file__).parent.parent / 'scripts/data/frameworks/nidp_v1.0.json'
DB_URL = 'postgresql+asyncpg://cap_user:testpassword@127.0.0.1:5432/cap'

async def seed():
    payload = json.loads(FILE.read_text())
    engine = create_async_engine(DB_URL)
    async with engine.begin() as conn:
        await conn.execute(
            text("INSERT INTO frameworks (code, title, vendor) VALUES (:code, :title, :vendor) "
                 "ON CONFLICT (code) DO UPDATE SET title=EXCLUDED.title, vendor=EXCLUDED.vendor"),
            {'code': payload['framework'], 'title': payload['title'], 'vendor': payload.get('vendor')}
        )
        for ctrl in payload.get('controls', []):
            await conn.execute(
                text("INSERT INTO controls (id, framework_code, code, title, text, meta_json) "
                     "VALUES (gen_random_uuid(), :fc, :code, :title, :text, :meta) "
                     "ON CONFLICT (framework_code, code) DO UPDATE "
                     "SET title=EXCLUDED.title, text=EXCLUDED.text, meta_json=EXCLUDED.meta_json"),
                {'fc': payload['framework'], 'code': ctrl['code'],
                 'title': ctrl['title'], 'text': ctrl['text'],
                 'meta': json.dumps(ctrl.get('meta', {}))}
            )
    await engine.dispose()
    print(f"Seeded {payload['framework']}: {len(payload['controls'])} controls")

asyncio.run(seed())
