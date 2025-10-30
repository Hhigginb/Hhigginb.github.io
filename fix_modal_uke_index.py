import re
from datetime import datetime

def fix_modal_uke_index(file_path):
    """Change slideshow index from 1 to 2 in modal-uke section"""
    
    # Create backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Save backup
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Backup saved: {backup_path}")
    
    lines = content.split('\n')
    in_modal_uke = False
    changes_made = 0
    
    for i, line in enumerate(lines):
        # Detect start of modal-uke
        if 'id="modal-uke"' in line:
            in_modal_uke = True
            print(f"Line {i+1}: Found modal-uke start")
        
        # Detect end of modal-uke (start of next modal)
        if in_modal_uke and 'id="modal-art"' in line:
            in_modal_uke = False
            print(f"Line {i+1}: Found modal-uke end")
        
        # Replace slideshow index from 1 to 2 in modal-uke section
        if in_modal_uke:
            # Match patterns like plusDivs(-1,1), plusDivs(1,1), showDivs(n,1)
            old_line = line
            line = re.sub(r'plusDivs\((-?\d+),\s*1\)', r'plusDivs(\1, 2)', line)
            line = re.sub(r'showDivs\((\d+),\s*1\)', r'showDivs(\1, 2)', line)
            
            if line != old_line:
                lines[i] = line
                changes_made += 1
                # print(f"Line {i+1}: Updated index from 1 to 2")
    
    # Write the fixed content
    fixed_content = '\n'.join(lines)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"\nFixed {changes_made} slideshow index references in modal-uke")
    return changes_made

if __name__ == '__main__':
    file_path = 'hand.html'
    changes = fix_modal_uke_index(file_path)
    print(f"\nTotal changes: {changes}")
