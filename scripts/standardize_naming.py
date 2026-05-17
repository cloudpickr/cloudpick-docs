import os

# Updated full list of markdown files in the repo (excluding _book, .git, node_modules)
all_md_files = []
for root, dirs, files in os.walk('.'):
    if any(d in root for d in ['_book', '.git', 'node_modules']):
        continue
    for file in files:
        if file.endswith('.md'):
            all_md_files.append(os.path.join(root, file))

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    content = None
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'latin-1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
            
    if content is None:
        return

    # Special handling for internal technical identifiers or URLs we might want to keep?
    # Actually, the user asked for "GCP Google Cloud 명칭이 섞여있는데... 일관성을 가지는게 좋겠습니다"
    # So we'll stick to branding. Technical strings like .gcp.internal are borderline but let's see.
    # We will exclude common URL parts to avoid breaking links if possible, 
    # but the current replacement is simple.
    
    new_content = content
    # Replace Google Cloud Platform first
    new_content = new_content.replace('Google Cloud Platform', 'Google Cloud')
    # Replace GCP
    # To be safer, replace " GCP " or "| GCP |" or "GCP:"? 
    # But usually in this doc it's used as a brand.
    new_content = new_content.replace('GCP', 'Google Cloud')
    
    # Fix potential double "Google Cloud" if "Google Cloud Cloud" happens
    new_content = new_content.replace('Google Cloud Google Cloud', 'Google Cloud')
    new_content = new_content.replace('Google Clouding', 'GCPing') # Restore GCPing tool name
    new_content = new_content.replace('gcp.internal', 'gcp.internal') # Restore internal DNS

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

for f in all_md_files:
    process_file(f)
