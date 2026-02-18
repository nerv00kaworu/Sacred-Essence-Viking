# migrate_legacy.py
# Migrates MEMORY.md to Sacred Essence v3.1
# Author: Zhu (鑄)

import os
import re
import sys
from datetime import datetime

# Path Configuration
WORKSPACE_DIR = "/home/nerv0/.openclaw/workspace"
LEGACY_MEMORY_PATH = os.path.join(WORKSPACE_DIR, "MEMORY.md")
ENGINE_DIR = os.path.join(WORKSPACE_DIR, "memory/octagram/engine")

sys.path.append(ENGINE_DIR)
from main import main as engine_main

def migrate():
    if not os.path.exists(LEGACY_MEMORY_PATH):
        print(f"Legacy memory not found at {LEGACY_MEMORY_PATH}")
        return

    with open(LEGACY_MEMORY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by topics (headers like ## Topic)
    # We want to catch everything under ## ... until the next ## or ---
    sections = re.split(r'\n##\s+', content)
    
    # The first section is usually the header/metadata
    header = sections[0]
    print(f"Skipping header: {header.strip().splitlines()[0]}")

    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
            
        topic_title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        
        # Clean up topic title for engine
        # e.g. "🌟 核心身份" -> "Identity"
        # e.g. "✅ 系統與專案里程碑" -> "Milestones"
        topic_map = {
            "🌟 核心身份": "identity",
            "✅ 系統與專案里程碑": "milestones",
            "📍 當前狀態": "status",
            "🔧 工具使用規範": "guidelines",
            "🧭 核心價值與哲學": "philosophy",
            "🚨 與月影塵的約定（不可違反）": "rules",
            "2026-02-18：神髓 v3.1「維京矩陣」正式搬遷": "milestones"
        }
        
        # Find matches or use sanitized title
        target_topic = "general"
        for key, val in topic_map.items():
            if key in topic_title:
                target_topic = val
                break
        
        # Milestones section is special, it contains many sub-entries
        if target_topic == "milestones":
            # Split by ### 
            entries = re.split(r'\n###\s+', section)
            for entry in entries:
                entry_lines = entry.strip().splitlines()
                if not entry_lines: continue
                
                title = entry_lines[0].strip()
                if title.startswith("##"): continue # Skip the main header
                
                entry_content = "\n".join(entry_lines[1:]).strip()
                
                print(f"Migrating Milestone: {title}")
                # Mock sys.argv for engine_main
                import sys as _sys
                _sys.argv = [
                    "main.py", "encode",
                    "--topic", "milestones",
                    "--title", title,
                    "--content", entry_content,
                    "--abstract", title[:50]
                ]
                try:
                    engine_main()
                except Exception as e:
                    print(f"Failed to migrate {title}: {e}")
        else:
            # Generic migration
            print(f"Migrating Section: {topic_title} -> {target_topic}")
            import sys as _sys
            _sys.argv = [
                "main.py", "encode",
                "--topic", target_topic,
                "--title", topic_title,
                "--content", body,
                "--abstract", topic_title
            ]
            try:
                engine_main()
            except Exception as e:
                print(f"Failed to migrate {topic_title}: {e}")

if __name__ == "__main__":
    migrate()
